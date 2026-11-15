"""Fill the replacement pairs' distractors and token diffs from validate.json into a NEW copy of the V1.2 candidate.
Usage: python3 apply_validate.py <V1.2 xlsx> validate.json <out xlsx> [--exclude R05 ...]
--exclude is for pairs the PI has decided to drop because fewer than three pool cities meet the rule; they are marked
EXCLUDED, never filled. All checks run first; on any failure nothing is written and the script exits 2.
Checks (Qualam 3.3): validate.json was produced from this exact dataset file (sha256); every included pair has a validation
record; every existing pair has a distractor record that passes; every retained replacement pair has three cities."""
import sys, json, os, openpyxl, hashlib
src, vj, dst = sys.argv[1:4]
EXCL = sys.argv[sys.argv.index("--exclude") + 1:] if "--exclude" in sys.argv else []
V = json.load(open(vj))
ANS_ALL = {"R02": "Kyoto", "R05": "Sydney", "R06": "Vienna", "R10": "Hyderabad"}
assert all(e in ANS_ALL for e in EXCL), f"--exclude accepts only {list(ANS_ALL)}"
ANS = {k: v for k, v in ANS_ALL.items() if k not in EXCL}
problems = []
src_sha = hashlib.sha256(open(src, "rb").read()).hexdigest()
if V.get("dataset_sha256") != src_sha:
    problems.append(f"validate.json was produced from dataset {V.get('dataset_sha256')}, not from {os.path.basename(src)} ({src_sha})")
wb = openpyxl.load_workbook(src); ws = wb["BC Paired Items"]; H = [c.value for c in ws[1]]; col = {h: i + 1 for i, h in enumerate(H)}
included = sorted({r[col["Pair ID"] - 1] for r in ws.iter_rows(min_row=2, values_only=True)
                   if r[0] and str(r[col["V1 status"] - 1]).startswith("INCLUDED") and r[col["Pair ID"] - 1] not in EXCL})
for pid in included:
    pv = V["pairs"].get(pid)
    if not pv: problems.append(f"{pid}: no validation record"); continue
    if not pv.get("token_pass"): problems.append(f"{pid}: question token diff {pv.get('diff')} outside +-2")
    if pid in ANS:
        nd = V.get("new_distractors", {}).get(ANS[pid])
        if not nd: problems.append(f"{pid} ({ANS[pid]}): no distractor-selection record")
        elif not nd["enough"]: problems.append(f"{pid} ({ANS[pid]}): only {len(nd['chosen'])}/3 pool cities satisfy equal tokens and +-1 nat")
    else:
        d = pv.get("distractors")
        if not d: problems.append(f"{pid}: no distractor record")
        elif not d["enough"]: problems.append(f"{pid}: existing distractors fail on this run")
if problems:
    print("PROBLEMS (nothing written):\n - " + "\n - ".join(problems)); sys.exit(2)
for row in ws.iter_rows(min_row=2):
    pid = row[col["Pair ID"] - 1].value
    if pid in EXCL:
        row[col["V1 status"] - 1].value = "EXCLUDED (PI decision 11: fewer than three pool cities meet equal tokens and +-1 nat)"
        row[col["V1 reason"] - 1].value = "Modal validate: no complete set of three distractors within the recorded region and name rules; dropped by PI decision 11"
        row[col["Row status"] - 1].value = "EXCLUDED after Qwen validation"
    elif pid in ANS:
        pv = V["pairs"][pid]; nd = V["new_distractors"][ANS[pid]]
        row[col["Qwen token diff"] - 1].value = f"B {pv['tokens_B']} / C {pv['tokens_C']} / diff {pv['diff']} - PASS (Modal validate)"
        row[col["V1 status"] - 1].value = "INCLUDED (Qwen-validated)"
        if row[col["Condition"] - 1].value == "B":
            for i, c in enumerate(nd["chosen"]): row[col[f"Distractor {i+1}"] - 1].value = c
            row[col["Prominence score verified"] - 1].value = "PASS (Modal validate, +-1 nat, equal tokens)"
            row[col["Row status"] - 1].value = "CANDIDATE - Qwen-validated (A2)"
assert os.path.abspath(dst) != os.path.abspath(src), "refusing to overwrite the input"
wb.save(dst)
print(("all pairs pass" if not EXCL else f"all remaining pairs pass; excluded {EXCL}") + "; written", dst, hashlib.sha256(open(dst, "rb").read()).hexdigest())
