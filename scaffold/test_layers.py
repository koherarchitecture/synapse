"""Run with: python3 scaffold/test_layers.py   (no packages needed)

Each layer here is a stand-in for a model. A real one is wrapped so that it returns
the number of an item in the list it was given, or None.
"""

from chooser import chooser
from layers import PERSON, route, run, window

NOTE = "The caterer's bill came in on Monday. Meena will check it against the order."
PASSAGES = NOTE.split(". ")
DONE_BY = ["a named person", "nobody named"]

WORDS = {  # written by people, before any case is read
    "named": "Sent on: somebody is named to do it.",
    "unnamed": "Returned: the note names nobody to do it.",
}


def decide(chosen):
    return {"a named person": "named", "nobody named": "unnamed"}.get(chosen["done by"])


def layer(answer):
    return lambda case, choices: answer


# The window lets through only a number that names an item.
assert window(1, PASSAGES) == 1
assert window(None, PASSAGES) is None
assert window(2, PASSAGES) is None                      # past the end of the list
assert window(-1, PASSAGES) is None
assert window(True, PASSAGES) is None                   # a yes is not a number
assert window("Meena will check it", PASSAGES) is None  # words are never an answer

# Every layer answers: the top call comes from the table, in words written in advance.
assert run([("which passage", layer(1), PASSAGES), ("done by", layer(0), DONE_BY)],
           NOTE, decide, WORDS) == ("say", WORDS["named"])
assert run([("which passage", layer(1), PASSAGES), ("done by", layer(1), DONE_BY)],
           NOTE, decide, WORDS) == ("say", WORDS["unnamed"])

# A layer that does not know, or answers in words, stops the case and hands it to a person.
assert run([("which passage", layer(None), PASSAGES), ("done by", layer(0), DONE_BY)],
           NOTE, decide, WORDS) == (PERSON, "which passage")
assert run([("which passage", layer(1), PASSAGES), ("done by", layer("Meena"), DONE_BY)],
           NOTE, decide, WORDS) == (PERSON, "done by")

# A top call outside the table is handed on too.
assert run([("done by", layer(0), DONE_BY)], NOTE, lambda chosen: "approve", WORDS) == (PERSON, "decide")

# A layer's list can come from the case itself, such as its sentences, for a model that points into the text.
sentences = lambda case: case.split(". ")
assert run([("which passage", layer(1), sentences), ("done by", layer(0), DONE_BY)],
           NOTE, decide, WORDS) == ("say", WORDS["named"])
assert run([("which passage", layer(2), sentences)], NOTE, decide, WORDS) == (PERSON, "which passage")

# The chooser holds any model that scores labels to the list: off the list or under the threshold is don't know.
SOUNDS = ["doorbell", "knock"]
assert chooser(lambda case: {"knock": 0.8, "music": 0.1}, 0.5)(None, SOUNDS) == 1
assert chooser(lambda case: {"knock": 0.4, "music": 0.1}, 0.5)(None, SOUNDS) is None   # under the threshold
assert chooser(lambda case: {"sine wave": 0.98, "knock": 0.01}, 0.5)(None, SOUNDS) is None  # top label not on the list

# The router sends a case to the pipeline its table names for that kind; an unknown kind goes to a person.
TABLE = {
    "short": ([("which passage", layer(1), sentences), ("done by", layer(0), DONE_BY)], decide, WORDS),
    "long": ([("which passage", layer(None), sentences)], decide, WORDS),
}
assert route(TABLE, "short", NOTE) == ("say", WORDS["named"])
assert route(TABLE, "long", NOTE) == (PERSON, "which passage")
assert route(TABLE, "invoice", NOTE) == (PERSON, "route")

print("all checks pass")
