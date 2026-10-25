# Versioning

Synapse uses semantic versioning, MAJOR.MINOR.PATCH, from the release after 1.5. The version number says whether either of two things a person can build on has changed.

The first is the method's rules. Every model answers with a number or nothing. Code checks every answer, and code, not a model, runs the layers. A case no layer can settle goes to a person or to rules written in advance. Every sentence a person reads was written by people. Generation is outside the method. These rules are stated in [METHOD.md](METHOD.md) and in this repository's README.

The second is the scaffold's code: `window`, `run` and `route` in `layers.py`, `Pointer`, `Finder`, `runs`, `narrowed` and `chooser`, with the arguments they take and what they return.

**MAJOR** (2.0.0): a system or a piece of code built to the last version no longer works with this one, or no longer follows the method. A rule is removed or narrowed, or a function's arguments change so that calling code breaks. The first line of a major version's release notes says what it breaks.

**MINOR** (1.6.0): something is added and everything that was true stays true: a new kind of layer, a new section of METHOD.md that adds a use without changing a rule, a new worked example, or a rule widened in a way no earlier system is hurt by. Its release notes name the check it was tested with and the result.

**PATCH** (1.5.1): nothing a person builds on changes. Wording, corrections, diagrams, the README, tests, the release checks, and fixes that change no behaviour. A worked example whose measured numbers change is a minor version, not a patch. Changes to the wording of METHOD.md that change no rule are patches, and they are gathered into one release rather than given a number each.

**The record of *small*.** METHOD.md keeps a dated record of how the idea of small has changed. A new line there is a patch when it says the idea more clearly, a minor when it widens what counts as small, and a major when it narrows it so that an earlier system no longer counts.

## Releasing

A version is written in [ROADMAP.md](ROADMAP.md), with what it adds and how it is checked, before it is built. A change that is not on the roadmap is added to it first.

Each release:

1. runs `scripts/check.sh`;
2. is pushed, then cloned into an empty directory;
3. is installed by following the README exactly, and every example is run there.

Three places always carry the new version: `version` and `date-released` in `CITATION.cff`, the citation line in the README, and the git tag with its GitHub release (`v1.6.0`). The second line of METHOD.md changes only when METHOD.md's text does, and so names the version in which its text last changed.

## Versions before this scheme

Versions 1.0 to 1.5 were numbered with two parts and a minor step for every change, four of them in one day for changes to the wording of METHOD.md. They keep their numbers, since they are cited and linked. Under this scheme they would have read: 1.0 → 1.0.0 · 1.1, the method in prose → 1.0.1 · 1.2, copyright added to what small means → 1.0.2 · 1.3, a case may go to rules written in advance → 1.1.0 · 1.4, a restatement of the window rule → 1.1.1 · 1.5, the router and the finder → 1.2.0. Numbering continues from 1.5: the next patch is 1.5.1 and the next minor 1.6.0.
