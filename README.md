<h1 align="center">Synapse</h1>

<p align="center"><strong>Layers of small models: a method for using AI in which no model writes a word.</strong></p>

<p align="center">
  <a href="LICENSE-METHOD.md"><img src="https://img.shields.io/badge/method-CC--BY--4.0-373E3C" alt="method licence CC-BY-4.0"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/scaffold-AGPL--3.0-373E3C" alt="scaffold licence AGPL-3.0"></a>
  <a href="CITATION.cff"><img src="https://img.shields.io/badge/cite-CITATION.cff-D59A3A" alt="cite with CITATION.cff"></a>
  <a href="https://splitdomaincognition.org"><img src="https://img.shields.io/badge/follows-Split--Domain_Cognition-2E7D5B" alt="follows Split-Domain Cognition"></a>
</p>

---

The method is Prayas Abhinav's. He first set it out on 24 September 2026, and it is published by Koher. The method itself, in his words, is in **[METHOD.md](METHOD.md)**. This page gives its shape, two working models built on it, a small scaffold in code, and how to cite it.

<p align="center"><img src="assets/layers.svg" width="860" alt="A case goes to several small models, each taking one small decision and answering with a number or nothing. Code checks every answer. The top call is made only from a list written in advance, and the words a person reads were written by people. Any don't-know goes to a person, or to rules people wrote in advance."></p>

## Two models built on it

Both are released by Koher. Each has its own reader, fine-tuned from the same 33-million-parameter base, which runs on an ordinary CPU and can only point at words already in front of it.

<p align="center"><img src="assets/rai-ram.svg" width="860" alt="rai and RAM side by side in the same six rows: what is written in advance, the small decision, the answer, what code checks, the top call, and what was measured."></p>

