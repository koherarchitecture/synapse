"""A worked example of semantic search: one matter asked about in notes longer than the pointer reads.

The use. A note, a file or a collection is too long to read whole, and a person asks about
one matter in it, in their own words: "who is doing the ink for the printer?" The finder
(semantic search, an encoder of 110M parameters) chooses the run of sentences closest in meaning to
the matter the person named, though the words need not match the note's. The pointer then
asks its one fixed question, "Who will do it?", of that run only, and answers with a sentence
number or nothing.

The notes. The twenty notes of office_note.py are made long: two and a half paragraphs of
office background go in front of each and the rest after it, so the sentence naming the doer
falls past the ~380 tokens the pointer reads. The background names people too, for what they
did before, which is the trap for a reader that sees only the start. Each note comes with the
matter a person might ask about, written in other words than the note's.

Both thresholds are set on the first ten notes and reported on the other ten. Then a router, a
table written in advance, sends short notes to the pointer alone and long ones to the finder
and pointer together, by a rule on their length. Importing office_note.py runs it first; the
pointer alone keeps the threshold it set there.

The background, the matters and all keys were written by hand for this example, before the
models saw them. Twenty notes show the method's shape. They are not a measurement.

Run from the repository root:  python3 examples/long_note.py
"""
import sys

sys.path.insert(0, "scaffold")
sys.path.insert(0, "examples")
from finder import Finder, narrowed, runs  # noqa: E402
from layers import route  # noqa: E402
from office_note import HELD_OUT, TUNE, pointer  # noqa: E402

BACKGROUND = [
    ["The TA bill for the October field visit to Gandhinagar was submitted without the sanction order attached.",
     "Under the current rules a claim has to reach accounts within sixty days of the journey, so the sanction period ends on 30 November.",
     "Last year Rakesh Patel handled the field-visit claims, and most of them came back once for missing bus tickets.",
     "The finance office has asked that every claim now carry the original tickets, not photocopies, along with the duty certificate.",
     "Claims for hired taxis need the vendor's GST invoice, which the travel desk can request again if it was lost.",
     "Daily allowance is paid at the rate in force on the date of travel, not on the date of the claim.",
     "Two claims from September are still pending because their duty certificates were signed by the wrong officer.",
     "The e-office module shows the status of each claim, though it is not yet updated every day."],
    ["The quarterly reconciliation shows a mismatch between the purchase register and GSTR-2A for three suppliers.",
     "Input tax credit cannot be claimed on invoices the supplier has not uploaded, so that amount is held back for now.",
     "In the last quarter Sunita Rao wrote to two of the same suppliers, and one of them filed the missing invoices within a week.",
     "The third supplier changed its GSTIN in August, which is why its invoices appear under a different number.",
     "The chartered accountant's office has said the difference is small but must be cleared before the annual return.",
     "A list of the invoices concerned, with their dates and amounts, is kept in the shared accounts folder.",
     "The portal allows corrections only until the return for the following month has been filed.",
     "Nothing has been paid twice, and the suppliers' accounts are otherwise up to date."],
    ["Seventeen students have applied for the state scholarship this year, up from eleven last year.",
     "Each application needs an income certificate issued by the Tehsildar's office and valid for the current financial year.",
     "Four of the certificates submitted were issued in the previous year and expired on 31 March, before the applications opened.",
     "When this happened in 2024, Deepak Joshi from the student section went with the students to the taluka office to explain the dates.",
     "The scholarship portal closes on 15 November and does not accept an application without a valid certificate.",
     "Students from outside the district may need a certificate from their home taluka, which usually takes longer.",
     "The portal's helpline has confirmed that a certificate applied for but not yet issued cannot be uploaded.",
     "The list of students, with the status of each certificate, is pinned up in the student section."],
    ["The fire safety audit in September found that two extinguishers on the third floor were past their refill date.",
     "It also noted that the emergency exit beside the library was blocked by furniture stacked there from the old reading area.",
     "After the previous audit Harish Kumar from estates had the extinguishers refilled within a week, and the inspector closed the point.",
     "The fire department expects a written reply to each point before its next visit, which is due in December.",
     "The furniture cannot be disposed of until the condemnation committee has met and approved the list.",
     "The audit report runs to nine pages and lists seven points in all, four of them minor.",
     "One copy of the report has been placed in the estates file and another sent to the registrar's office.",
     "The insurance renewal in January will ask whether the points have been closed."],
    ["The data for the annual survey has to be entered on the government portal by the end of the month.",
     "Most of the figures are already in the office's own registers, but the staff qualification details are out of date.",
     "Last year Neha Shah collected those details by sending a short form to every department, and nearly all of them replied within ten days.",
     "The portal saves a draft only when every field on a page has been filled, so the work cannot be done in pieces.",
     "Two departments have new staff whose appointment letters are still with the registrar.",
     "The figures entered this year will be compared with last year's, and large differences will be queried.",
     "The portal login was reset last week, and the new details are with the office superintendent.",
     "The deadline was extended twice last year, but there is no word of an extension this time."],
    ["The electricity bill for October is higher than usual because the meter on the hostel block was replaced in the middle of the month.",
     "The board has billed the old meter's last reading and the new meter's first reading as one month's use.",
     "When the same thing happened in 2023, Anil Mehta from estates took both readings to the sub-division office and the bill was revised.",
     "Payments over one lakh rupees now go through PFMS and need two approvals before they are released.",
     "The due date on the bill is 8 November, and late payment adds a surcharge of two per cent.",
     "The sub-division office takes complaints on weekday mornings only.",
     "Photographs of both meters, showing their readings, are in the estates file.",
     "The hostel's own sub-meter readings for the month are also available if they are needed."],
]

