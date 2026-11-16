"""AlignedLab Experiment 2 — Gate 7 analysis package (16 Nov 2026).

Reproducible from the frozen Gate 6 outputs only. The model is NOT rerun and the frozen statistical procedures are NOT
changed: every statistic is computed by calling the frozen functions in pipeline/exp2/analysis.py and the frozen
analyse() in pipeline/exp2/run.py, and is checked against evidence/main_2026-11-16/analysis.json.

Run from the repository root (exp2_pilot/):   python3 analysis/gate7/gate7_analysis.py
Writes to evidence/main_2026-11-16/gate7/ : tables (CSV), gate7_stats.json, figures (PNG), SHA256SUMS.

Labels used in every output: PRE-REGISTERED (V0.4 s6-7), DESCRIPTIVE (V0.4, no confirmatory claim),
EXPLORATORY-POSTHOC (not in V0.4; chosen after seeing the data; no confirmatory weight), REPRODUCIBILITY (checks of the
computation itself, not new analyses)."""
import csv, hashlib, json, os, sys, platform
import numpy as np

ROOT = os.getcwd()
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from exp2 import config as C                                   # frozen
from exp2.analysis import paired_summary, bootstrap_ci, signflip_perm_test, two_sample, holm   # frozen
from exp2.run import analyse                                    # frozen

EV = os.path.join(ROOT, "evidence/main_2026-11-16")
OUT = os.path.join(EV, "gate7"); os.makedirs(OUT, exist_ok=True)
raw = json.load(open(f"{EV}/raw_results.json")); R, K = raw["records"], raw["knownness"]
frozen = json.load(open(f"{EV}/analysis.json")); meta = json.load(open(f"{EV}/run_meta.json"))

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
EXPECTED = {"raw_results.json": "5885afb2ae6d410d8f03b7436aee9996209b3dfefe856fa9b08f4cdda5b0b759",
            "analysis.json": "92e725b0cc186a01b75237b2388b73988418b3f3d8ee86ce06e648730ac799f0",
            "run_meta.json": "3d1fa74c7319e62ab8386e968d5801de41eae994dfd06d07cddd90e3891d986c"}
inputs = {k: sha(f"{EV}/{k}") for k in EXPECTED}
assert inputs == EXPECTED, f"frozen Gate 6 inputs changed: {inputs}"

def wcsv(name, rows, header):
    with open(f"{OUT}/{name}", "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

def close(a, b, tol=1e-9):
    if isinstance(a, dict): return all(close(a[k], b.get(k), tol) for k in a)
    if isinstance(a, (list, tuple)): return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, float) or isinstance(b, float): return a is not None and b is not None and abs(a - b) <= tol
    return a == b

stats = dict(gate="7", inputs_sha256=inputs, environment=dict(python=platform.python_version(), numpy=np.__version__,
             frozen_run_numpy=meta["numpy"]), labels={})

# ---------------- 1. Reproduce the frozen analysis exactly (REPRODUCIBILITY) ----------------
re = json.loads(json.dumps(analyse(R, K, "main", meta["integrity_failures"]), default=float))
stats["frozen_analysis_reproduced_exactly"] = close(re, frozen)
assert stats["frozen_analysis_reproduced_exactly"], "frozen analyse() does not reproduce analysis.json"

# ---------------- 2. P1-P3 against V0.4, recomputed block by block with the frozen functions ----------------
by = {(r["pair"], r["cond"]): r for r in R if r["pair"]}
pairs = sorted({r["pair"] for r in R if r["pair"]})
cls = {p: K[p]["cls"] for p in pairs}
unk = [p for p in pairs if cls[p] == "Unknown"]; kn = [p for p in pairs if cls[p] == "Known"]
D = lambda key, sub: np.array([by[(p, "C")][key] - by[(p, "B")][key] for p in sub])
def block(x):
    s = paired_summary(x); s["ci95"] = list(bootstrap_ci(x)); s["perm"] = signflip_perm_test(x); return s
