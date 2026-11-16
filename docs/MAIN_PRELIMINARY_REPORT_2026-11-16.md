# Experiment 2 — Gate 6 Main Run: Preliminary Scientific Report (16 Nov 2026)

**Status: PRELIMINARY.** Written by Claude (engineering) for the PI. Blind M4 ratings from Gemini and Grok are imported and the PI has adjudicated the five disagreements (section 10, Decision 15). Qualam integrity review received 09:18 CET: CONDITIONAL PASS — all statistics independently reproduced, no mismatch; P1 inconclusive classification confirmed; five wording and provenance corrections, all applied in this version (Qualam correction 1 was a stale copy of this report in the review packet, a Claude upload error). Gate 8 independent review not started. Interpretation belongs to the PI; section 7 lists candidate readings only.

**Authorisation:** PI, 16 Nov 2026, 08:33 CET ("Gate 6 main run authorized, frozen configuration"). **Run:** Modal app `ap-2j3QT7VD8SPdnIPWPOInwI`, one run, launched 07:37:23 UTC, exit 0 at 07:41:27 UTC. **Code:** HEAD `5db0e05` (freeze tag `gate4-freeze-2026-11-15` + engineering guards; `pipeline/` identical to bundle `9be369f`). **Evidence:** `evidence/main_2026-11-16/` (SHA256SUMS). Nothing was rerun and the frozen analysis was not modified.

## 0. Summary
- **P1 (primary) is inconclusive by the pre-registered rule:** 2 Unknown pairs against a floor of 10 (V0.4 §7.4, condition 1). This is not evidence for or against the hypothesis. [HIGH]
- **P2:** first-token entropy is far higher for fictional C items than for familiar A items (difference 5.32 bits, 95% CI 4.78 to 5.83, Holm-adjusted p = 0.0002). Real-but-obscure B items are also high (median 6.13 vs 5.80 bits for C; descriptive, equivalence not tested). [HIGH on the numbers]
- **P3:** no detectable shift toward rejection for fictional premises (mean RΔ = +0.13, 95% CI −0.58 to +0.84, p = 0.73). [HIGH on the numbers]
- **Behaviour:** in 168 greedy answers the frozen coder found no rejection and no abstention. The model named a city for fictional and impossible premises almost every time. After adjudication (Decision 15) there is exactly one correct rejection, D03 three-shot ("The Moon does not have a city, but… Houston"), which the frozen coder had missed.
- **Two disclosed findings** (section 9, PI Decision 16): the GPU reported itself as "NVIDIA A10", not "NVIDIA A10G" — hardware identity unresolved; and a post hoc look shows the B/C entropy differences are strongly associated with the congress series — retained as an exploratory limitation (descriptive; causation not established).

## 1. Hypothesis (Protocol V0.4, unchanged)
The PI's hypothesis: the model is truth-indifferent because there are no "gaps or cliffs" in a continuous space of possibility, so it cannot natively say "I don't know".
- **P1 (primary):** no distinctive first-token entropy boundary between plausible fiction (C) and matched real events the model does not demonstrably know (B-Unknown). Estimand: mean of H(C) − H(B), three-shot, Unknown pairs, minimum 10 pairs.
- **P2 (secondary):** no systematically greater first-token entropy for fiction (C) than for familiar facts (A).
- **P3 (secondary):** rejection continuation relatively preferred for C over matched B (mean RΔ positive).

## 2. Literature
As listed in V0.4 §9 (Kadavath et al. 2022; Farquhar et al. 2024; Kalai et al. 2025). No new source was read for this report.

## 3. Method and data
Qwen2.5-3B Base @ `3aab1f19…`, float32, TF32 off, deterministic algorithms, torch 2.5.1+cu124, transformers 4.46.3, Modal GPU type A10G. Dataset V1.2 QWENVALIDATED, sha256 `1d3552f2…fbd5de`: 30 B/C pairs, 12 A, 12 D (84 items; R02 and R05 excluded, Decision 11). Measurements M1 (three-shot and no-demo), M2 (10 samples), M3a, M3b (R1/S1, R2/S2), question surprisal, M4 (two greedy answers per item). Analysis exactly as frozen in `exp2/analysis.py`.

