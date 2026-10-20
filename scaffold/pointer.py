"""A pointer: one question asked of a text given as a list of passages.

It answers with the number of the passage that holds the answer, or None. The reader is
extractive (deepset/minilm-uncased-squad2, the base rai and RAM were trained from): it can
only point at words already in the text, never write one. Only the first ~380 tokens are
read; an answer past that is not found, so the case goes to a person.
"""
import torch
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from transformers.utils import logging

logging.set_verbosity_error()
logging.disable_progress_bar()

BASE = "deepset/minilm-uncased-squad2"
MAX_SPAN = 30


class Pointer:
    def __init__(self, question, threshold, model=BASE):
        """threshold: how far the best span must score above 'no answer'. Measure it on cases keyed by hand."""
        self.question, self.threshold = question, threshold
        self.tok = AutoTokenizer.from_pretrained(model)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model).eval()

    def margin(self, passages):
        """The best span's score over 'no answer', and the character where it starts."""
        enc = self.tok(self.question, " ".join(passages), return_tensors="pt", truncation="only_second",
                       max_length=384, return_offsets_mapping=True)
        with torch.no_grad():
            out = self.model(input_ids=enc["input_ids"], attention_mask=enc["attention_mask"])
        s, e = out.start_logits[0], out.end_logits[0]
        text = [i for i, sid in enumerate(enc.sequence_ids(0)) if sid == 1]
        best, i = max(((s[i] + e[j]).item(), i) for i in text for j in text if i <= j < i + MAX_SPAN)
        return best - (s[0] + e[0]).item(), enc["offset_mapping"][0][i][0].item()

    def __call__(self, case, passages):
        margin, start = self.margin(passages)
        if margin <= self.threshold:
            return None
        end = 0
        for k, passage in enumerate(passages):
            end += len(passage) + 1
            if start < end:
                return k
        return None
