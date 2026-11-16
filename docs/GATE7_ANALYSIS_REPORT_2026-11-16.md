# Experiment 2 — Gate 7 Analysis: evidence package and report (16 Nov 2026)

**Prepared by:** Claude (implementation and reproducibility). **Methodology review:** Qualam (pending). **Interpretation and Gate 7 decision:** the PI.
**Package:** `evidence/main_2026-11-16/gate7/` (9 tables, 4 figures, `gate7_stats.json`, `SHA256SUMS`). **Script:** `analysis/gate7/gate7_analysis.py`; run from `exp2_pilot/` with `python3 analysis/gate7/gate7_analysis.py`.
**Inputs:** the frozen Gate 6 outputs only (hashes asserted by the script). The model was not rerun. Every statistic is computed by the frozen functions in `pipeline/exp2/analysis.py` / `run.py`; no procedure was changed. Two consecutive runs produced byte-identical tables and statistics (Python 3.10.12, numpy 2.2.6; frozen run used numpy 2.5.4, results identical).

Labels used throughout: **PRE-REGISTERED** (V0.4 §6–7) · **DESCRIPTIVE** (V0.4, no confirmatory claim) · **EXPLORATORY-POSTHOC** (not in V0.4, chosen after seeing data) · **REPRODUCIBILITY** (checks of the computation).

## 0. Gate 6 closure (targeted check)
Checked against the current preliminary report (sha256 `06d9bee4…`) and `decisions/`: Qualam corrections 1–5 present; Decision 16 recorded in the report and in `PI_DECISION_16_2026-11-16.md`. All six checks PASS (`gate7_stats.json` → `gate6_closure_check`). Qualam's confirmation of the follow-up packet is still pending.

## 1. Gate 7 checklist
| Requirement (V0.4 Gate 7 / PI-Qualam instruction) | Status | Where |
|---|---|---|
| P1, P2, P3 recomputed against V0.4: paired differences, 10,000-resample percentile bootstrap (seed 20261116), two-sided sign-flip (exact ≤ 24 pairs, Monte Carlo 100,000 above), P2 two-sample bootstrap and label permutation, Holm across P2/P3 | Done; every block matches the frozen `analysis.json` | T1, `gate7_stats.json` |
| Frozen analysis reproduced in full from raw data | Done; zero differences | `gate7_stats.json` |
| Five inconclusive conditions | Done | T2 |
| Condition summaries (M1 both formats, top-token probability, M3b, question surprisal, M2) | Done | T3, Fig. 1, Fig. 4 |
| Behavioural frequencies (M4 automatic and adjudicated; M2 response groups) | Done | T4, T5 |
| Supplementary Istanbul analysis | Done (no Istanbul pair among the Unknown pairs, so identical to primary) | T1 |
| Robustness checks (pre-registered: no-demo format, R2/S2 templates, Known-pairs, all pairs) | Done | T1 |
| Per-pair data and knownness vs recall | Done | T6, T7, Fig. 2 |
| Uncertainty assessment (resampling-seed sensitivity) | Done | T8 |
| Exploratory series breakdown (Decision 16, 9B) | Done, labelled | T9, Fig. 3 |
| Evidence-quality limitations; null, negative and unexpected findings | Done | §3–4 below |

## 2. Results, by kind of evidence

**PRE-REGISTERED statistical evidence**
| Analysis | n | Mean | 95% CI | p | Note |
|---|---|---|---|---|---|
| P1 primary, Unknown pairs, three-shot | 2 | −0.24 bits | −1.22 to 0.75 | 1.00 (exact) | **Inconclusive by §7.4 condition 1** |
| P2, mean H(C) − mean H(A) | 30 vs 12 | +5.32 bits | 4.78 to 5.83 | 0.0001 (floor of 10,000 permutations); Holm 0.0002 | C > A |
| P3, RΔ (R1/S1), all pairs | 30 | +0.13 | −0.58 to 0.84 | 0.73; Holm 0.73 | Not distinguishable from 0 |
| Istanbul supplementary | 2 | −0.24 bits | −1.22 to 0.75 | 1.00 | Same pairs as primary |

Inconclusive conditions: 1 **met** (2 Unknown pairs < 10); 2 not met (median H3: A 0.20, B-Unknown 6.36 bits, B-Unknown n = 2); 3 not met (0/30 non-answers in B and in C); 4 not met; 5 not met (GPU name recorded as hardware identity unresolved, Decision 16).