spec = [  # (name, label, key, subset, frozen key, V0.4 reference)
 ("P1_primary_unknown_3shot", "PRE-REGISTERED primary", "H3", unk, "P1_primary_unknown_3shot", "s6 P1, s7.1"),
 ("P1_all_pairs_3shot", "PRE-REGISTERED descriptive (all pairs reported)", "H3", pairs, "P1_all_pairs_3shot", "s6 P1"),
 ("known_pairs_3shot", "PRE-REGISTERED sensitivity (P2 matched check)", "H3", kn, "known_pairs_3shot", "s6 P2"),
 ("sens_unknown_0shot", "PRE-REGISTERED sensitivity (no-demo format)", "H0", unk, "sens_unknown_0shot", "s2.5, s7.2"),
 ("sens_all_0shot", "PRE-REGISTERED sensitivity (no-demo format)", "H0", pairs, "sens_all_0shot", "s2.5, s7.2"),
 ("P3_R1S1_all_pairs", "PRE-REGISTERED secondary test", "d_R1S1", pairs, "P3_R1S1_all_pairs", "s6 P3, s7.2"),
 ("P3_R2S2_all_pairs_robustness", "PRE-REGISTERED robustness template", "d_R2S2", pairs, "P3_R2S2_all_pairs_robustness", "s4 M3b"),
 ("P3_R1S1_unknown_descriptive", "DESCRIPTIVE", "d_R1S1", unk, "P3_R1S1_unknown_descriptive", "s4 M3b"),
]
tests, rows = {}, []
for name, lab, key, sub, fk, ref in spec:
    b = block(D(key, sub)); ok = close(b, {k: frozen[fk][k] for k in b}); tests[name] = dict(b, label=lab, v04=ref, matches_frozen=ok)
    rows.append([name, lab, ref, b["n"], f"{b['mean']:.4f}", f"{b['median']:.4f}", f"{b['prop_positive']:.3f}",
                 f"{b['ci95'][0]:.4f}", f"{b['ci95'][1]:.4f}", f"{b['perm']['p']:.4f}", b["perm"]["method"], b["perm"]["n_perm"], ok])
HC = [r["H3"] for r in R if r["cond"] == "C"]; HA = [r["H3"] for r in R if r["cond"] == "A"]
p2 = two_sample(HC, HA); p2["ci"] = list(p2["ci"]); ok2 = close(p2, frozen["P2_C_vs_A"])
tests["P2_C_vs_A"] = dict(p2, label="PRE-REGISTERED secondary test", v04="s6 P2, s7.2", matches_frozen=ok2)
rows.append(["P2_C_vs_A (mean H(C) - mean H(A))", "PRE-REGISTERED secondary test", "s6 P2, s7.2", f"{len(HC)}+{len(HA)}",
             f"{p2['diff']:.4f}", "", "", f"{p2['ci'][0]:.4f}", f"{p2['ci'][1]:.4f}", f"{p2['p']:.6f}", "label permutation", p2["n_perm"], ok2])
adj = holm([p2["p"], tests["P3_R1S1_all_pairs"]["perm"]["p"]])
tests["holm_secondary"] = dict(P2_raw=p2["p"], P3_raw=tests["P3_R1S1_all_pairs"]["perm"]["p"], P2_adj=adj[0], P3_adj=adj[1],
                               matches_frozen=close([adj[0], adj[1]], [frozen["holm_secondary"]["adjusted"]["P2"], frozen["holm_secondary"]["adjusted"]["P3"]]))
istb = [p for p in unk if p not in ("M02", "M13", "M31")]
bi = block(D("H3", istb)); tests["supp_istanbul_excl_unknown_3shot"] = dict(bi, n_istanbul_in_unknown=len(unk) - len(istb),
    label="PRE-REGISTERED supplementary (verification protocol, 14 Nov)", matches_frozen=close(bi, {k: frozen["supp_istanbul_excl_unknown_3shot"][k] for k in bi}))
rows.append(["supp_istanbul_excl_unknown_3shot", "PRE-REGISTERED supplementary", "consistency record #4", bi["n"], f"{bi['mean']:.4f}",
             f"{bi['median']:.4f}", f"{bi['prop_positive']:.3f}", f"{bi['ci95'][0]:.4f}", f"{bi['ci95'][1]:.4f}", f"{bi['perm']['p']:.4f}",
             bi["perm"]["method"], bi["perm"]["n_perm"], tests["supp_istanbul_excl_unknown_3shot"]["matches_frozen"]])