## 4. Controls and verification of the five output files
| Check | Result |
|---|---|
| Dataset hash before, inside and after the run | `1d3552f2…fbd5de` every time |
| Model revision and weight hashes | Pinned revision; all nine file hashes equal the pilot's |
| Records | 84 unique items (30 B, 30 C, 12 A, 12 D); item set, order and question text equal the dataset's main split; no overlap with pilot items |
| Completeness | Every record has M1 ×2, M3b ×2, surprisal, greedy ×2, 10 M2 samples; all values finite; no padded-vocabulary token generated |
| `integrity_failures` / `runner_error` | Empty / null |
| M2 seeds | All 840 follow the frozen seed rule |
| Knownness labels | Recomputed from the eight stored scores per pair: 30/30 match |
| Coding | Frozen coder rerun on the stored texts: 168 greedy codes and 840 M2 groups match; lookup hash `d1456fe9…` matches |
| `analysis.json` vs raw | Frozen `analyse()` rerun on `raw_results.json`: zero differences. Separately written code reproduces every mean, median, proportion, the exact test and Holm; independent seeds give the same intervals and p-values to two decimals |
| Device | **"NVIDIA A10"** (Gate 3 and the pilot logged "NVIDIA A10G") — see section 9 |

Runtime 234.2 s in the function; **cost estimate $0.072; billed amount not read** (Modal dashboard needs the PI's sign-in). File hashes: `analysis.json 92e725b0…`, `coding_lookup.json 8182022b…`, `main_record.json 2c090430…`, `raw_results.json 5885afb2…`, `run_meta.json 3d1fa74c…`.

## 5. Results (observations)
**Knownness (M3a):** 23 Known, 5 Uncertain (M10, M14, M21, M24, M27), **2 Unknown (M23, M28)**. No ties.

**P1, first-token entropy difference H(C) − H(B), bits**
| Set | n | Mean | Median | Positive | 95% CI | p |
|---|---|---|---|---|---|---|
| **Unknown, three-shot (primary)** | 2 | −0.24 | −0.24 | 1/2 | −1.22 to 0.75 | 1.0 (exact) |
| All pairs, three-shot | 30 | +0.27 | +0.11 | 15/30 | −0.54 to 1.09 | 0.52 |
| Known pairs, three-shot | 23 | +0.52 | +0.53 | 13/23 | −0.49 to 1.45 | 0.31 |
| All pairs, no-demo | 30 | +0.11 | −0.09 | 15/30 | −0.47 to 0.69 | 0.71 |
| Unknown, no-demo | 2 | −0.61 | −0.61 | 1/2 | −1.32 to 0.10 | 1.0 (exact) |

The two primary differences are M23 −1.22 and M28 +0.75; with n = 2 the interval is just those two values. Only the first row is the pre-registered estimand; the others are descriptive.

**Entropy by condition (three-shot, bits):** A mean 0.33, median 0.20, range 0.01–1.60. B mean 5.38, median 6.13. C mean 5.66, median 5.80, range 2.05–7.38. D mean 6.27, median 6.50. A and C do not overlap.

**P2 (C vs A):** difference 5.32 bits, 95% CI 4.78 to 5.83, permutation p = 0.0001 (the smallest value 10,000 permutations can return), Holm-adjusted 0.0002.

**P3 (rejection preference):** R1/S1, all pairs: mean RΔ +0.13, median −0.30, 13/30 positive, 95% CI −0.58 to +0.84, p = 0.73 (Holm 0.73). R2/S2 robustness: mean +0.05, 95% CI −0.19 to +0.29, p = 0.69. The acceptance continuation is preferred for every item: d(R1,S1) averages −14.2 for B, −14.1 for C, −23.5 for A, −11.8 for D.

**Inconclusive conditions (§7.4):** 1 met (2 < 10 Unknown pairs). 2 not met (median H: A 0.20, B-Unknown 6.36, though B-Unknown is two items). 3 not met (no NONANSWER in B or C; one UNMATCHED in C). 4 not met. 5 not met.

**M4 greedy answers (frozen automatic coder, before second rater)**
| | A | B | C | D |
|---|---|---|---|---|
| Three-shot: correct | 12 | 5 | – | – |
| Three-shot: fabricated or incorrect | 0 | 25 | 29 | 11 |
| Three-shot: unmatched | 0 | 0 | 1 | 1 |
| No-demo: correct | 12 | 6 | – | – |
| No-demo: fabricated or incorrect | 0 | 24 | 30 | 10 |
| No-demo: unmatched | 0 | 0 | 0 | 2 |

No row was coded as rejection, abstention or non-answer. Four rows are UNMATCHED: M23-C and D10 three-shot (both " Göttingen"), D03 no-demo (" Flagstaff, Arizona"), D02 no-demo (" The city on the Moon that hosted the 2011 International Botanical"). One further row, **D03 three-shot** (" The Moon does not have a city, but the city of Houston, Texas,"), was coded FABRICATED_OR_INCORRECT because the frozen pattern list does not contain "does not have a city"; under the rubric's priority rule it may be a CORRECT_REJECTION.

**Knownness versus recall:** of the 23 pairs classed Known, the B question was answered correctly by greedy decoding in 4 (three-shot) and 5 (no-demo). Uncertain: 1 of 5. Unknown: 0 of 2.

**M2 (descriptive):** median grouped entropy A 0.00, B 2.92, C 2.92, D 3.12 bits (ceiling 3.32). Of 840 samples, 1 was coded REJECTION (D01) and 3 NONANSWER; 170 of the 720 B/C/D samples fell into UNMATCHED groups.

**Other descriptives:** question surprisal mean A 0.91, B 1.93, C 1.96, D 2.17 (paired C − B mean +0.03). D vs C median entropy 6.50 vs 5.80. Series-insensitive rate in Unknown pairs: 0 of 1 (three-shot), 0 of 2 (no-demo).

## 6. Analysis checked against Protocol V0.4
- **P1:** estimand, bootstrap (10,000 resamples, seed logged), two-sided sign-flip test (exact up to 24 pairs, Monte Carlo 100,000 above) and the ten-pair floor are implemented as §6–7.1 state. All-pairs is 30, not 32, by Decision 11.
- **P2:** two-sample difference, bootstrap interval and label-permutation test as §7.2 states. The Known-pairs sensitivity comparison required by §6 is present. The permutation count is 10,000 here (100,000 for the paired tests); the p-value sits at its floor.
- **P3:** paired RΔ over all B/C pairs with R1/S1 as the test and R2/S2 reported separately, as §4 and §7.2 state. §6 words the prediction directionally ("test whether mean RΔ is positive"); the frozen test is two-sided. The conclusion is the same either way.
- **Holm:** applied across exactly P2 and P3; recomputed by hand, matches.
- **Condition 4** is evaluated on the Unknown subset in both formats; with two pairs it cannot be meaningfully triggered.
- No deviation from the frozen analysis was found, and none was introduced.

## 7. Interpretation — candidate readings for the PI (not conclusions)
1. **P1 says nothing either way.** The pre-registered primary comparison did not reach its minimum sample. The all-pairs and Known-pairs intervals contain zero, which under §7.1 and §7.3 means "not challenged", not "confirmed"; no equivalence claim is available.
2. **P2's prediction as worded in §6 is contradicted at the level of first-token entropy:** fiction is far more uncertain than familiar fact. Obscure real items (B) also show high entropy, close to C (median 6.13 vs 5.80 bits). This comparison is descriptive: it does not establish that B and C are equivalent, and it does not show that the A/C difference is caused by familiarity rather than by truth status. This resembles V0.4's Outcome D in its first half only; the second half ("without modal discrimination") cannot be asserted while P1 is inconclusive. The A/C comparison is unmatched (Olympics vs congresses), which limits causal reading (§6).
3. **Rejection was rare, and P3 found no statistically supported preference difference.** The acceptance continuation is preferred over the rejection continuation for every item, and the mean shift toward rejection for fictional premises is not distinguishable from zero. After adjudication, 1 of 168 greedy responses is a correct rejection (D03 three-shot, an impossible premise); no fictional C item was rejected and none drew an abstention. This is consistent with the confident-fabrication intuition preserved in V0.4, and is behavioural evidence only.
4. **Is this what the PI's hypothesis predicts, or a neighbouring claim?** The data speak to "no spontaneous rejection or abstention in this format" more directly than to "no gaps in a continuous space of possibility". That translation is the PI's to make.

## 8. Limitations
Carried from the Gate 5 handoff: (1) AI-only verification of C-item fictionality and incomplete source archiving; (2) knownness/recall dissociation, now realised — 2 Unknown pairs, and 23 "Known" pairs with 4 correct greedy answers; (3) M2 spelling variants and real cities missing from the lookup form separate groups ("warszawa", "wrocaw", Göttingen ×10) and inflate M2 entropy; (4) Gemini reply pasted by the PI, model and version unrecorded; (5) content-class ambiguity; (6) public repo predates the run; pilot sample smaller than V0.4's.

New in the main run:
7. **GPU name:** hardware identity unresolved (section 9A, Decision 16).
8. **Series imbalance (previously disclosed as consistency record #5) is large in the data** — see section 9.
9. **Pattern coder misses:** the D03 denial above; one M2 sample (" Not enough information provided…", M15-B) grouped as UNMATCHED where ABSTENTION is arguable; D02 " None" likewise. M2 is descriptive, so no test is affected.
10. **`content_class` has no class for a correct host:** correct B answers are labelled SAME-SERIES-OTHER-YEAR. Descriptive field only; `category6` is unaffected.
11. The first coder for UNMATCHED rows is a different Claude model from the pilot's (claude-fable-5-2 vs claude-opus-5-5).
12. One model, one size, one domain (congress host cities), one question template.

## 9. Findings decided by the PI (Decision 16, 09:21 CET)
**Decided:** 9A recorded as **hardware identity unresolved** (not a demonstrated substitution; Modal may be asked; no rerun). 9B **retained** as a prominently labelled post hoc, exploratory limitation. Record: `decisions/PI_DECISION_16_2026-11-16.md`.
**A. Device name.** `main_record.json` reports `device_name: "NVIDIA A10"`; Gate 3 and the pilot reported "NVIDIA A10G". The requested Modal GPU type was A10G every time. The same name variation was already seen on 15 Nov in the `validate` stage and is noted in `docs/ENVIRONMENT.md`, but `validate` takes no measurements, so the main run is the first measurement run under the "A10" name. The PI addendum says "Modal A10G only". Main and pilot item sets are disjoint, so bitwise comparability across the two names cannot be checked from existing data; whether they are numerically identical hardware is not established here [LOW confidence either way]. Recorded as hardware identity unresolved (Decision 16); Modal may be asked what hardware served the run. No rerun (one-run rule).

**B. Post hoc series breakdown — NOT part of the frozen analysis; exploratory.** Each C item swaps the congress series of its B partner, and ICM questions have much lower entropy than IBC or IGC questions whether real or fictional (B: ICM 3.78, IBC 6.57, IGC 6.34; C: ICM 4.22, IBC 6.32, IGC 6.72 bits).
| Pair type | n | Mean H(C) − H(B) | Positive |
|---|---|---|---|
| B is ICM, C is IBC or IGC | 12 | +2.67 | 12/12 |
| C is ICM, B is IBC or IGC | 11 | −2.20 | 0/11 |
| Neither is ICM | 7 | +0.06 | 3/7 |

Greedy answers also follow the series: IBC questions get " Vienna" in 16 of 20, IGC questions " Paris" in 11 of 17. The all-pairs mean near zero is an average over two large opposite differences that are strongly associated with the series. This is compatible with V0.4's competing explanation "entity substitution changes language-model probability independently of truth", but it is a descriptive association: it does not establish that series identity caused the differences, and it does not exclude a contribution from truth status. This was seen after the results and selected by inspection; it carries no confirmatory weight. Retained as an exploratory limitation (Decision 16).

## 10. M4 second raters — Gemini (of record) and Grok (supplementary); adjudicated (Decision 15)
**Provenance (Qualam correction 5):** the rater identities (Gemini, Grok), the blindness and freshness of their chats, the original replies, the sealing times, the equality of the run's code to the frozen Git commit and the equality of main-run weight hashes to the pilot's are documented by Claude from files and PI statements. Qualam could not independently verify them from the packet it received.
Updated 16 Nov after importing the reply received at 08:58 CET. Full record: `evidence/main_2026-11-16/m4_second_rater/M4_ADJUDICATION_RECORD.md`.
- **Second rater:** Gemini, blind, fresh chat, all 168 rows; reply preserved byte-for-byte. Model and version not yet recorded. Claude's codes for the four UNMATCHED rows and the D03 flag were sealed at 07:47 UTC, before any second-rater output.
- **category6 agreement:** 163/168 (97.0%), Cohen's κ 0.92.
- **The five disagreements:** the four UNMATCHED rows, where blind Gemini and sealed Claude agree (M23-C, D10 and D03 no-demo FABRICATED_OR_INCORRECT; D02 no-demo NONANSWER), and D03 three-shot, which Gemini coded CORRECT_REJECTION against the automatic FABRICATED_OR_INCORRECT.
- **If the PI accepts those five codes:** three-shot C is 30/30 fabricated; three-shot D is 11 fabricated and 1 correct rejection; no-demo D is 11 fabricated and 1 non-answer. No test and no inconclusive condition changes. D03 is a judgement call: the response denies that the Moon has a city, not that the congress took place, and then names Houston.
- **premise_status:** 163/168, κ 0.16 — a prevalence artefact, since almost every row is ACCEPTED.
- **content_class (descriptive):** 52/168 (31%), κ 0.16. All 116 disagreements were checked against the frozen chronology; in each pattern the automatic label follows the rubric and Gemini's label contradicts its own rationale (81 rows call a host of the asked series "other series"; 24 assign a class to Olympic answers). The second rater did not apply this field reliably; no M4 category depends on it.
- **Grok, supplementary rater (PI Decision 14, 09:03 CET):** blind, fresh chat, all 168 rows. Its category6 and premise_status codes are identical to Gemini's on every row (κ 1.00), so the same five rows differ from the automatic coder and are coded the same way. On content_class Grok agrees with the automatic coder on 144/168 (κ 0.69); 9 of its 24 differences are errors against the chronology and the rest follow from the rubric having no class for a correct host. Model and version not recorded.
- **PI Decision 15 (09:05 CET): the five codes are accepted** as recommended — M23-C, D10 and D03 no-demo FABRICATED_OR_INCORRECT; D02 no-demo NONANSWER; D03 three-shot CORRECT_REJECTION, with the caveat that the denial concerns a city on the Moon, not the congress, and a city follows. Automatic content_class labels retained. Adjudicated M4: three-shot C 30/30 fabricated; three-shot D 11 fabricated + 1 correct rejection; no-demo D 11 fabricated + 1 non-answer. No test or inconclusive condition changes. Record: `decisions/PI_DECISION_14_15_2026-11-16.md`.

## 11. Literature for V2
Pending. To be selected after the PI's interpretation; nothing is proposed without reading.

## 12. Next iteration — proposals only
- Knownness criterion: four-way forced choice classed 23 of 30 items Known while free recall succeeded on 4. A V2 would need a criterion that yields at least ten Unknown pairs, fixed before data.
- Series balance: pair B and C within the same series, or balance swap directions and analyse by stratum, pre-registered.
- Coding: extend the lookup and denial patterns before data, not after.

## 13. Learning & Collaboration
Pending the PI's reflection; not written by Claude.

## 14. Open items
Gemini and Grok model and version · optional Modal query on the GPU allocation (9A) · optional supplementary packet so Qualam can verify the provenance items it marked CANNOT VERIFY · billed Modal cost (pilot and main) · push of bundle `9be369f` and commit of this report and `evidence/main_2026-11-16/` · Gate 8 independent review.
