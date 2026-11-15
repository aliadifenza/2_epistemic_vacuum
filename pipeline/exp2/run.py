"""Integrated run: dataset -> M3a knownness -> M1 (3-shot, 0-shot) -> M3b -> question surprisal -> M4 greedy -> M2 samples
-> coding (M2/M4) -> analysis. Raw per-item results are written before any analysis; nothing is filtered.
Usage: python -m exp2.run --dataset X.xlsx --out DIR --stage {gate3,pilot,main,coldrun_main,coldrun_pilot} [--toy] [--limit N]
       [--skip-m2] [--expected-dataset-sha256 H] [--device cuda]"""
import argparse, json, os, time, hashlib, platform
import numpy as np, openpyxl
from . import config as C
from .stages import split_for
from .prompts import three_shot, zero_shot, knownness_prompt
from .measure import first_token_entropy, knownness_class, rejection_pref
from .coding import build_lookup, parse_aliases, series_year_from_question, code_response, m2_group
from .analysis import (paired_summary, bootstrap_ci, signflip_perm_test, two_sample, secondary_tests, group_entropy_bits,
                       nonanswer_bounds, inconclusive_conditions, pilot_feasibility, series_insensitive)

A_ALIASES = {"Rio de Janeiro": ["Rio"], "Turin": ["Torino"], "Munich": ["München"], "Mexico City": ["Ciudad de México"]}

def load_dataset(path, split):
    wb = openpyxl.load_workbook(path, data_only=True)
    bc = wb["BC Paired Items"]; H = [c.value for c in bc[1]]
    rows = [dict(zip(H, r)) for r in bc.iter_rows(min_row=2, values_only=True) if r[0]]
    inc = lambda r: str(r.get("V1 status", "INCLUDED")).startswith("INCLUDED")
    pairs = {}
    for r in rows:
        if r["Split"] != split or not inc(r): continue
        pairs.setdefault(r["Pair ID"], {})[r["Condition"]] = r
    pairs = {k: v for k, v in pairs.items() if "B" in v and "C" in v}
    ad = wb["A and D Items"]; HA = [c.value for c in ad[1]]
    items = [dict(zip(HA, r)) for r in ad.iter_rows(min_row=2, values_only=True) if r[0]]
    A = [r for r in items if r["Split"] == split and r["Condition"] == "A" and inc(r)]
    D = [r for r in items if r["Split"] == split and r["Condition"] == "D" and inc(r)]
    return pairs, A, D

def dataset_lookup(path, pools_path=None):
    """One coding lookup table per dataset file (all splits, all B rows, A answers) plus the distractor pools, so the table
    is identical for every stage and can be frozen with the dataset (verification protocol s4)."""
    recs = []
    for split in ("main", "pilot"):
        pairs, A, _ = load_dataset_all(path, split)
        for pr in pairs.values():
            if "B" in pr: recs.append(item_meta(pr["B"], "B"))
        recs += [item_meta(r, "A") for r in A]
    extra = json.load(open(pools_path)) if pools_path and os.path.exists(pools_path) else {}
    return build_lookup(recs, extra_cities=sorted({c for v in extra.values() for c in v}))

def load_dataset_all(path, split):
    """Like load_dataset but ignores V1 status (the lookup covers every answer and distractor in the file)."""
    wb = openpyxl.load_workbook(path, data_only=True)
    bc = wb["BC Paired Items"]; H = [c.value for c in bc[1]]
    pairs = {}
    for r in (dict(zip(H, x)) for x in bc.iter_rows(min_row=2, values_only=True) if x[0]):
        if r["Split"] == split: pairs.setdefault(r["Pair ID"], {})[r["Condition"]] = r
    ad = wb["A and D Items"]; HA = [c.value for c in ad[1]]
    A = [r for r in (dict(zip(HA, x)) for x in ad.iter_rows(min_row=2, values_only=True) if x[0]) if r["Split"] == split and r["Condition"] == "A"]
    return pairs, A, []

