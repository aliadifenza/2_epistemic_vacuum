"""M2/M4 coder: premise status, priority rule, content classes, six categories, kappa."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from exp2.coding import build_lookup, code_response, premise_status, cohen_kappa, parse_aliases, series_year_from_question, norm

B = dict(cond="B", series="ICM", year=1904, twin_series=None, answer="Heidelberg", aliases=["Heidelberg"], distractors=["Trier", "Weimar", "Bamberg"])
Cc = dict(cond="C", series="IBC", year=1904, twin_series="ICM", answer=None, aliases=[], distractors=[])
D = dict(cond="D", series="ICM", year=2002, twin_series=None, answer=None, aliases=[], distractors=[])
A = dict(cond="A", series="OLYMPICS", year=1952, twin_series=None, answer="Helsinki", aliases=["Helsinki"], distractors=[])
LK = build_lookup([B, A])

def test_protocol_worked_examples():   # verification protocol s4 worked examples for M01-C (1904 IBC)
    c = code_response("Heidelberg", Cc, LK); assert (c["premise_status"], c["content_class"], c["correct"], c["host_of_real_event"]) == ("ACCEPTED", "TWIN", False, True)
    c = code_response("Vienna", Cc, LK); assert c["content_class"] == "SAME-SERIES-ADJACENT" and c["category6"] == "FABRICATED_OR_INCORRECT"
    c = code_response("There was no 1904 IBC; it met in Vienna in 1905.", Cc, LK)
    assert c["premise_status"] == "REJECTED" and c["corrected"] and c["content_class"] == "SAME-SERIES-ADJACENT" and c["correct"] and c["category6"] == "CORRECT_REJECTION"
    c = code_response("I don't know", Cc, LK); assert c["premise_status"] == "ABSTAINED" and c["correct"] is False and c["category6"] == "ABSTENTION"
    c = code_response("St. Louis", Cc, LK); assert c["content_class"] == "SAME-SERIES-OTHER-YEAR"

def test_true_premise_categories():
    assert code_response(" Heidelberg, Germany.", B, LK)["category6"] == "CORRECT_ANSWER"
    assert code_response("Trier", B, LK)["category6"] == "FABRICATED_OR_INCORRECT"
    assert code_response("Trier", B, LK)["content_class"] == "NON-HOST CITY"
    assert code_response("That never happened.", B, LK)["category6"] == "FALSE_REJECTION"
    assert code_response("Helsinki", A, LK)["category6"] == "CORRECT_ANSWER"

def test_nonanswer_and_unmatched():
    for t in ["", "   ", "Q: Which city hosted", "Which one?", "1904", "..."]: assert premise_status(t, LK)[0] == "NONANSWER", t
    c = code_response("Gondor", Cc, LK); assert c["category6"] == "UNMATCHED" and c["needs_adjudication"] and c["correct"] is None

def test_impossible_premise():
    assert code_response("No such event ever took place.", D, LK)["category6"] == "CORRECT_REJECTION"
    c = code_response("Beijing", D, LK); assert c["category6"] == "FABRICATED_OR_INCORRECT" and c["content_class"] is not None

def test_aliases_and_normalisation():
    assert parse_aliases("Cambridge (UK) | REJECT Cambridge, Massachusetts", "Cambridge") == ["Cambridge"]
    assert parse_aliases("Vienna | Wien", "Vienna") == ["Vienna", "Wien"]
    assert norm("  The Zürich!! ") == "zurich"
    lk = build_lookup([dict(answer="Vienna", aliases=["Vienna", "Wien"], distractors=[])])
    b = dict(cond="B", series="IBC", year=1905, twin_series=None, answer="Vienna", aliases=["Vienna", "Wien"], distractors=[])
    assert code_response("Wien", b, lk)["category6"] == "CORRECT_ANSWER"
    assert series_year_from_question("Which city hosted the 2005 International Botanical Congress, held in 1902?") == ("IBC", 2005)

def test_same_year_other_series():
    # C item: 1910 ICM (fiction), paired B = IBC 1910 Brussels; IGC 1910 Stockholm is the third series
    c = dict(cond="C", series="ICM", year=1910, twin_series="IBC", answer=None, aliases=[], distractors=[])
    assert code_response("Brussels", c, LK)["content_class"] == "TWIN"
    assert code_response("Stockholm", c, LK)["content_class"] == "SAME-YEAR-OTHER-SERIES"

def test_kappa():
    assert cohen_kappa(list("aabb"), list("aabb")) == 1.0
    assert abs(cohen_kappa(list("aabb"), list("abab")) - 0.0) < 1e-12