stats["tests"] = tests
wcsv("T1_tests.csv", rows, ["analysis", "status", "V0.4 ref", "n", "mean", "median", "prop_positive", "ci95_lo", "ci95_hi", "p", "test", "n_perm", "matches_frozen_analysis_json"])
stats["protocol_settings_used"] = dict(bootstrap_resamples=C.BOOTSTRAP_N, bootstrap_seed=C.BOOTSTRAP_SEED, signflip_exact_up_to_n=C.EXACT_PERM_MAX_N,
                                       signflip_mc=C.PERM_MC_N, perm_seed=C.PERM_SEED, p2_label_permutations=C.PERM_MC_N // 10, alpha=C.ALPHA, min_unknown_pairs=C.MIN_UNKNOWN_PAIRS)

# ---------------- 3. Inconclusive conditions (PRE-REGISTERED, V0.4 s7.4) ----------------
ic = frozen["inconclusive_conditions"]
wcsv("T2_inconclusive_conditions.csv", [
 ["1 fewer than 10 Unknown pairs", ic["1_fewer_than_10_unknown_pairs"], f"{len(unk)} Unknown pairs ({', '.join(unk)})"],
 ["2 positive control fails (median H(A) not below median H(B-Unknown))", ic["2_positive_control_fails"],
  f"median H3 A {np.median(HA):.3f} vs B-Unknown {np.median([by[(p,'B')]['H3'] for p in unk]):.3f} bits (B-Unknown n = {len(unk)})"],
 ["3 >25% non-answers in B or C greedy (three-shot)", ic["3_nonanswers_over_25pct"], "automatic: B 0/30, C 0/30 (+1 UNMATCHED, adjudicated FABRICATED, Decision 15)"],
 ["4 formats give clear opposite-sign results", ic["4_format_dependent"], "Unknown-pair intervals in both formats contain 0"],
 ["5 integrity or implementation defect", ic["5_integrity_defect"], "integrity_failures empty; runner_error null; GPU name 'NVIDIA A10' recorded as hardware identity unresolved (Decision 16)"]],
 ["condition", "met (True = inconclusive)", "evidence"])

# ---------------- 4. Condition summaries (DESCRIPTIVE) ----------------
cs = []
for c in "ABCD":
    rr = [r for r in R if r["cond"] == c]
    for key, unit in (("H3", "bits"), ("H0", "bits"), ("pmax3", "prob"), ("pmax0", "prob"), ("d_R1S1", "log-prob"), ("d_R2S2", "log-prob"),
                      ("surprisal_q", "mean neg. log-prob per question token"), ("m2_entropy_bits", "bits")):
        x = np.array([r[key] for r in rr], float)
        f4 = lambda v: f"{float(v) + 0.0:.4f}".replace("-0.0000", "0.0000")
        cs.append([c, key, unit, len(x), f4(x.mean()), f4(np.median(x)), f4(x.std(ddof=1)), f4(x.min()), f4(x.max())])
wcsv("T3_condition_summaries.csv", cs, ["condition", "measure", "unit", "n", "mean", "median", "sd", "min", "max"])

# ---------------- 5. Behaviour: M4 automatic and adjudicated (DESCRIPTIVE) ----------------
CATS = ("CORRECT_ANSWER", "CORRECT_REJECTION", "FALSE_REJECTION", "ABSTENTION", "FABRICATED_OR_INCORRECT", "NONANSWER", "UNMATCHED")
key = json.load(open(f"{EV}/m4_second_rater/key.json"))["key"]
dec = {}
for row in csv.DictReader(open(f"{EV}/m4_second_rater/pi_adjudication_DECIDED.csv")):
    if row["PI_decision"] in CATS: dec[(key[row["row_id"]]["item"], key[row["row_id"]]["format"])] = row["PI_decision"]
assert len(dec) == 5, dec
beh = []
for layer in ("automatic (frozen)", "adjudicated (Decision 15)"):
    for fmt, f in (("three-shot", "code3"), ("no-demo", "code0")):
        for c in "ABCD":
            cnt = {k: 0 for k in CATS}
            for r in R:
                if r["cond"] != c: continue
                cat = r[f]["category6"]
                if layer.startswith("adj"): cat = dec.get((r["item"], fmt), cat)
                cnt[cat] += 1
            beh.append([layer, fmt, c, sum(cnt.values())] + [cnt[k] for k in CATS])
wcsv("T4_M4_behaviour.csv", beh, ["layer", "format", "condition", "n"] + list(CATS))
m2 = []
for c in "ABCD":
    tot = {"CITY": 0, "UNMATCHED": 0, "REJECTION": 0, "ABSTENTION": 0, "NONANSWER": 0}
    for r in R:
        if r["cond"] == c:
            for g, n in r["m2_groups"].items(): tot[g.split(":")[0]] += n
    m2.append([c, sum(tot.values())] + list(tot.values()))
wcsv("T5_M2_sample_groups.csv", m2, ["condition", "samples", "CITY", "UNMATCHED", "REJECTION", "ABSTENTION", "NONANSWER"])

# ---------------- 6. Per-pair table (DESCRIPTIVE) and knownness vs recall ----------------
pp = []
for p in pairs:
    b, c = by[(p, "B")], by[(p, "C")]
    pp.append([p, cls[p], b["series"], c["series"], b["answer"], b["greedy3"]["text"].strip(), b["code3"]["category6"], c["greedy3"]["text"].strip(),
               f"{b['H3']:.4f}", f"{c['H3']:.4f}", f"{c['H3']-b['H3']:.4f}", f"{c['H0']-b['H0']:.4f}", f"{c['d_R1S1']-b['d_R1S1']:.4f}",
               f"{c['d_R2S2']-b['d_R2S2']:.4f}", f"{min(f['margin'] for f in K[p]['formulations']):.3f}"])
wcsv("T6_per_pair.csv", pp, ["pair", "knownness", "B_series", "C_series", "B_answer", "B_greedy3", "B_code3", "C_greedy3", "H3_B", "H3_C",
                             "dH3", "dH0", "dR1S1", "dR2S2", "min_knownness_margin"])
kr = []
for k_ in ("Known", "Uncertain", "Unknown"):
    ps = [p for p in pairs if cls[p] == k_]
    kr.append([k_, len(ps), sum(by[(p, "B")]["code3"]["category6"] == "CORRECT_ANSWER" for p in ps),
               sum(by[(p, "B")]["code0"]["category6"] == "CORRECT_ANSWER" for p in ps)])
wcsv("T7_knownness_vs_recall.csv", kr, ["M3a class", "pairs", "B greedy correct (three-shot)", "B greedy correct (no-demo)"])

# ---------------- 7. Uncertainty: seed sensitivity of the resampling (REPRODUCIBILITY) ----------------
seeds = [20261116, 1, 2, 3, 4, 5]
ss = []
for name, key_, sub in (("P1_all_pairs_3shot", "H3", pairs), ("known_pairs_3shot", "H3", kn), ("P3_R1S1_all_pairs", "d_R1S1", pairs),
                        ("P3_R2S2_all_pairs_robustness", "d_R2S2", pairs), ("sens_all_0shot", "H0", pairs)):
    x = D(key_, sub)
    for s in seeds:
        lo, hi = bootstrap_ci(x, seed=s); pr = signflip_perm_test(x, seed=s)
        ss.append([name, s, f"{lo:.4f}", f"{hi:.4f}", f"{pr['p']:.4f}"])
x2 = []
for s in seeds:
    t = two_sample(HC, HA, seed=s); x2.append(["P2_C_vs_A", s, f"{t['ci'][0]:.4f}", f"{t['ci'][1]:.4f}", f"{t['p']:.6f}"])
wcsv("T8_seed_sensitivity.csv", ss + x2, ["analysis", "seed (20261116 = frozen)", "ci95_lo", "ci95_hi", "p"])

# ---------------- 8. EXPLORATORY-POSTHOC: series stratification (Decision 16, 9B) ----------------
grp = {"B is ICM": [], "C is ICM": [], "neither ICM": []}
for p in pairs:
    g = "B is ICM" if by[(p, "B")]["series"] == "ICM" else "C is ICM" if by[(p, "C")]["series"] == "ICM" else "neither ICM"
    grp[g].append(by[(p, "C")]["H3"] - by[(p, "B")]["H3"])
wcsv("T9_EXPLORATORY_series_strata.csv", [[g, len(v), f"{np.mean(v):.4f}", f"{np.median(v):.4f}", sum(d > 0 for d in v)] for g, v in grp.items()],
     ["stratum (EXPLORATORY-POSTHOC; no test; Decision 16)", "n", "mean dH3", "median dH3", "n positive"])
stats["exploratory_series_strata"] = {g: dict(n=len(v), mean=float(np.mean(v))) for g, v in grp.items()}

# ---------------- 9. Figures ----------------
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
INK, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"     # reference categorical slots 1-3 (all-pairs validated)
plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": SURF, "axes.facecolor": SURF})
def save(fig, name): fig.tight_layout(); fig.savefig(f"{OUT}/{name}", dpi=160); plt.close(fig)
rng = np.random.default_rng(0)   # horizontal jitter only

fig, ax = plt.subplots(figsize=(6.4, 3.8))
for i, c in enumerate("ABCD"):
    y = [r["H3"] for r in R if r["cond"] == c]
    ax.scatter(i + rng.uniform(-0.15, 0.15, len(y)), y, s=22, color=S1, alpha=0.75, edgecolor=SURF, linewidth=0.8)
    ax.hlines(np.median(y), i - 0.3, i + 0.3, color=INK, linewidth=2); ax.text(i + 0.33, np.median(y), f"{np.median(y):.2f}", va="center", color=MUTED, fontsize=8)
ax.set_xticks(range(4), ["A familiar\n(n=12)", "B obscure real\n(n=30)", "C fictional\n(n=30)", "D impossible\n(n=12)"])
ax.set_ylabel("First-token entropy, three-shot (bits)"); ax.grid(axis="y", color=GRID, linewidth=0.6); ax.set_axisbelow(True)
ax.set_title("Fig. 1  M1 entropy by condition (DESCRIPTIVE); bar = median", loc="left", fontsize=9, color=INK)
save(fig, "fig1_entropy_by_condition.png")

order = sorted(pairs, key=lambda p: by[(p, "C")]["H3"] - by[(p, "B")]["H3"])
fig, ax = plt.subplots(figsize=(6.4, 5.9))
mk = {"Known": ("o", S1), "Uncertain": ("s", S2), "Unknown": ("D", S3)}
for k_, (m, col) in mk.items():
    idx = [i for i, p in enumerate(order) if cls[p] == k_]
    ax.scatter([by[(order[i], "C")]["H3"] - by[(order[i], "B")]["H3"] for i in idx], idx, marker=m, s=34, color=col, edgecolor=SURF, linewidth=0.8,
               label=f"{k_} (n={len(idx)})", zorder=3)
t = tests["P1_all_pairs_3shot"]; ax.axvspan(t["ci95"][0], t["ci95"][1], color=GRID, zorder=1)
ax.axvline(0, color=MUTED, linewidth=1); ax.axvline(t["mean"], color=INK, linewidth=1.5, linestyle="--")
ax.set_yticks(range(len(order)), order, fontsize=7); ax.set_xlabel("H(C) − H(B), three-shot (bits)")
ax.legend(frameon=False, loc="lower right", fontsize=8, title="M3a knownness of B", title_fontsize=8)
ax.set_title(f"Fig. 2  P1 paired differences, all 30 pairs (descriptive)\nshaded = 95% bootstrap CI of the mean ({t['ci95'][0]:.2f} to {t['ci95'][1]:.2f}); dashed = mean {t['mean']:.2f}\nthe pre-registered primary estimand uses only the 2 Unknown pairs (diamonds)",
             loc="left", fontsize=8.5, color=INK)
save(fig, "fig2_P1_paired_differences.png")

fig, ax = plt.subplots(figsize=(6.4, 3.6))
cols = {"B is ICM": S1, "C is ICM": S2, "neither ICM": S3}
for i, (g, v) in enumerate(grp.items()):
    ax.scatter(np.array(v), i + rng.uniform(-0.12, 0.12, len(v)), s=30, color=cols[g], edgecolor=SURF, linewidth=0.8, zorder=3)
    ax.vlines(np.mean(v), i - 0.3, i + 0.3, color=INK, linewidth=2); ax.text(np.mean(v), i + 0.36, f"mean {np.mean(v):+.2f}", ha="center", fontsize=8, color=MUTED)
ax.axvline(0, color=MUTED, linewidth=1); ax.set_yticks(range(3), [f"{g}\n(n={len(v)})" for g, v in grp.items()])
ax.set_xlabel("H(C) − H(B), three-shot (bits)"); ax.set_ylim(-0.6, 2.7)
ax.set_title("Fig. 3  EXPLORATORY, POST HOC (Decision 16): paired differences by congress series\nassociation only; no test; causation not established",
             loc="left", fontsize=8.5, color=INK)
save(fig, "fig3_EXPLORATORY_series_strata.png")

fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.6), sharey=False)
for ax, (key_, nm) in zip(axs, (("d_R1S1", "R1/S1 (test)"), ("d_R2S2", "R2/S2 (robustness)"))):
    for i, c in enumerate("ABCD"):
        y = [r[key_] for r in R if r["cond"] == c]
        ax.scatter(i + rng.uniform(-0.15, 0.15, len(y)), y, s=18, color=S1, alpha=0.75, edgecolor=SURF, linewidth=0.6)
        ax.hlines(np.median(y), i - 0.3, i + 0.3, color=INK, linewidth=2)
    ax.axhline(0, color=MUTED, linewidth=1); ax.set_xticks(range(4), list("ABCD")); ax.grid(axis="y", color=GRID, linewidth=0.6); ax.set_axisbelow(True)
    ax.set_title(nm, fontsize=9, color=INK, loc="left")
