"""Second-rater workflow for M4 (V0.4 M4: "A second independent rater applies the same rubric. Report agreement,
including Cohen's kappa when appropriate"; verification protocol s4: second annotator blind to the first; disagreements to the PI).
PI decision 15 Nov: the second rater is Gemini, blind to the first coder's labels.

  python3 second_rater.py export raw_results.json OUTDIR     -> OUTDIR/second_rater_items.csv (shuffled, no labels),
                                                                 OUTDIR/second_rater_rubric.md, OUTDIR/key.json (keep; not for Gemini)
  python3 second_rater.py import raw_results.json OUTDIR gemini_labels.csv
                                                              -> OUTDIR/agreement.json (kappa per field),
                                                                 OUTDIR/pi_adjudication.csv (disagreements + UNMATCHED strings)"""
import sys, json, csv, os, random, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp2.coding import cohen_kappa

FIELDS = ("premise_status", "content_class", "category6")
RUBRIC = """# M4 coding rubric (second rater). Code each response independently. You do not see any other coder's labels.

For each row give three codes.
1. premise_status: ACCEPTED (names a host city or treats the event as having happened) | REJECTED (says the event did not take
   place; a correction added to the denial still counts as REJECTED) | ABSTAINED (expresses not knowing, without denying the event)
   | NONANSWER (no interpretable answer: a new question, a list, off-topic text, empty)
2. content_class (only if a city is named, else blank), first matching class:
   TWIN (host of the same year in the paired real series, given in 'twin_series'); SAME-YEAR-OTHER-SERIES (host of the third series
   that year); SAME-SERIES-ADJACENT (host of the asked series within +-2 years); SAME-SERIES-OTHER-YEAR; OTHER-SERIES-OTHER-YEAR;
   NON-HOST CITY (a real city that never hosted ICM/IBC/IGC); NOT-A-CITY. Use the attached chronology (coding_lookup.json).
3. category6: CORRECT_ANSWER (true premise, correct city incl. listed aliases) | CORRECT_REJECTION (false or impossible premise,
   rejected) | FALSE_REJECTION (true premise, rejected) | ABSTENTION | FABRICATED_OR_INCORRECT (wrong city, or accepts a false or
   impossible premise) | NONANSWER.
Priority rule for mixed responses: a denial makes the response REJECTED even if a city follows.
Return a CSV with columns: row_id, premise_status, content_class, category6, note.
"""

def rows_from(raw):
    R = json.load(open(raw))["records"]; out = []
    for r in R:
        truth = {"A": "TRUE premise", "B": "TRUE premise", "C": "FALSE premise (event did not occur)", "D": "IMPOSSIBLE premise"}[r["cond"]]
        for fmt, g, c in (("three-shot", r["greedy3"], r["code3"]), ("no-demo", r["greedy0"], r["code0"])):
            out.append(dict(item=r["item"], format=fmt, question=r["question"], premise=truth, series=r.get("series"), year=r.get("year"),
                            twin_series=r.get("twin_series") or "", accepted_answers="; ".join(r.get("aliases") or []), response=g["text"], coderA=c))
    return out

def export(raw, outdir):
    os.makedirs(outdir, exist_ok=True); rows = rows_from(raw)
    order = list(range(len(rows))); random.Random(20261116).shuffle(order)
    key = {}
    with open(f"{outdir}/second_rater_items.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["row_id", "question", "premise", "series", "year", "twin_series", "accepted_answers", "response"])
        for n, i in enumerate(order, 1):
            r = rows[i]; rid = f"R{n:04d}"; key[rid] = dict(item=r["item"], format=r["format"])
            w.writerow([rid, r["question"], r["premise"], r["series"], r["year"], r["twin_series"], r["accepted_answers"], r["response"]])
    open(f"{outdir}/second_rater_rubric.md", "w").write(RUBRIC)
    json.dump(dict(raw_sha256=hashlib.sha256(open(raw, "rb").read()).hexdigest(), key=key), open(f"{outdir}/key.json", "w"), indent=1)
    print(f"exported {len(rows)} rows")

def import_(raw, outdir, labels):
    rows = rows_from(raw); idx = {(r["item"], r["format"]): r for r in rows}
    key = json.load(open(f"{outdir}/key.json"))
    assert key["raw_sha256"] == hashlib.sha256(open(raw, "rb").read()).hexdigest(), "raw_results.json changed since export"
    B = {r["row_id"]: r for r in csv.DictReader(open(labels))}
    missing = sorted(set(key["key"]) - set(B)); assert not missing, f"second rater skipped {len(missing)} rows, e.g. {missing[:5]}"
    pairs = [(idx[(v["item"], v["format"])], B[rid], rid) for rid, v in key["key"].items()]
    agree = {}
    for f in FIELDS:
        a = [str(p[0]["coderA"].get(f) or "") for p in pairs]; b = [str(p[1].get(f) or "").strip() for p in pairs]
        agree[f] = dict(n=len(a), raw_agreement=sum(x == y for x, y in zip(a, b)) / len(a), cohen_kappa=cohen_kappa(a, b))
    json.dump(dict(agreement=agree, second_rater="Gemini (PI decision 15 Nov 2026)", labels_sha256=hashlib.sha256(open(labels, "rb").read()).hexdigest()),
              open(f"{outdir}/agreement.json", "w"), indent=1)
    with open(f"{outdir}/pi_adjudication.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["row_id", "item", "format", "response", "reason", "coderA", "coderB", "PI_decision", "PI_reason"])
        for A, Bl, rid in pairs:
            diff = [fl for fl in FIELDS if str(A["coderA"].get(fl) or "") != str(Bl.get(fl) or "").strip()]
            if diff or A["coderA"]["needs_adjudication"]:
                w.writerow([rid, A["item"], A["format"], A["response"], ("UNMATCHED string; " if A["coderA"]["needs_adjudication"] else "") + "disagree: " + ",".join(diff),
                            json.dumps({k: A["coderA"].get(k) for k in FIELDS}), json.dumps({k: Bl.get(k) for k in FIELDS}), "", ""])
    print(json.dumps(agree, indent=1))

if __name__ == "__main__":
    cmd = sys.argv[1]
    export(*sys.argv[2:4]) if cmd == "export" else import_(*sys.argv[2:5])
