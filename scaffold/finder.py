"""A finder: semantic search as a layer.

The use: a text is too long to read whole, such as a file of office notes or a collection of
documents, and a person asks about one matter in it in their own words. The finder answers with
the number of the passage closest in meaning to those words, or None when even the closest is
not close enough. The words need not match the text's: "ink for the printer" finds "the printer
cartridges are over".

The encoder (BAAI/bge-base-en-v1.5, 110M parameters) turns text into
numbers and compares them; it cannot write a word. Put it in front of the pointer when a text is
longer than the pointer reads: the finder chooses the passage, the pointer answers its fixed
question inside it.
"""
import torch
from transformers import AutoModel, AutoTokenizer
from transformers.utils import logging

logging.set_verbosity_error()
logging.disable_progress_bar()

BASE = "BAAI/bge-base-en-v1.5"
PREFIX = "Represent this sentence for searching relevant passages: "  # the encoder's query prefix, not optional


class Finder:
    def __init__(self, query, threshold, model=BASE):
        """query: words written in advance, or a function that takes the case and returns the words a person asked with.
        threshold: the lowest similarity that still counts as found. Measure it on cases keyed by hand."""
        self.query, self.threshold = query, threshold
        self.tok = AutoTokenizer.from_pretrained(model)
        self.model = AutoModel.from_pretrained(model).eval()

    def embed(self, texts):
        enc = self.tok(texts, padding=True, truncation=True, max_length=512, return_tensors="pt")
        with torch.no_grad():
            vectors = self.model(**enc).last_hidden_state[:, 0]
        return torch.nn.functional.normalize(vectors, dim=-1)

    def similarity(self, case, passages):
        """The best passage's similarity to the query, and its number."""
        query = self.query(case) if callable(self.query) else self.query
        best, k = (self.embed(passages) @ self.embed([PREFIX + query])[0]).max(dim=0)
        return best.item(), k.item()

    def __call__(self, case, passages):
        best, k = self.similarity(case, passages)
        return k if best > self.threshold else None


def runs(sentences, size):
    """Runs of `size` sentences, each starting halfway through the last, so no sentence sits only at an edge."""
    return [(i, sentences[i:i + size]) for i in range(0, max(len(sentences) - size // 2, 1), size // 2)]


def narrowed(finder, pointer, size):
    """One layer from two: the finder chooses a run of sentences, the pointer reads only that run.

    It answers with the number of a sentence in the whole text, or None if either does not know.
    """
    def layer(case, sentences):
        found = runs(sentences, size)
        k = finder(case, [" ".join(run) for _, run in found])
        if k is None:
            return None
        start, run = found[k]
        i = pointer(case, run)
        return None if i is None else start + i
    return layer
