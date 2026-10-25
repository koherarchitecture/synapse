# Roadmap

Every planned version, what it adds and how it is checked. Versioning is described in [VERSIONING.md](VERSIONING.md). Each feature is assigned to one version, or sits under *Deferred* with the condition that would give it one.

**How every version is measured.** On every worked example, counting held-out cases only:

- **wrong yes**: a layer named an item the key does not name;
- **found**: a case with an answer, answered correctly;
- **handed on**: a case sent to a person or to rules written in advance.

A version that changes a layer ships only if wrong yes stays at zero on every example and found does not fall on any. At 1.5, `office_note.py` found 4 of 5, with no wrong yes and one note handed on; `long_note.py` found 5 of 5 with the finder and none without it, with no wrong yes.

## 1.5.1: patch

- `runs` and `narrowed` move into `layers.py`, which needs no packages, so `scaffold/test_layers.py` can check them with stand-in layers. `finder.py` still exports both, so `from finder import narrowed` keeps working.
- `scripts/check.sh` skips a virtual environment inside the tree, whose installed packages contain strings its secret-key check mistakes for keys.
- The README's long sentence on `run` is split in two.

The test must fail on a deliberately broken `narrowed` and pass on the real one, and the fresh-clone test must pass with a virtual environment inside the clone.

## 1.6.0: smaller encoders for the finder

`long_note.py` is run with two smaller encoders beside `bge-base-en-v1.5` (110M): `BAAI/bge-small-en-v1.5` (33M) and `ibm-granite/granite-embedding-small-english-r2` (48M). Each uses its own query prefix, and each threshold is set on the ten notes that are not held out. The README's model table marks which were tried. The aim is the same finds with fewer parameters, measured on the held-out long notes for each encoder. If no smaller encoder matches, the release says so and the default stays `bge-base-en-v1.5`.

## 1.7.0: the chooser on real recordings

`chooser.py` has been tried only on three made-up sounds, where it refused all three, and no threshold has been measured for it. 1.7.0 measures it on openly licensed recordings of a doorbell, a knock and a smoke alarm, keyed by hand before the model hears them, with the threshold set on half and reported on the other half.

## 1.8.0: one layer in a web browser

METHOD.md says a model this small can be run in a web browser if needed; the scaffold has not yet shown it. The pointer is exported to ONNX and run in a web page with transformers.js on the held-out office notes. Its answers must match the CPU's on all ten, and the page's download size is stated.

## Deferred

- **A chooser that picks the pipeline in the router**, for cases that arrive without saying what kind they are. *Condition:* hand-keyed cases show that such cases are common. Until then the sender, or a rule written in advance, says the kind.
- **A finder for Hindi**, with a multilingual encoder from the README's table. *Condition:* a hand-keyed Hindi set, written or checked by a speaker of Hindi.
- **Hinglish in Roman script.** *Condition:* the Hindi finder has shipped, and a hand-keyed Hinglish set exists.
- **A base model trained on less text taken without permission**, the open problem in METHOD.md. *Condition:* a decision to train one.
- **2.0.0.** No major version is planned (see VERSIONING.md).
