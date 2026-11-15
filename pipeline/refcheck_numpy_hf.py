"""Compare the Modal/HF prominence scores in validate.json with the scores recorded in Dataset V0.7's 'Qwen Validation'
sheet (computed 14 Nov with the PI's custom numpy forward pass, 'answer_nats_ref' / 'distractor_nats_ref').
Usage: python3 refcheck_numpy_hf.py validate.json AlignedLab_Experiment_2_Dataset_V0_7.xlsx OUTDIR
Writes OUTDIR/refcheck_numpy_hf.csv (one row per city) and OUTDIR/refcheck_numpy_hf_summary.json.
Scope: neutral-prefix city scoring ("The city of" + city) only. It does not validate M1 entropy or generation."""
import sys, json, csv, os, hashlib, openpyxl
vj, xlsx, outdir = sys.argv[1:4]; os.makedirs(outdir, exist_ok=True)
V = json.load(open(vj))
ws = openpyxl.load_workbook(xlsx, read_only=True)["Qwen Validation"]; H = [c.value for c in next(ws.iter_rows(max_row=1))]
ref = {}
for r in ws.iter_rows(min_row=2, values_only=True):
    d = dict(zip(H, r))
    if d.get("item") and d.get("split") in ("main", "pilot"):
        ref[d["answer"]] = (d["answer_tokens"], d["answer_nats_ref"]); ref[d["distractor"]] = (d["distractor_tokens"], d["distractor_nats_ref"])
hf = {}
for pv in V["pairs"].values():
    d = pv.get("distractors")
    if d:
        hf[d["answer"]] = (d["answer_tokens"], d["answer_logp"])
        for t in d["table"]: hf[t["city"]] = (t["tokens"], t["logp"])
rows = [(c, hf[c][0], ref[c][0], hf[c][1], ref[c][1], hf[c][1] - ref[c][1]) for c in sorted(set(hf) & set(ref))]
with open(f"{outdir}/refcheck_numpy_hf.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["city", "tokens_hf", "tokens_numpy_ref", "logp_hf", "logp_numpy_ref", "diff_nats"]); w.writerows(rows)
summ = dict(n_cities=len(rows), max_abs_diff_nats=max(abs(r[5]) for r in rows), mean_abs_diff_nats=sum(abs(r[5]) for r in rows) / len(rows),
            token_mismatches=[r[0] for r in rows if r[1] != r[2]], validate_json_sha256=hashlib.sha256(open(vj, "rb").read()).hexdigest(),
            dataset_sha256=hashlib.sha256(open(xlsx, "rb").read()).hexdigest(),
            scope="neutral-prefix city prominence only ('The city of' + city); not M1 entropy, not generation",
            reference="Dataset V0.7 'Qwen Validation' sheet: custom numpy forward pass on the PI's Mac, 14 Nov 2026")
json.dump(summ, open(f"{outdir}/refcheck_numpy_hf_summary.json", "w"), indent=1)
print(json.dumps({k: summ[k] for k in ("n_cities", "max_abs_diff_nats", "token_mismatches")}))