# What a person might ask about in each note, in their own words: the same order as office_note.py.
MATTERS_TUNE = ["checking the catering invoice", "the broken projector", "paying out the advance",
                "the leave application", "handing out visitor passes", "the tender returned by finance",
                "putting the new timings on the notice board", "the October vehicle log book",
                "signing the bills", "renewing the rent agreement"]
MATTERS_HELD_OUT = ["ink for the printer", "circulating the minutes", "a venue for the workshop",
                    "the leaking drinking-water machine", "sending fee receipts to the bank",
                    "the overdue payment to the vendor", "collecting forms from the hostels",
                    "replies to the audit queries", "buying stamp paper for the contract",
                    "updating the notice on the website"]
SIZE = 4  # sentences in each run the finder chooses between


def lengthen(cases, matters):
    """Background in front of each note and after it; the key moves with the sentence it names."""
    out = []
    for n, ((note, key), matter) in enumerate(zip(cases, matters)):
        a, b, c = BACKGROUND[n % 6], BACKGROUND[(n + 2) % 6], BACKGROUND[(n + 4) % 6]
        front = a + b + c[:3]
        out.append(((matter, front + note + c[3:]), None if key is None else len(front) + key))
    return out


LONG_TUNE, LONG_HELD_OUT = lengthen(TUNE, MATTERS_TUNE), lengthen(HELD_OUT, MATTERS_HELD_OUT)
tokens = lambda sentences: len(pointer.tok(" ".join(sentences)).input_ids)
past = sum(1 for (_, note), key in LONG_HELD_OUT if key is not None and tokens(note[:key]) > 380)
print(f"held-out long notes whose doer sits past the pointer's reach: {past} of 5")


def score(read, cases):
    """Doers found, and wrong yes: a sentence named that the key does not name, the failure that matters."""
    got = [(read(case, case[1]), key) for case, key in cases]
    return sum(1 for g, key in got if key is not None and g == key), sum(1 for g, key in got if g is not None and g != key)


# The pointer alone, at the threshold office_note.py set on the short notes.
short_threshold = pointer.threshold
found, wrong = score(pointer, LONG_HELD_OUT)
print(f"pointer alone on the long notes: {found} of 5 doers found, {wrong} wrong yes")

# Finder and pointer. The finder's threshold lets every tuning note through; the pointer's is set
# again, on the runs the finder chose, as the lowest with no wrong yes.
finder = Finder(lambda case: case[0], threshold=-1.0)
texts = lambda note: [" ".join(run) for _, run in runs(note, SIZE)]
finder.threshold = min(finder.similarity(case, texts(case[1]))[0] for case, _ in LONG_TUNE) - 0.01
read = narrowed(finder, pointer, SIZE)

margins = []
for case, _ in LONG_TUNE:
    margins.append(pointer.margin(runs(case[1], SIZE)[finder(case, texts(case[1]))][1])[0])
for threshold in [0.0] + sorted(margins):
    pointer.threshold = threshold
    if score(read, LONG_TUNE)[1] == 0:
        break
print(f"thresholds set on the first ten long notes: finder {finder.threshold:.2f}, pointer {threshold:.2f}")

chose = 0
for case, key in LONG_HELD_OUT:
    k = finder(case, texts(case[1]))
    if k is not None and key is not None:
        start, run = runs(case[1], SIZE)[k]
        chose += start <= key < start + len(run)
found, wrong = score(read, LONG_HELD_OUT)
print(f"finder and pointer on the long notes: the finder chose a run holding the doer in {chose} of 5, "
      f"{found} of 5 doers found, {wrong} wrong yes")


# The router: a table written in advance, and a rule on length that says which kind a note is.
def at(t, reader):
    def layer(case, choices):
        pointer.threshold = t
        return reader(case, choices)
    return layer


WORDS = {"named": "Sent on: the note names who will do it."}  # any other case goes to a person
TABLE = {
    "short": ([("who", at(short_threshold, pointer), lambda case: case[1])], lambda chosen: "named", WORDS),
    "long": ([("who", at(threshold, read), lambda case: case[1])], lambda chosen: "named", WORDS),
}


def kind(note):
    return "long" if tokens(note) > 380 else "short"


for (matter, note), key in [((m, n), k) for (n, k), m in zip(HELD_OUT, MATTERS_HELD_OUT)] + LONG_HELD_OUT:
    print(f"{kind(note):5}  {matter:40}  key {str(key):4} ->", route(TABLE, kind(note), (matter, note)))
