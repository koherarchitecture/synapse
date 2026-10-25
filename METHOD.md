# Synapse: the method

*Prayas Abhinav, 20 October 2026. Version 1.5, 25 October 2026.*

## Why Koher and SDC use small models

Koher and Split-Domain Cognition (SDC) use small models for six reasons.

First, memory, deployment and inference cost. A small model needs little memory, can be deployed on a computer you already have, and costs very little to run. The reader inside rai, Koher's model that checks whether a description is complete, has 33 million parameters and runs on an ordinary computer's CPU.

Second, the syntax of intelligence, which is what [Split-Domain Cognition](https://splitdomaincognition.org) describes.

Third, small models are fast.

Fourth, they are less expensive to train. RAM's reader trains in about 155 seconds a run on a single NVIDIA GB10.

Fifth, they give more control over the kind of logical steps performed, and over when each is performed.

Sixth, they are less of a black box.

### An open problem

Reading is still built on copyright violations. The readers in rai and RAM are fine-tuned from a base model whose pretraining drew on BookCorpus, thousands of self-published books taken without their authors being asked, and on text scraped from the web.

## The steps

First, identify what function of intelligence has to be performed. Name it narrowly: for an office note, for example, knowing who will do each act.

Then break that function down into a series, or parallel arrays, of singular operations, each doing one thing. RAM, Koher's model that points at who will do each act in office writing, breaks its function into four: finding the acts, asking one fixed question of each, pointing at the words that name the doer, and checking that those words name somebody.

For each singular operation, figure out whether a small model can perform it. Some need no model at all. In RAM a parser finds the acts and plain code does the checking; only the pointing is a trained model.

For each model that remains, identify the kind of data needed to train it. RAM's reader learnt from 14,000 generated rows of office writing.

Then build the model.

## What runs the layers

Code runs the layers, never a model. A table written by people says which layers each kind of case goes through, in what order, and where a case goes when a layer does not know. One table can hold every small model in a system, so each model is loaded once and shared; that table is the router. A model that plans the order, or writes a query, a sub-question or a step for another model, is outside Synapse whatever its size, because it would take over what the fifth reason above keeps: which operation runs, and when.

A harder job does not call for a bigger model. It usually means the function has not yet been broken into singular operations. Semantic search sounds like a job for a large model; it is one small operation. When a text is too long for a reader to read whole, such as a long office file or a collection of documents, and a person asks about one matter in it in their own words, a finder answers with the number of the passage closest in meaning to those words, or nothing. The words need not match: *ink for the printer* finds *the printer cartridges are over*. The finder is an encoder of 110 million parameters. The reader then asks its one fixed question of that passage only.

Semantic search starts with one kind of model: an encoder, which turns a passage into a list of numbers so that passages close in meaning get close numbers. Each passage is encoded once and kept, so a collection of any length is searched by comparing numbers. Two other kinds can follow it on the few passages it found, only where they are measured to help: a late-interaction model, which keeps numbers for every word of a passage rather than one set for the whole, and a cross-encoder, which reads the question and one passage together and returns a score. Both are slower than the encoder, and like it, both return numbers and write nothing. A model that rewrites the person's question, or writes an imagined answer to search with, is not needed. Synapse leaves it out.

An encoder groups passages by topic. It cannot tell which of them someone who works in a field would give as the answer. A farmer asks why the new leaves of a groundnut crop are turning yellow between the veins. Passages on nitrogen shortage, iron shortage and waterlogging all describe yellow leaves, and an encoder places them close together; someone who knows crops reads *new leaves* and *between the veins* and, on the chalky soils groundnut is often grown on, takes the passage on iron as the likely one. Where held-out cases show the finder missing what a field would pick, a domain guide is added. It is a small model trained for that one field, on pairs of a question and a passage that people who know the field have labelled. The guide reads the question with each passage the finder found and answers with a number from its own list, a passage, a label or a region, or nothing. The labels carry the judgement; the guide returns a passage number.

A field's problem has more than one aspect, an aspect being one question a passage is checked for, and each aspect gets its own guide, in the same way *The steps* break a function into singular operations. In agriculture one guide reads a passage of advice for what it does to the other life in and around the field. Another reads it for the regions it applies to, from a list of regions written in advance. Each answers with a number from its own list, or nothing, and code combines the answers by rules people wrote. One such rule: advice meant for another region never reaches the farmer. This rule overrides the others.

## What small means

Small means size. It also means that the hardware needed to run the model should be free of cost: no paid server and no fee for each answer. If needed, a model this small can be run in a web browser, on your own device.

Small also describes a smaller copyright theft. A small model is trained on less text than a large one, so less is taken. rai's and RAM's readers are trained further on generated rows, and what was taken without asking sits in the base model they start from and in the large model that helped write those rows. It is still theft (see the open problem above).

### How the idea of small has changed

- **24 September 2026.** The word first described the decision: layers of small models, each taking one small decision that can be checked.
- **2 October 2026.** The question moved from the model to its output. Small named the part a model plays: the size of the window, not the door. What has to stay small is what passes out of the model, a few tokens set in the call and checked in code, and only ever a number, never English. So a large or hosted model held to that window by code also counts as small.
- **4 October 2026.** Keeping every word human does not scale, but in a narrower use it is fine.
- **20 October 2026, version 1.0 of this page.** Size, and hardware to run the model on that should be free of cost.
- **Version 1.1, the same day,** added running in a browser.
- **Version 1.2** added copyright.
- **Version 1.4.** The window still holds; it describes more specific things now.
- **Version 1.5, 25 October 2026.** No bigger model is added to orchestrate the small ones, and semantic search becomes one more small layer.

## Where it does not fit

Synapse does not fit generation jobs.

## What goes wrong without it

Without it, the current logistics of AI stay as they are.
