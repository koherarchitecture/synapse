"""A worked example: does an office note name who will do the work?

One layer, a Pointer, asks "Who will do it?" and answers with the number of the sentence
that names the doer, or with nothing. The threshold is set on one half of the notes and
reported on the other half, which it never saw. Code makes the top call from three
sentences written in advance; a note the pointer cannot settle goes to a person.

The notes and their keys were written by hand for this example, before the reader saw them.
Twenty notes show the method's shape. They are not a measurement of the reader.

Run from the repository root:  python3 examples/office_note.py
"""
import sys

sys.path.insert(0, "scaffold")
from layers import PERSON, run  # noqa: E402
from pointer import Pointer  # noqa: E402

# (the note, sentence by sentence; the number of the sentence naming the doer, or None if none does)
TUNE = [
    (["The caterer's bill came in on Monday.", "Meena will check it against the order."], 1),
    (["The projector in room 4 is not working.", "It needs to be looked at before Friday."], None),
    (["Ravi from accounts will release the advance today.", "The receipt is attached."], 0),
    (["Leave for the 14th has been applied for.", "Approval is awaited."], None),
    (["The visitor passes are ready.", "Suresh at the gate will hand them out at nine."], 1),
    (["The tender file has come back from finance.", "It may be put up again after corrections."], None),
    (["Please note the new timings.", "Anjali will update the notice board this evening."], 1),
    (["The vehicle log is incomplete for October.", "Necessary action may be taken."], None),
    (["Mr. Desai will sign the bills once they are checked.", "The bills are on his table."], 0),
    (["The rent agreement expires next month.", "Renewal is under consideration."], None),
]
HELD_OUT = [
    (["The printer cartridges are over.", "Kiran will order new ones from the store."], 1),
    (["The minutes of the meeting are pending.", "They should be circulated soon."], None),
    (["Farida will book the hall for the workshop.", "The dates are 3 and 4 November."], 0),
    (["The water cooler on the second floor leaks.", "The matter is being looked into."], None),
    (["The fee receipts have been checked.", "Mohan will send them to the bank on Thursday."], 1),
    (["A reminder may be sent to the vendor.", "The payment is overdue."], None),
    (["Priya will collect the forms from all three hostels.", "The last date is Friday."], 0),
    (["The audit queries have been received.", "Replies are to be prepared."], None),
    (["The stamp paper is needed for the contract.", "Imran will buy it tomorrow morning."], 1),
    (["The website notice is out of date.", "It may kindly be updated."], None),
]

WORDS = {  # every sentence a person reads, written beforehand
    "named": "Sent on: the note names who will do it.",
    "nobody": "Returned: the note does not say who will do it.",
}


def decide(chosen):
    return "named" if chosen["who"] != "nobody named" else "nobody"


def wrong_yes(pointer, cases, threshold):
    """Notes where the pointer named a sentence the key does not: the failure that matters."""
    pointer.threshold = threshold
    return sum(1 for note, key in cases if (got := pointer(None, note)) is not None and got != key)


pointer = Pointer("Who will do it?", threshold=0.0)
margins = sorted(pointer.margin(note)[0] for note, _ in TUNE)
threshold = next(t for t in [0.0] + margins if wrong_yes(pointer, TUNE, t) == 0)
pointer.threshold = threshold
print(f"threshold set on the first ten notes: {threshold:.2f}")

found = sum(1 for note, key in HELD_OUT if key is not None and pointer(None, note) == key)
named = sum(1 for _, key in HELD_OUT if key is not None)
print(f"on the ten held-out notes: {found} of {named} doers found, "
      f"{wrong_yes(pointer, HELD_OUT, threshold)} wrong yes")


# The whole layered run on each held-out note. A pointer that does not know sends the note to a person;
# a pointer that finds nobody is a real answer, so "nobody named" is on the list it can choose from.
def who(case, choices):
    k = pointer(case, choices[:-1])
    return len(choices) - 1 if k is None and pointer.margin(choices[:-1])[0] < 0 else k


for note, _ in HELD_OUT:
    print(" ".join(note), "->", run([("who", who, lambda case: case + ["nobody named"])], note, decide, WORDS))
