# Synapse: the method

*Prayas Abhinav, 20 October 2026. Version 1.2.*

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

## Where it does not fit

Synapse does not fit generation jobs.

## What goes wrong without it

Without it, the current logistics of AI stay as they are.
