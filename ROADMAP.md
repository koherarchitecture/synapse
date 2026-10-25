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

## Agriculture, one guide for each aspect: 1.9.0 to 1.11.0

Agriculture comes first. Each aspect gets a guide and a minor version, with labelled pairs and a held-out set of its own. Each guide is trained from `cross-encoder/ettin-reranker-17m-v1` or the smallest cross-encoder that does the job, on pairs that share nothing with its held-out set. No example in these guides' data names an animal product. That is a rule Koher keeps for its own work and examples; others choose their own (see the README). Each ships only if wrong yes is zero on its held-out set; if the finder alone already does the guide's work, the release says this aspect needs no guide.

**1.9.0: biodiversity.** The guide reads a passage of crop advice and answers with what it does to the wild plants, insects, birds and soil life around the crop, from a list written in advance: it keeps that life, it harms it, or it does not touch it. Passages and labels are written by hand and checked by someone who knows the ecology of farmed land. Layers in `run` cannot yet see what earlier layers chose, and a guide that reads the passage the finder chose needs to, so 1.9.0 also lets a layer's list depend on the choices made so far, without breaking existing calls.

**1.10.0: regions.** The guide answers with the regions a passage of advice applies to, from a list such as a country's agro-climatic zones. Code drops advice meant for another region before anything reaches the farmer. Labels are checked by someone who knows the regions.

**1.11.0: the cause of a problem.** Questions a farmer asks about what is wrong with a crop, and passages on plant nutrition, water and disease. Passages about yellow leaves look alike to an encoder whatever their cause. The guide reads the question with each passage the finder found and points at the one that answers, as checked by someone who works with crops. The finder is measured alone and with the guide over the five passages it ranks highest, and the number of correct passages found must not fall.

METHOD.md's paragraphs on domain guides are published before any guide exists and released with 1.6.0; each trained guide and its example ship in its own version above.

## Deferred

- **A chooser that picks the pipeline in the router**, for cases that arrive without saying what kind they are. *Condition:* hand-keyed cases show that such cases are common. Until then the sender, or a rule written in advance, says the kind.
- **A finder for Hindi**, with a multilingual encoder from the README's table. *Condition:* a hand-keyed Hindi set, written or checked by a speaker of Hindi.
- **Hinglish in Roman script.** *Condition:* the Hindi finder has shipped, and a hand-keyed Hinglish set exists.
- **A base model trained on less text taken without permission**, the open problem in METHOD.md. *Condition:* a decision to train one.
- **Guides for other domains**, one guide each. *Condition:* a field is chosen, and people who know it have labelled a set of question and passage pairs.
- **2.0.0.** No major version is planned (see VERSIONING.md).