def item_meta(r, cond, pair=None, twin_series=None):
    if cond in ("B", "C"):
        series = r["True Series"] if cond == "B" else r["Counterfactual Series"]
        return dict(item=r["Item ID"], pair=pair, cond=cond, series=series, year=int(r["Year"]), twin_series=twin_series,
                    answer=r["Reference Answer"] if cond == "B" else None,
                    aliases=parse_aliases(r.get("Answer aliases"), r["Reference Answer"]) if cond == "B" else [],
                    distractors=[r.get("Distractor 1"), r.get("Distractor 2"), r.get("Distractor 3")] if cond == "B" else [])
    if cond == "D":
        s, y = series_year_from_question(r["Question"])
        return dict(item=r["Item ID"], pair=None, cond="D", series=s, year=y, twin_series=None, answer=None, aliases=[], distractors=[])
    return dict(item=r["Item ID"], pair=None, cond="A", series="OLYMPICS", year=int(r["Year"]) if r.get("Year") else None, twin_series=None,
                answer=r["Reference Answer"], aliases=[r["Reference Answer"]] + A_ALIASES.get(r["Reference Answer"], []), distractors=[])

def integrity_checks(meta, records, pairs, be, expected_sha, toy):
    fails = []
    if expected_sha and meta["dataset_sha256"] != expected_sha: fails.append("dataset sha256 differs from the expected (manifest) hash")
    if not toy and be.commit_hash != C.MODEL_REVISION: fails.append(f"model commit {be.commit_hash} != pinned {C.MODEL_REVISION}")
    if be.lm_head_rows < be.vocab_size: fails.append("LM head smaller than tokenizer vocabulary")
    for pid, pr in pairs.items():
        if any(str(pr["B"].get(f"Distractor {i}")).startswith(("PENDING", "None")) for i in (1, 2, 3)):
            fails.append(f"{pid}: distractor not validated (PENDING)")
    num_keys = ("H3", "pmax3", "H0", "pmax0", "d_R1S1", "d_R2S2", "surprisal_q")
    for r in records:
        if not all(np.isfinite(r[k]) for k in num_keys): fails.append(f"{r['item']}: non-finite measurement")
        if not meta["skip_m2"] and len(r.get("m2", [])) != C.M2_SAMPLES: fails.append(f"{r['item']}: {len(r.get('m2', []))} M2 samples")
        for g in [r["greedy3"], r["greedy0"]] + r.get("m2", []):
            if g["max_new_id"] is not None and g["max_new_id"] >= be.vocab_size: fails.append(f"{r['item']}: generated a padded-vocabulary token")
    return fails

