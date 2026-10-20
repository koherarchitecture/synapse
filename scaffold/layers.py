"""Layers of small models, in code.

Every model answers with a number or with nothing. Code checks each answer, a case
nobody can settle goes to a person, and the only words anyone reads were written
by people beforehand.
"""

PERSON = "person"


def window(answer, choices):
    """Pass an answer only as the number of an item in the list the model was given.

    Anything else, words included, counts as don't know.
    """
    if type(answer) is int and 0 <= answer < len(choices):
        return answer
    return None


def run(layers, case, decide, words):
    """Run each layer on one case, then make the top call from a table written in advance.

    layers: a list of (name, model, choices); model(case, choices) returns a number or None.
        choices is a list written in advance, or a function that takes the case and returns
        its own parts, such as its sentences, for a model that points into the text.
    decide: takes {name: chosen item} and returns a key of words, or None.
    words: every sentence a person may read, written by people.

    Returns ("say", sentence) or (PERSON, where it stopped).
    """
    chosen = {}
    for name, model, choices in layers:
        if callable(choices):
            choices = choices(case)
        i = window(model(case, choices), choices)
        if i is None:
            return PERSON, name
        chosen[name] = choices[i]
    key = decide(chosen)
    if key not in words:
        return PERSON, "decide"
    return "say", words[key]
