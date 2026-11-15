"""apply_validate (Qualam 3.3), refcheck_numpy_hf (4.4) and the second-rater round trip (M4)."""
import subprocess, sys, os, json, hashlib, csv, tempfile, shutil
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from _paths import V12, V07, VAL
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()

def _synthetic_validate(tmp, dataset_sha, drop_pair=None, short=None):
    import openpyxl
    ws = openpyxl.load_workbook(V12, read_only=True)["BC Paired Items"]; H = [c.value for c in next(ws.iter_rows(max_row=1))]
    inc = sorted({dict(zip(H, r))["Pair ID"] for r in ws.iter_rows(min_row=2, values_only=True) if r[0] and str(dict(zip(H, r))["V1 status"]).startswith("INCLUDED")})
    pairs = {p: dict(tokens_B=15, tokens_C=14, diff=-1, token_pass=True, **({} if p.startswith("R") else dict(distractors=dict(enough=True)))) for p in inc if p != drop_pair}
    nd = {a: dict(chosen=["X", "Y", "Z"], enough=True) for a in ("Kyoto", "Sydney", "Vienna", "Hyderabad")}
    if short: nd[short] = dict(chosen=["X"], enough=False)
    p = os.path.join(tmp, "v.json"); json.dump(dict(dataset_sha256=dataset_sha, pairs=pairs, new_distractors=nd), open(p, "w")); return p

def _run(*args):
    return subprocess.run([sys.executable, os.path.join(HERE, "apply_validate.py"), *args], capture_output=True, text=True)

def test_apply_validate_checks():
    tmp = tempfile.mkdtemp()
    try:
        ok = _synthetic_validate(tmp, sha(V12)); out = os.path.join(tmp, "o.xlsx")
        r = _run(V12, ok, out); assert r.returncode == 0 and os.path.exists(out), r.stdout
        os.remove(out)
        r = _run(V12, _synthetic_validate(tmp, "0" * 64), out); assert r.returncode == 2 and "produced from dataset" in r.stdout and not os.path.exists(out)
        r = _run(V12, _synthetic_validate(tmp, sha(V12), drop_pair="M07"), out); assert r.returncode == 2 and "M07: no validation record" in r.stdout
        r = _run(V12, _synthetic_validate(tmp, sha(V12), short="Sydney"), out); assert r.returncode == 2 and "R05" in r.stdout
        r = _run(V12, _synthetic_validate(tmp, sha(V12), short="Sydney"), out, "--exclude", "R05"); assert r.returncode == 0
        import openpyxl
        ws = openpyxl.load_workbook(out)["BC Paired Items"]; H = [c.value for c in ws[1]]
        st = {(d["Pair ID"], d["Condition"]): d for r in ws.iter_rows(min_row=2, values_only=True) if r[0] for d in [dict(zip(H, r))]}
        assert st[("R05", "B")]["V1 status"].startswith("EXCLUDED") and "fewer than three" in st[("R05", "B")]["V1 status"]
        assert st[("R06", "B")]["Distractor 1"] == "X" and st[("R06", "B")]["V1 status"] == "INCLUDED (Qwen-validated)"
    finally:
        shutil.rmtree(tmp)

def test_refcheck_reproduces_logged_comparison():
    tmp = tempfile.mkdtemp()
    try:
        r = subprocess.run([sys.executable, os.path.join(HERE, "refcheck_numpy_hf.py"), VAL, V07, tmp], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        s = json.load(open(os.path.join(tmp, "refcheck_numpy_hf_summary.json")))
        assert s["n_cities"] >= 60 and s["max_abs_diff_nats"] < 0.001 and s["token_mismatches"] == []
    finally:
        shutil.rmtree(tmp)

def test_second_rater_round_trip():
    tmp = tempfile.mkdtemp()
    try:
        raw = os.path.join(tmp, "raw.json")
        rec = lambda item, cond, g3, g0, c3, c0: dict(item=item, cond=cond, question="Q?", series="ICM", year=1904, twin_series=None, aliases=["Heidelberg"],
                                                       greedy3=dict(text=g3), greedy0=dict(text=g0), code3=c3, code0=c0)
        code = lambda s, cl, c, adj=False: dict(premise_status=s, content_class=cl, category6=c, needs_adjudication=adj)
        json.dump(dict(records=[rec("M01-B", "B", "Heidelberg", "Trier", code("ACCEPTED", None, "CORRECT_ANSWER"), code("ACCEPTED", "NON-HOST CITY", "FABRICATED_OR_INCORRECT")),
                                rec("M01-C", "C", "Gondor", "No.", code("UNMATCHED", None, "UNMATCHED", True), code("REJECTED", None, "CORRECT_REJECTION"))]), open(raw, "w"))
        subprocess.run([sys.executable, os.path.join(HERE, "second_rater.py"), "export", raw, tmp], check=True, capture_output=True)
        items = list(csv.DictReader(open(os.path.join(tmp, "second_rater_items.csv"))))
        assert len(items) == 4 and "coderA" not in items[0] and "category6" not in items[0]
        key = json.load(open(os.path.join(tmp, "key.json")))["key"]
        lab = os.path.join(tmp, "gemini.csv")
        with open(lab, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["row_id", "premise_status", "content_class", "category6", "note"])
            for rid, v in key.items():   # rater agrees except on M01-B no-demo
                if (v["item"], v["format"]) == ("M01-B", "no-demo"): w.writerow([rid, "ACCEPTED", "NON-HOST CITY", "CORRECT_ANSWER", ""])
                elif v["item"] == "M01-B": w.writerow([rid, "ACCEPTED", "", "CORRECT_ANSWER", ""])
                elif v["format"] == "three-shot": w.writerow([rid, "UNMATCHED", "", "UNMATCHED", ""])
                else: w.writerow([rid, "REJECTED", "", "CORRECT_REJECTION", ""])
        subprocess.run([sys.executable, os.path.join(HERE, "second_rater.py"), "import", raw, tmp, lab], check=True, capture_output=True)
        ag = json.load(open(os.path.join(tmp, "agreement.json")))["agreement"]
        assert ag["premise_status"]["raw_agreement"] == 1.0 and ag["category6"]["raw_agreement"] == 0.75
        adj = list(csv.DictReader(open(os.path.join(tmp, "pi_adjudication.csv"))))
        assert {a["item"] for a in adj} == {"M01-B", "M01-C"} and any("UNMATCHED" in a["reason"] for a in adj)
    finally:
        shutil.rmtree(tmp)