**PRE-REGISTERED robustness and sensitivity (descriptive estimates)**
| Analysis | n | Mean | 95% CI | p |
|---|---|---|---|---|
| P1 all pairs, three-shot | 30 | +0.27 bits | −0.54 to 1.09 | 0.52 |
| Known pairs, three-shot | 23 | +0.52 bits | −0.49 to 1.45 | 0.31 |
| All pairs, no-demo | 30 | +0.11 bits | −0.47 to 0.69 | 0.71 |
| Unknown pairs, no-demo | 2 | −0.61 bits | −1.32 to 0.10 | 1.00 |
| P3 R2/S2 robustness template | 30 | +0.05 | −0.19 to 0.29 | 0.69 |

**DESCRIPTIVE observations**
- First-token entropy, three-shot, median bits: A 0.20, B 6.13, C 5.80, D 6.50 (Fig. 1). Median top-token probability: A 0.98, B 0.17, C 0.165, D 0.11.
- M3b: the acceptance continuation is preferred for every one of the 84 items under both template pairs (Fig. 4).
- M4, adjudicated (Decision 15), three-shot: A 12/12 correct; B 5/30 correct, 25 fabricated or incorrect; C 30/30 fabricated; D 11 fabricated, 1 correct rejection. No abstention anywhere; no false rejection. Automatic layer shown alongside in T4.
- M2: median grouped entropy A 0.00, B 2.92, C 2.92, D 3.12 bits; 1 rejection and 3 non-answers in 840 samples (T5).
- Knownness vs recall: of 23 pairs classed Known, B was answered correctly by greedy decoding in 4 (three-shot); Uncertain 1/5; Unknown 0/2 (T7).

**EXPLORATORY-POSTHOC (no test, no confirmatory weight)**
- Paired H(C) − H(B) by congress series: B is ICM +2.67 bits (12/12 positive); C is ICM −2.20 (0/11 positive); neither +0.06 (3/7) (T9, Fig. 3). A strong association; causation not established; a contribution from truth status not excluded.

**Interpretation:** reserved for the PI. The only classifications stated here are those the protocol's own decision rules produce: P1 inconclusive (§7.4); P2's test shows C > A, which is contrary to P2's prediction as worded in §6; P3's test does not support a rejection preference for fictional premises.

## 3. Uncertainty assessment (REPRODUCIBILITY)
- **Resampling noise is small.** Across six seeds (the frozen seed plus five others; T8), bootstrap bounds move by at most 0.06 bits and permutation p-values by at most 0.005. No conclusion depends on the seed.
- **Sampling uncertainty is large.** With 2 pairs, the primary interval is just the two observed differences; the exact sign-flip test cannot give p below 0.5 at n = 2. With 30 pairs, the all-pairs interval spans about 1.6 bits.
- **P2's p-value is at its floor** (1/10,001): the true p is smaller; the 10,000-permutation count is the frozen setting.

## 4. Limitations and null, negative and unexpected findings
- **Inconclusive (not null):** P1 primary (too few Unknown pairs to test).
- **Null (interval includes 0):** P3 and its robustness template; all-pairs, no-demo and Known-pairs sensitivity estimates of P1.
- **Negative for a stated prediction:** P2 (C > A by 5.3 bits).
- **Unexpected:** knownness/recall dissociation (23 Known vs 4 recalled); series association (Fig. 3); a single correct rejection that still names a city (D03); greedy answers concentrate on a few cities per series (IBC → Vienna 16/20, IGC → Paris 11/17).
- **Evidence quality** (detail in the preliminary report §8): one model, size, domain and template; AI-only fictionality verification; GPU hardware identity unresolved; M2 lookup gaps inflate M2 entropy; content_class second-rater agreement weak (descriptive field only); rater identities and chat freshness rest on PI statements; unmatched comparison A vs C (Olympics vs congresses) limits causal reading of P2.

## 5. Decisions needed from the PI
1. **Gate 7: pass or not**, after Qualam's methodology review.
2. **P3 test sidedness — acknowledge.** V0.4 §6 words P3 directionally ("whether mean RΔ is positive"); the frozen test is two-sided. Recommendation: keep the frozen two-sided result and disclose it; the conclusion is the same either way (observed mean +0.13, CI includes 0).
3. **M4 headline layer — confirm.** Recommendation: report the adjudicated layer (Decision 15) as the M4 result, with the automatic layer alongside.