**[rai](https://github.com/koherarchitecture/rai)** checks whether a description is complete. A form of questions is fixed before anyone answers. For each question the reader points at the phrase in the person's answer that answers it, or at nothing. Code refuses vague, deferred and empty answers. The top call is one of two words, *complete* or *not complete*, and rai never says why. On four forms it never trained on, version 0.3.8 found 64 of 96 honest answers and counted none of 72 non-answers. It misses real answers more often than it lets a wrong one through; the method prefers that error to the other.

**[RAM](https://github.com/koherarchitecture/ram)** points at who is doing each act in a piece of office writing. A parser finds the acts and asks one fixed question of each: who will do this? The reader points at the words that name the doer, or at nothing. Code refuses titles that name nobody. The top call, for each act, is one of two lines: *&lt;doer&gt; karega* (will do), with the doer copied from the note, or *RAM bharose* (left to chance). On its five test sets, which were written by models and keyed by hand, version 0.5 named the right doer, or nobody, for all 178 acts, against 162 for the parser alone; notes written by office staff have not been measured yet. The doer RAM prints is copied from the note, so no word of it is the model's.

## The code

Four small files in `scaffold/`, to copy into your own work.

- **`layers.py`**, plain Python with no packages, is the part every system built this way shares. `window` lets an answer through only as the number of an item in the list the model was given; anything else, words included, counts as *don't know*. `run` puts a case through each layer, stops it the moment a layer does not know and hands it on, to a person or to rules people wrote in advance, and makes the top call from a table people wrote, so every sentence a person reads comes from that table. A layer's list is either fixed beforehand or taken from the case itself, such as its sentences. `route` is the router: a table written by people that sends each kind of case to its pipeline, so several pipelines share the same small models and no model chooses the order. A kind the table does not hold goes to a person.
- **`pointer.py`** asks one question of a text given as a list of sentences and answers with the number of the sentence that holds the answer, or nothing. It uses the base that rai's and RAM's readers were fine-tuned from, `deepset/minilm-uncased-squad2`, as it comes. It reads the first 380 or so tokens; an answer past that is not found, and the case is handed on.
- **`finder.py`** is semantic search as a layer. When a text is too long for the pointer, such as a long office file or a collection of documents, and a person asks about one matter in it in their own words, the finder answers with the number of the passage closest in meaning to those words, or nothing. It uses `BAAI/bge-base-en-v1.5` (110M parameters, MIT licence), an encoder that turns text into numbers and writes nothing. `narrowed` joins it to the pointer as one layer: the finder chooses a run of sentences, the pointer reads only that run.
- **`chooser.py`**, with no packages, holds a model that scores labels to a fixed list: the number of the item it scores highest, or nothing when that score is under the threshold or the model's top label is not on the list. It has been tried once, with an AudioSet sound classifier (`MIT/ast-finetuned-audioset-10-10-0.4593`) on three made-up sounds, a pure tone, beeps and silence, against a list of doorbell, knock and smoke alarm. It returned nothing for all three, because each sound's top label (*Sine wave*, *Beep, bleep*, *Silence*) is not on the list. That trial shows refusal only; it has not yet been shown choosing a right item, and no threshold was measured for it.

Before a layer is used, its threshold is set on cases keyed by hand before the model sees them, as in the example below.

```bash
python3 scaffold/test_layers.py          # the checks, no packages needed
pip install -r requirements.txt          # torch and transformers, for the pointer
python3 examples/office_note.py          # the worked example
python3 examples/long_note.py            # semantic search in front of the pointer, and the router
```

**The worked example**, `examples/office_note.py`, asks of twenty short office notes *who will do it?* The notes and their keys were written by hand for it before the reader saw them. The threshold is set on ten notes and reported on the other ten, which it never saw. On those ten the pointer found 4 of the 5 people named and named nobody wrongly; the fifth note (*Imran will buy it tomorrow morning*) scored between *no answer* and the threshold, so it was handed on instead of answered. Every note comes out as one of two fixed sentences, *Sent on: the note names who will do it* or *Returned: the note does not say who will do it*, or as a case handed on. Twenty notes show the method's shape; they are not a measurement of the reader. Tested with Python 3.12 and torch 2.14, with transformers 5.17 and again with 5.20 in a fresh install from `requirements.txt` alone; both gave the same results.

**The second example**, `examples/long_note.py`, is semantic search. It makes the same twenty notes long: two and a half paragraphs of office background (a TA bill, a GSTR-2A mismatch, income certificates from the Tehsildar's office, a fire safety audit, a government survey and an electricity bill) go in front of each note and the rest after it, so the sentence naming the doer falls past the pointer's reach. The background names people too, for what they did before, which is the trap for a reader that sees only the start. Each note comes with the matter a person might ask about, in other words than the note's, such as *ink for the printer* for *the printer cartridges are over*. Five of the ten held-out notes name a doer, and the pointer alone found none of them. With the finder in front, the finder chose a run holding the doer in all 5, the pointer found all 5, and nobody was named wrongly. To get there, the pointer's threshold had to rise from 5.47 to 10.33, because background sentences naming people fell inside the runs the finder chose. The example ends with the router: a rule on length sends each short note to the pointer alone and each long one to the finder and pointer. Twenty notes are too few to measure anything. The encoder is a further download of about 440 MB. Tested with Python 3.12, torch 2.14 and transformers 5.20.

**Models for the finder.** METHOD.md sets out the kinds: an encoder first, then a late-interaction model (ColBERT) or a cross-encoder on the few passages it found, only where that is measured to help. Only `bge-base-en-v1.5` has been tried here. The rest are listed from their model cards, checked on 25 October 2026, and each is under an open licence. Each needs its own query prefix or instruction; leaving it out breaks the search.

| Kind | Model | Size | Licence | Languages | On Hugging Face since |
|---|---|---|---|---|---|
| encoder | `BAAI/bge-base-en-v1.5` (used here) | 110M | MIT | English | Sep 2023 |
| encoder | `BAAI/bge-small-en-v1.5` | 33M | MIT | English | Sep 2023 |
| encoder | `sentence-transformers/all-MiniLM-L6-v2` | 23M | Apache-2.0 | English | Mar 2022 |
| encoder | `MongoDB/mdbr-leaf-ir` | 23M | Apache-2.0 | English | Aug 2025 |
| encoder | `ibm-granite/granite-embedding-small-english-r2` | 48M | Apache-2.0 | English | Jul 2025 |
| encoder | `ibm-granite/granite-embedding-97m-multilingual-r2` | 97M | Apache-2.0 | 52, Hindi among them | Apr 2026 |
| encoder | `intfloat/multilingual-e5-small` | 118M | MIT | many, Hindi among them | Jun 2023 |
| encoder | `microsoft/harrier-oss-v1-270m` | 268M | MIT | 94, Hindi among them | Mar 2026 |
| encoder | `Qwen/Qwen3-Embedding-0.6B` | 596M | Apache-2.0 | multilingual | Jun 2025 |
| late interaction | `mixedbread-ai/mxbai-edge-colbert-v0-17m` | 17M | Apache-2.0 | English | Oct 2025 |
| late interaction | `lightonai/LateOn` | 149M | Apache-2.0 | English | Mar 2026 |
| cross-encoder | `cross-encoder/ettin-reranker-17m-v1` | 17M | Apache-2.0 | English | May 2026 |
| cross-encoder | `cross-encoder/ms-marco-MiniLM-L6-v2` | 23M | Apache-2.0 | English | Mar 2022 |
| cross-encoder | `ibm-granite/granite-embedding-reranker-english-r2` | 150M | Apache-2.0 | English | Aug 2025 |

For Hindi, the multilingual encoders are the place to start; Hinglish written in Roman script has not been tested with any of them. Models under non-commercial licences, or licences of their makers' own, are left out of the table.

`scripts/check.sh` runs before every release: it refuses without `METHOD.md`, when a check fails, or when anything in the tree looks like a key.

## Cite it

Use GitHub's *Cite this repository* button, which reads `CITATION.cff`, or:

> Abhinav, P. (2026). *Synapse: layers of small models* (Version 1.5). Koher. https://github.com/koherarchitecture/synapse

If you cite a model built on it, cite rai or RAM through their own `CITATION.cff` as well. The idea underneath, Split-Domain Cognition, is at https://splitdomaincognition.org.

## Licence

The method (`METHOD.md`, this README and the figures) is under the Creative Commons Attribution 4.0 International licence: see `LICENSE-METHOD.md`. The scaffold code is under the GNU Affero General Public License v3.0: see `LICENSE`.