axs[0].set_ylabel("d(q) = log P(reject) − log P(accept)")
fig.suptitle("Fig. 4  M3b rejection preference per item (DESCRIPTIVE); below 0 = acceptance preferred", x=0.01, ha="left", fontsize=9, color=INK)
save(fig, "fig4_M3b_rejection_preference.png")

# ---------------- 10. Gate 6 closure check (targeted; Qualam corrections 1-5 and Decision 16) ----------------
rep = open(os.path.join(ROOT, "docs/MAIN_PRELIMINARY_REPORT_2026-11-16.md"), encoding="utf-8").read()
checks = {
 "1 current report (Decision 15 present, nothing 'pending' about adjudication)": "Decision 15" in rep and "PI adjudication pending" not in rep,
 "2 P2 narrowed": "This comparison is descriptive: it does not establish that B and C are equivalent" in rep,
 "3 P3/M4 wording": "Rejection was rare, and P3 found no statistically supported preference difference" in rep,
 "4 series qualified": "does not exclude a contribution from truth status" in rep,
 "5 provenance qualified": "documented by Claude from files and PI statements" in rep,
 "Decision 16 recorded (report + decision file)": "Decision 16" in rep and os.path.exists(os.path.join(ROOT, "decisions/PI_DECISION_16_2026-11-16.md")),
}
stats["gate6_closure_check"] = dict(report_sha256=sha(os.path.join(ROOT, "docs/MAIN_PRELIMINARY_REPORT_2026-11-16.md")), checks=checks)

stats["all_pre_registered_blocks_match_frozen"] = all(v.get("matches_frozen", True) for v in tests.values())
json.dump(stats, open(f"{OUT}/gate7_stats.json", "w"), indent=1, default=float)
files = sorted(f for f in os.listdir(OUT) if f != "SHA256SUMS")
open(f"{OUT}/SHA256SUMS", "w").write("".join(f"{sha(f'{OUT}/{f}')}  {f}\n" for f in files))
print(json.dumps(dict(reproduced=stats["frozen_analysis_reproduced_exactly"], all_match=stats["all_pre_registered_blocks_match_frozen"],
                      gate6_checks=checks, files=files), indent=1))
