"""A chooser: any model that scores labels, held to a list written in advance.

It answers with the number of the list item the model scores highest, or None when
that score is under the threshold or the model's top label is not on the list.
"""


def chooser(scores_for, threshold):
    """scores_for(case) returns {label: score}. The threshold is measured, never guessed."""
    def layer(case, choices):
        scores = scores_for(case)
        label = max(scores, key=scores.get)
        if scores[label] < threshold or label not in choices:
            return None
        return choices.index(label)
    return layer