def main(argv=None, backend=None):
    """backend: an already-loaded model (Modal passes the one used for the Gate 3 checks, so only one copy is ever resident)."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True); ap.add_argument("--out", required=True); ap.add_argument("--stage", required=True)
    ap.add_argument("--toy", action="store_true"); ap.add_argument("--limit", type=int, default=0); ap.add_argument("--device", default="cpu")
    ap.add_argument("--skip-m2", action="store_true"); ap.add_argument("--expected-dataset-sha256", default=None)
    ap.add_argument("--pools", default=None)
    a = ap.parse_args(argv); split = split_for(a.stage)
    from .stages import MEASUREMENT_STAGES
    if a.stage not in MEASUREMENT_STAGES: raise ValueError(f"stage {a.stage!r} takes no measurements; exp2.run accepts {MEASUREMENT_STAGES}")
    os.makedirs(a.out, exist_ok=True)
    import torch, transformers
    from .backend_hf import HFBackend, toy_backend
    be = backend if backend is not None else (toy_backend() if a.toy else HFBackend.load(C.MODEL_ID, C.MODEL_REVISION, a.device))
    pairs, A, D = load_dataset(a.dataset, split)
    if a.limit: pairs = dict(list(pairs.items())[:a.limit]); A = A[:a.limit]; D = D[:a.limit]
    items = []
    for pid, pr in pairs.items():
        items.append(item_meta(pr["B"], "B", pid)); items.append(item_meta(pr["C"], "C", pid, twin_series=pr["B"]["True Series"]))
    items += [item_meta(r, "A") for r in A] + [item_meta(r, "D") for r in D]
    lookup = dataset_lookup(a.dataset, a.pools)
    json.dump(json.loads(lookup.to_json()), open(f"{a.out}/coding_lookup.json", "w"), indent=1, ensure_ascii=False)
    meta = dict(stage=a.stage, split=split, limit=a.limit, skip_m2=a.skip_m2, toy=a.toy,
                model=("TOY-RANDOM-WEIGHTS" if a.toy else f"{C.MODEL_ID}@{C.MODEL_REVISION}"), model_commit_hash=be.commit_hash,
                dataset=os.path.basename(a.dataset), dataset_sha256=hashlib.sha256(open(a.dataset, "rb").read()).hexdigest(),
                coding_lookup_sha256=lookup.sha256(), torch=torch.__version__, transformers=transformers.__version__, numpy=np.__version__,
                python=platform.python_version(), device=a.device, dtype=C.DTYPE, demos=C.DEMOS,
                tokenizer_vocab=be.vocab_size, lm_head_rows=be.lm_head_rows,
                checkpoint_generation_config=be.checkpoint_generation_config, effective_generation=be.effective_generation,
                seeds=dict(bootstrap=C.BOOTSTRAP_SEED, perm=C.PERM_SEED, m2_rule=C.SEED_RULE),
                started=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    records, known = [], {}
    by_pid = {pid: pr for pid, pr in pairs.items()}
    for it in items:
        src = (by_pid[it["pair"]][it["cond"]] if it["cond"] in ("B", "C") else next(r for r in (A if it["cond"] == "A" else D) if r["Item ID"] == it["item"]))
        q = src["Question"]; p3, p0 = three_shot(q), zero_shot(q)
        assert p3.endswith("A:") and not p3.endswith(" "), "prompt must end immediately after A:"
        if it["cond"] == "B":
            cls, forms = knownness_class(be, knownness_prompt(src["Knownness paraphrase 1"]), knownness_prompt(src["Knownness paraphrase 2"]),
                                         src["Reference Answer"], it["distractors"])
            known[it["pair"]] = dict(cls=cls, formulations=forms, any_tie=any(f["tie_at_top"] for f in forms))
        H3, pm3 = first_token_entropy(be, p3); H0, pm0 = first_token_entropy(be, p0)
        qs = p3.rindex("Q: " + q) + 3
        sur, n_qtok = be.question_surprisal(p3, qs, qs + len(q))
        g3, g0 = be.greedy(p3), be.greedy(p0)
        r = dict(it, question=q, H3=H3, pmax3=pm3, H0=H0, pmax0=pm0,
                 d_R1S1=rejection_pref(be, p3, C.REJECT_R1, C.ACCEPT_S1), d_R2S2=rejection_pref(be, p3, C.REJECT_R2, C.ACCEPT_S2),
                 surprisal_q=sur, n_question_tokens=n_qtok, greedy3=g3, greedy0=g0,
                 code3=code_response(g3["text"], it, lookup), code0=code_response(g0["text"], it, lookup))
        if not a.skip_m2:
            r["m2"] = [be.sample(p3, C.m2_seed(it["item"], k)) for k in range(C.M2_SAMPLES)]
            groups = {}
            for s in r["m2"]:
                g = m2_group(code_response(s["text"], it, lookup), s["text"]); s["group"] = g; groups[g] = groups.get(g, 0) + 1
            r["m2_groups"] = groups; r["m2_entropy_bits"] = group_entropy_bits(groups)
        records.append(r)
    fails = integrity_checks(meta, records, pairs, be, a.expected_dataset_sha256, a.toy)
    meta["integrity_failures"] = fails; meta["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    json.dump(meta, open(f"{a.out}/run_meta.json", "w"), indent=1, default=str)
    json.dump(dict(knownness=known, records=records), open(f"{a.out}/raw_results.json", "w"), indent=1, default=float)
    out = analyse(records, known, split, fails)
    json.dump(out, open(f"{a.out}/analysis.json", "w"), indent=1, default=float)
    print(json.dumps({k: out[k] for k in ("n_pairs", "n_unknown", "P1_primary_unknown_3shot", "inconclusive_conditions")}, indent=1, default=float))
    return out

def analyse(records, known, split, integrity_failures):
    by = {(r["pair"], r["cond"]): r for r in records if r["pair"]}
    allp = sorted({r["pair"] for r in records if r["pair"]})
    unk = [p for p in allp if known[p]["cls"] == "Unknown"]; kn = [p for p in allp if known[p]["cls"] == "Known"]
    d = lambda key, sub: np.array([by[(p, "C")][key] - by[(p, "B")][key] for p in sub])
    def block(x):
        if len(x) == 0: return dict(n=0)
        s = paired_summary(x); s["ci95"] = bootstrap_ci(x); s["perm"] = signflip_perm_test(x); return s
    out = dict(n_pairs=len(allp), n_unknown=len(unk), n_known=len(kn), n_uncertain=len(allp) - len(unk) - len(kn),
               knownness_ties=[p for p in allp if known[p]["any_tie"]])
    out["P1_primary_unknown_3shot"] = block(d("H3", unk))
    out["P1_all_pairs_3shot"] = block(d("H3", allp))
    out["known_pairs_3shot"] = block(d("H3", kn))
    out["sens_unknown_0shot"] = block(d("H0", unk)); out["sens_all_0shot"] = block(d("H0", allp))
    istb = [p for p in unk if p not in ("M02", "M13", "M31")]
    out["supp_istanbul_excl_unknown_3shot"] = dict(block(d("H3", istb)), n_istanbul_in_unknown=len(unk) - len(istb))
    H = lambda cond, key="H3": [r[key] for r in records if r["cond"] == cond]
    out["P2_C_vs_A"] = two_sample(H("C"), H("A")) if H("A") and H("C") else {}
    out["P3_R1S1_all_pairs"] = block(d("d_R1S1", allp))                      # secondary test (two-sided; prediction: positive)
    out["P3_R2S2_all_pairs_robustness"] = block(d("d_R2S2", allp))
    out["P3_R1S1_unknown_descriptive"] = block(d("d_R1S1", unk))
    out["holm_secondary"] = secondary_tests(out["P2_C_vs_A"], out["P3_R1S1_all_pairs"])
    out["surprisal"] = dict({c: dict(n=len(H(c, "surprisal_q")), mean=float(np.mean(H(c, "surprisal_q"))) if H(c, "surprisal_q") else None,
                                     median=float(np.median(H(c, "surprisal_q"))) if H(c, "surprisal_q") else None) for c in ("A", "B", "C", "D")},
                            paired_C_minus_B_all=paired_summary(d("surprisal_q", allp)) if allp else None)
    cat = lambda cond, f="code3": {k: sum(r[f]["category6"] == k for r in records if r["cond"] == cond) for k in
                                   ("CORRECT_ANSWER", "CORRECT_REJECTION", "FALSE_REJECTION", "ABSTENTION", "FABRICATED_OR_INCORRECT", "NONANSWER", "UNMATCHED")}
    out["M4_categories"] = {f: {c: cat(c, f) for c in ("A", "B", "C", "D")} for f in ("code3", "code0")}
    out["M4_pending_adjudication"] = sorted({r["item"] + ":" + f for r in records for f in ("code3", "code0") if r[f]["needs_adjudication"]})
    out["D_vs_C_descriptive"] = dict(medianH_D=float(np.median(H("D"))) if H("D") else None, medianH_C=float(np.median(H("C"))) if H("C") else None,
                                     M4_D=cat("D"), M4_C=cat("C"))
    if any("m2_entropy_bits" in r for r in records):
        out["M2_descriptive"] = {c: dict(median_bits=float(np.median([r["m2_entropy_bits"] for r in records if r["cond"] == c])))
                                 for c in ("A", "B", "C", "D") if any(r["cond"] == c for r in records)}
    na_B = nonanswer_bounds([by[(p, "B")]["code3"] for p in allp]); na_C = nonanswer_bounds([by[(p, "C")]["code3"] for p in allp])
    medA = float(np.median(H("A"))) if H("A") else float("nan")
    medBunk = float(np.median([by[(p, "B")]["H3"] for p in unk])) if unk else float("nan")
    clear = lambda b: b.get("n", 0) and not (b["ci95"][0] <= 0 <= b["ci95"][1])
    oppose = bool(clear(out["P1_primary_unknown_3shot"]) and clear(out["sens_unknown_0shot"]) and
                  np.sign(out["P1_primary_unknown_3shot"]["mean"]) != np.sign(out["sens_unknown_0shot"]["mean"]))
    out["inconclusive_conditions"] = inconclusive_conditions(len(unk), medA, medBunk, na_B, na_C, oppose, integrity_failures)
    out["series_insensitive"] = dict(three_shot=series_insensitive([by[(p, "C")]["code3"] for p in unk]),
                                     no_demo=series_insensitive([by[(p, "C")]["code0"] for p in unk]))
    if split == "pilot":
        out["pilot_feasibility"] = pilot_feasibility([r["code3"] for r in records if r["cond"] == "A"], H("A", "pmax3"))
    return out

if __name__ == "__main__": main()
