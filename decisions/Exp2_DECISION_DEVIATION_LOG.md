# Experiment 2 — Permanent Decision and Deviation Log

Maintained by Claude (engineer) for the final report. Append-only; entries dated. Scientific authority: PI (Dr. Ali Antonio Di Fenza). Authoritative specification: Protocol V0.4 (14 Nov 2026). Nothing below changes the hypotheses, measurements, statistics or interpretation rules of V0.4.

## 1. What the experiment tests (unchanged from V0.4)

- **Model:** Qwen2.5-3B Base, revision `3aab1f1954e9cc14eb9509a215f9e5ca08227a9b`; full logits, float32; no training.
- **P1 (primary, modal discrimination):** no distinctive first-token entropy boundary between plausible fiction (C) and real-but-unknown events (B-Unknown). Estimand Δ = mean[H(Cᵢ) − H(Bᵢ)], three-shot, Unknown pairs only, floor 10 pairs; 95 % percentile bootstrap (10 000, seeded), two-sided sign-flip permutation (exact ≤ 24 pairs), median and share positive. All pairs reported as well.
- **P2 (secondary, functional uncertainty):** no systematic greater first-token uncertainty for C than for familiar facts (A); two-sample bootstrap + permutation; Known-B vs C as sensitivity.
- **P3 (secondary, premise rejection):** mean RΔ = d(C) − d(B) with d = log P(R1|q) − log P(S1|q) is positive; R2/S2 robustness reported separately. Holm across P2, P3; P1 alone at α = 0.05.
- **Measurements:** M1 first-token entropy (primary; three-shot and no-shot formats); M2 discrete semantic entropy, 10 samples, T 1.0, top-p 1.0, no top-k, rep. 1.0, 16 tokens, stop at newline, per-item seeds (descriptive); M3a knownness proxy from two declarative paraphrases vs three distractors (covariate); M3b rejection preference (secondary); M4 greedy answer in six categories with a second rater and κ (descriptive); question surprisal (diagnostic).
- **Exploratory D condition:** impossible premises compared with C descriptively; no confirmatory claim.
- **Inconclusive if:** < 10 Unknown pairs; median H(A) not below median H(B-Unknown); > 25 % uninterpretable greedy answers in B or C; the two formats give clear opposite signs; an integrity defect.
- **No equivalence claim** (PI rejected the ±0.5-bit margin).

## 2. Sample: planned vs approved

| | Planned (V0.4 §2.3) | V1.0 candidate (PI authorisation 15 Nov) |
|---|---:|---:|
| Main B/C pairs | 32 | **32 (V1.2, amendment A2)**; V1.0 had 23, V1.1 had 21 |
| Pilot B/C pairs | 6 | **4 (V1.2)**; V1.1 had 2 |
| A main / pilot | 12 / 4 | 12 / 4 |
| D main / pilot | 16 / 4 | 12 / 3 |

V1.2 (current): all M-pairs except M05, M06, M08, M17, plus R02, R05, R06, R10; pilot P02, P03, P04, P06. Earlier: included main pairs (V1.1): M01 M02 M03 M04 M07 M09 M10 M11 M13 M16 M18 M20 M23 M24 M25 M26 M28 M29 M30 M31 M32 (M16, M18, M28 at MED). Pilot: P03 P06. V1.0 (23 main, 4 pilot: + M19, M27, P02, P04) is preserved as a separate file.

## 3. Exclusions and reasons

| Pair | Reason |
|---|---|
| M05 | Imperial Botanical Conference, London, 7–16 July 1924; described at the time as comparable to an International Congress while the IBCs were in abeyance |
| M06 | INQUA's own history: founded "at the International Geological Congress held in Copenhagen" in 1928 (FAIL-level) |
| M08 | Same INQUA page ties a 1936 Vienna meeting to an IGC; 1933 press announced the next IGC for "1936 or 1937" |
| M19 | 5th International Congress of the International Association of Engineering Geology, Buenos Aires, 20–25 Oct 1986 (series check 17:45; reverses the 17:10 recovery) |
| M27 | BGCI 8th International Congress on Education in Botanic Gardens, Mexico City, 12–16 Nov 2012 (series check 17:45; reverses the 16:18 recovery) |
| P02 | 2nd World Botanic Gardens Congress incorporating the 7th International Botanic Gardens Conservation Congress, Barcelona, April 2004 |
| P04 | International Congress on Mathematical Physics, Kyoto 1975 |
| M12 | 2nd International Congress of the International Association of Engineering Geology, São Paulo, Aug 1974 (found by the adversarial reviewer; name rule) |
| M14 | 1910 Brussels international congress on mathematics teaching (ICMI) |
| M15 | 5th International Congress of Botanic Gardens, Cape Town, Sept 1998 (name rule; reviewer rated it usable at MED) |
| M17 | A memoir calls the Sept 1935 Moscow Topology Conference "ICM-1935"; attribution is not a publication artefact |
| M21 | Frascati, Oct 1964, listed by ICMI among its "international congresses" |
| M22 | First International Congress on Mathematical Education, Lyon 1969 |
| P01 | ICME-13, Hamburg, July 2016 (IMU/ICMI); 7ECM Berlin 2016 |
| P05 | ICME-15, Sydney, July 2024 |
| D13–D16, DP04 | "…, held in no city?" is neither a logical contradiction nor a physical impossibility (V0.4 §2.2); excluded from D, retained in file |

Recovered after review: M01, M03, M04, M10, M24, M30, M32, P06 (16:18); M18, M28 (17:10). M27 and M19 were recovered and then excluded again at 17:45 when the full ICME/ICMP/IAEG/BGCI congress lists were checked. Confirmed over run-1 dissent: M12 (later excluded on a new finding), M16, M26.

Rule applied to every C candidate (disclosed): an event is confusable if its own name contains "International", the series' discipline word (mathemat-/botan-/geolog-) and "Congress/Conference", or if contemporary sources describe it as a substitute for the series; explicitly national or regional names are not candidates; publications, circulars, commission meetings and society sessions are not candidates; a source attributing the series name to the C year excludes the pair unless the attribution is demonstrably a publication-year or imprint artefact.

## 4. Verification limitations

- **Checker not independent:** Gemini could not run (search quota, 14 Nov); Qualam (GPT-6), a design participant, verified all 96 rows (Deviation 1). Run 1's log was lost; run 2 is the record (Deviation 2).
- **No human spot-check:** decision 8's human review was not performed. Replaced by Claude adjudication (15 Nov, 16:13–16:18 and 16:42–16:50) and an independent adversarial review by a fresh Claude instance with no prior verdicts (17:01–17:05). Both are AI reviews (Deviation 3). A prioritised "Human Spot-Check Sheet" is in the adjudicated log for a later human pass.
- **No archive snapshots:** archive.org unreachable from the workspace; Mac folder access not granted. Verbatim, hashed captures of the three organiser chronologies were taken via the desktop browser; 44 other URLs remain unarchived (`archive_urls.txt`, `archive_save.py`) (Deviation 4).
- **Selection:** exclusions remove the fictional years with a nearby similarly named event; surviving fictions may be the least attested. Series balance of included C items: IBC 9 / ICM 8 / IGC 6.
- **Checker's judgement unstable between runs** (13 of 38 C items changed verdict between run 1 and run 2); disclosed.

## 5. Decisions (PI unless marked)

| 15 Nov ~20:36 | **PI Decision 12:** residual verification risks accepted; PI instruction: FREEZE. Pilot and main experiment not authorised. Source: the PI's Gate 4 instruction message of 15 Nov (~20:36 CET). The full written text of Decision 12, including the list of accepted risks, is **not in this archive** (see `docs/GATE4_FREEZE.md`, missing evidence). |
| 15 Nov 19:32 | **PI methodological clarifications C1–C4** after the Qualam Gate 3 review (labelled "PI decisions 12–15" in earlier versions of this log; relabelled at the freeze because the PI numbers the risk-acceptance decision as Decision 12; content unchanged): P3 two-sided (direction reported); knownness strictly highest, ties recorded; one shared M2/M4 coder before Gate 3; second rater Gemini, blind. All 16 implementation corrections approved for execution. See `Exp2_Gate3_Corrections_ChangeLog_2026-11-15.md`. |

| 15 Nov 19:20 | **PI decision 11:** drop R05 (Sydney: no Oceania city within the distractor rule). Drop R02 as well if Kyoto still fails with the Asia-wide pool. Applied via `apply_validate.py --exclude`. Main sample becomes 31 pairs, or 30 if R02 is dropped. |

| 15 Nov 17:48 | **Amendment A2** (applied 17:55 on explicit PI instruction): named-series criterion; restores M12, M14, M15, M21, M22; adds R02, R05, R06, R10; rebases D06, D09, D10, D12. Closes decision 10 (option B+C). Full text: `Exp2_Amendment_A2_2026-11-15.md` |

| Date | Decision |
|---|---|
| 14 Nov | V0.4 approved; Mars D type → "held in no city"; D14 rebased to ICM 1966; 50 % series-insensitive threshold (descriptive); P01/P02 cross-continent distractors (pilot only); P05 retained with cutoff flag; Istanbul distractors retained + sensitivity analysis; P04 modern-name aliases; human 10 % spot-check; UNCERTAIN C → replace, never waive; amendment A1 ("first 20 results" → up to 20, count logged) |
| 15 Nov 16:13 | Written authorisation: 60-minute adjudication; unresolved pairs excluded rather than replaced; reduced sample authorised; originals preserved |
| 15 Nov 16:54 | Verification completed autonomously; AI review not to be presented as human verification |
| 15 Nov 17:10 (Claude, engineering) | Demonstrations fixed: Lima / Nairobi / Agra (outside test domains; no refusal) — needs PI confirmation at Gate 4 |
| 15 Nov (Claude, applying V0.4) | D13–D16/DP04 excluded from D; calendar and time-contradiction items retained, disclosed as "conventional" |
| 15 Nov 17:45 (open, PI decision 10) | Scope of "plausibly confusable": A strict name rule as applied (21/2); B narrow rule restoring 11 pairs (28/4); C rebase five D items to admit five replacement pairs |

## 6. Deviations

| # | Date | Deviation | Disclosure |
|---|---|---|---|
| 1 | 14 Nov | Independent checker replaced by Qualam | every report |
| 2 | 15 Nov | Run-1 log lost; full re-run | every report |
| 3 | 15 Nov | Human spot-check replaced by AI adjudication + AI adversarial review | every report |
| 4 | 15 Nov | Archive snapshots not saved; organiser lists captured and hashed instead | every report |
| 5 | 15 Nov | Sample reduced 32→21 main (V1.0: 23), 6→2 pilot (V1.0: 4); D 16→12 main, 4→3 pilot | every report |
| 9 | 15 Nov 19:20 | Sample 32 → 31 (or 30) main pairs by PI decision 11; distractor rule unchanged | every report |
| 8 | 15 Nov 17:55 | Four replacement pairs added by A2 without their Qwen token/distractor checks; freeze blocked until the Modal validate stage runs | A2 |
| 7 | 15 Nov 17:45 | Nine PI-proposed replacement pairs initially rejected (superseded for R02, R05, R06, R10 by A2): R01, R09, R12 by the name rule; R02, R04, R05, R06, R10, R11 by integrity (B event duplicates a pilot item or a D base event). Gemini's PASS verdicts came without sources and were not relied on | ledger |
| 6 | 15 Nov | Validation code and Qwen weights on the PI's Mac not reachable; pipeline rebuilt in the cloud workspace and tested on a toy model; real-model validation deferred to Modal GPU | Gate 3 report |

## 7. Engineering record (Gate 3)

**Rebuilt pipeline** (`pipeline/exp2/`): config (all fixed constants), prompts (three-shot/no-shot/knownness), measure (entropy, candidate scoring, knownness class, rejection preference), analysis (bootstrap, exact/MC sign-flip permutation, two-sample, Holm, M2 grouping, inconclusive rules), backend_hf (HF backend with padded-vocab stripping, manual-verified sequence scoring, explicit generation overrides, inherited config logged), run (integrated runner writing raw results before analysis), `modal_run.py` (GPU runner that pins the revision, hashes every checkpoint file, checks the tokenizer hash prefix recorded in the dataset, and runs the same code).

**Deterministic tests, 20/20 passed (15 Nov 17:30 CET, Python 3.13.18, torch 2.15.0, transformers 5.23.0, numpy):** entropy on uniform / one-hot / two-point distributions; padded vocabulary rows ignored; numerically stable log-softmax; prompt ends immediately after "A:", demos identical across conditions and free of refusal wording; bootstrap recovers a known effect and is seed-reproducible; permutation test exact for n ≤ 24 (verified p = 2/8 on a 3-point case; 2²³ patterns enumerated), Monte-Carlo branch above; two-sample test; Holm; M2 normalisation and grouping (cap log₂10 verified); inconclusive-rule logic. Toy-model backend tests: sequence log-probability equals a manual token-by-token sum; entropy equals an independent torch computation; knownness classification returns both formulation flags; sampling is seed-reproducible and greedy is fixed; rejection preference finite; padded rows present in the model and stripped.

**Integrated cold run (toy random-weight model):** V1.0 candidate, main split 23 pairs; re-run on V1.1 (21/2) and at 17:58 on V1.2 (32 pairs, 4 pilot pairs, 12 A, 12 D; exact permutation over 2^24 patterns) + 12 A + 12 D (70 questions), pilot 4 pairs; every measurement produced for every item; analysis JSON complete, exact permutation on 2²⁰ patterns for the 20 toy-"Unknown" pairs; inconclusive-condition checks evaluated. **These numbers are noise from random weights and establish only that the code runs end to end; they say nothing about Qwen.**

**Not executed (model-dependent, blocked):** correct-checkpoint verification, tokenizer hash, logits extraction on Qwen, cross-check of the Mac numpy forward pass against HF (`ref_check.py`), the Qwen validation of V1.0 items (unchanged since V0.6 for B/C; D changes do not touch Qwen checks). Reason: no Qwen weights or GPU reachable from the workspace; `api.modal.com` not on the workspace allowlist and no Modal token present.

**Failed checks (real model, 15 Nov ~19:00, Modal `validate` run on the PI's Mac):** distractor selection for the A2 replacement pairs: R02 Kyoto 0/3, R05 Sydney 2/3, R06 Vienna 0/3 cities met equal-token + ±1 nat; R10 Hyderabad passed. Engineering response (19:10): pools expanded within the recorded V0.7 distractor rule (Kyoto 10→38, Sydney 10→22, Vienna 10→43; Hyderabad unchanged), screened mechanically by `screen_pools.py`. The 17:50 pools themselves broke the recorded rule (Munich is an A answer; Adelaide, Hobart, Kobe are first names; Darwin carries a botanist-surname confound in a botany item); those five removed. Selection still uses only the V0.4/V0.5 criteria (equal Qwen tokens, |Δ| ≤ 1 nat under "The city of", closest first); pools were fixed before the re-run, as in V0.5's replacements.

**Gate 3 corrections (19:35–20:30):** 16 implementation defects fixed (15 from the Qualam review, 1 found while fixing: the coding lookup differed between stages). 42/42 deterministic and toy tests pass, with one regression test per defect. NumPy/HF comparison saved as evidence. Toy cold runs on V1.2 complete; integrity condition 5 correctly flags the four unvalidated replacement pairs. Record corrections: "every measurement" (cold run) overstated; "no pool city meets" (Sydney) wrong, Wellington met the rule; "128 scores" = 73 distinct cities. Details and the V0.4 comparison in the change log.

**Regression (19:57, Gate 3 on Modal: `torch.OutOfMemoryError`, A10G 22.08 GiB):** `modal_run.py` loaded Qwen once for the Gate 3 checks, and `exp2.run.main` then loaded a second copy; two float32 copies (~12.4 GB each) exceed the card. The second copy was unnecessary; the pilot and main stages had the same defect. Fix (20:05): the runner accepts the already-loaded model; `modal_run.py` has exactly one model load, reused by every stage. Same revision, float32, measurements and protocol. Regression tests: one load in `modal_run.py`, both runner calls pass the model; the runner never loads when given one. 46/46 pass. GPU unchanged. Gate 3 has not passed.

**Regression (19:49, found by the PI on the first Modal run of the corrected pipeline):** the new stage dispatcher did not register `validate`, so `modal run ... --stage validate` raised ValueError before any GPU work. Cause: the stage-lock correction (A3) was tested for gate3/pilot/main only. Fix (19:55): `validate` registered with scope main+pilot; `exp2.run` rejects it explicitly (it takes no measurements); regression test asserts every stage dispatched in `modal_run.py` is registered. 44/44 tests pass. No protocol or dataset change.

**Second Modal `validate` (19:16):** R02 Kyoto 0/3, R05 Sydney 1/3, R06 Vienna 1/3; nothing written (correct). Diagnosis from the dataset's own V0.5/V0.6 Qwen records (same "The city of" scorer): Vienna is 1 token at -5.98 nats, among the most prominent answers; most one-token European cities score -7 to -9.5, so the binding constraint is the ±1 nat window, not tokens. The only recorded cities inside the window are Kiev (+0.06), Istanbul (-0.51) and Venice (-0.91), the validated triple already used for Vienna in M13-B and M31-B. Kiev was missing from the pool, and Istanbul had been screened out wrongly: PI decision 6 concerns its anachronism for 1903-1908 items, not a 2005 event. Fix (19:25): screen made year-aware; Kiev and Istanbul added. Kyoto: the V0.6 change log records the identical failure ("Kyoto: no Japanese candidate within ±1 nat"; P01 replaced), so R02 is very likely unsatisfiable under the main-item rule; PI decision needed after the re-run. Sydney: no recorded score; awaiting validate.json.

**Modal `validate` output analysed (19:35; file `validate_run2_1916.json`, run with the first pool fix):**
- *Gate 3 cross-check:* the 128 prominence-score pairs (73 distinct cities; corrected 20:30) shared with the dataset's V0.5 records (custom numpy forward pass) agree with the HF/Modal scores to within 0.00035 nats, and every Qwen token count is identical. This is the pending `ref_check.py` item. All 28 existing main pairs and 4 pilot pairs still pass the token and distractor rules on the real model.
- *Vienna (R06):* the binding constraint is the ±1 nat window (22 same-token cities, only Venice inside). The same run scored Kiev (+0.057) and Istanbul (−0.515) for Vienna in M13/M31, so the 19:25 pool fix yields Kiev, Istanbul, Venice deterministically.
- *Kyoto (R02):* both constraints. Kyoto is one token at −5.17 nats; 34 of 38 East Asian candidates are 2+ tokens, and the four one-token cities fall outside the window (closest: Shanghai −1.21). Fix (19:35): pool widened to continent level (Asia), as the dataset's own AFR, EU and NA pools already are; period-correct names for 1990 (Bombay, Calcutta). Kobe remains excluded.
- *Sydney (R05):* the ±1 nat window. Sydney is one token at −7.14; Wellington (−0.06) is the only Oceania city inside. The next ones are Canberra (−1.38) and Perth (−1.42). The cities likely to fit are excluded by existing rules: Melbourne and Brisbane are congress hosts; Adelaide and Hobart are first names. Within the recorded rule, R05 cannot pass. PI decision required.
- *apply_validate.py:* added `--exclude R05` (or R02) so a PI decision to drop a pair is applied explicitly and recorded in the row; without it the script stays strict.

**Attention-mask warning (19:25):** raised by `generate()` because no attention_mask was passed and Qwen's pad token equals its EOS token. All sequences are single and unpadded and never contain EOS, so the implied mask is all ones. M1/M3/validate scores use plain forward passes, which are unaffected; greedy and sampled generations are unaffected. No measurement changed. Fix: explicit all-ones masks in every forward and generate call; verified identical logits with and without the explicit mask (toy model).

**Engineering bug fixed (19:10):** `apply_validate.py` saved the output workbook before running its checks, so a failing run still produced a file. Now all checks run first; on any failure nothing is written and the script exits 2; it also refuses to overwrite its input. Verified on synthetic pass/fail inputs (code check only).

**Earlier deterministic tests:** none failed. **Engineering corrections:** 1 — torch could not be installed from the PyTorch index (proxy 403); installed from PyPI instead.

## 8. Gate status

| Gate | Status |
|---|---|
| 1 Design review | complete (14 Nov) |
| 2 Dataset | V1.0 candidate built; ledger, evidence, manifest ready; not frozen |
| 3 Engineering validation | code-level checks complete; **Qwen-level checks pending Modal run** |
| 4 Operational freeze | **not reached**: needs Gate 3 Qwen checks, demonstration confirmation, archive decision, PI signature |
| 5 Pilot | not started |

## 9. Gate 4 freeze record (15 Nov 2026)

- **Gate 3 on real Qwen: PASS** (Mac file time 20:03 CET), on the A10G, 14/14 checks, end-to-end 3 pilot items with no integrity failures, dataset sha256 `1d3552f2…bfd5de`. Two regressions found on the way and fixed before the pass: `validate` stage not registered; two model copies resident (OOM). Record: `evidence/gate3/`.
- **Timestamp correction:** engineering entries above written in the workspace carry approximate clock times (for example "20:30", "20:05") that do not match the Mac clock. Where they conflict, the Mac file times in `docs/GATE4_FREEZE.md` are authoritative.
- **Gemini Gate 4 review: CONDITIONAL** (as reported by the PI). The review text is **not in this archive**.
- **Freeze** executed by Claude (engineering) on PI instruction. Canonical files and hashes: `MANIFEST.sha256`. No hypothesis, measurement, sample, threshold, control or analysis rule changed.

## 8. Engineering corrections for the pilot (16 Nov 2026, Claude; branch `pilot-prep-2026-11-16`; no scientific change)

Found while checking pilot readiness against the frozen code at `gate4-freeze-2026-11-15`:
1. `pilot`/`main` reported **PASS even when the runner logged integrity failures** (only `gate3` checked them). Now any integrity failure or runner exception sets FAIL (exit 1).
2. `pilot`/`main` did **not enforce the frozen dataset hash** (`--expected-sha` was optional). Now required and checked against the Gate 4 hash; a mismatch stops before any measurement.
3. On failure, `pilot`/`main` now **return every file** instead of withholding them (failures are observations); `gate3`/`validate` behaviour unchanged.
4. Installed package versions are recorded in the stage record (ENVIRONMENT.md "known reproducibility risk"; image not rebuilt).
Five regression tests added; suite 51/51. Hypotheses, measurements, sample, controls, thresholds and analysis untouched.

## 9. Gate 5 pilot and closure (16 Nov 2026)
| Time (CET) | Entry |
|---|---|
| 07:54 | PI authorises the pilot (Modal A10G, frozen configuration). |
| 08:01–08:03 | Pilot run `ap-fU9IM0saA4YsTnq4XNkAS7` on NVIDIA A10G, commit `5db0e05`. PASS; no integrity failures; 12/12 shared items bitwise identical to Gate 3. Estimated cost $0.023 (billed amount not yet read). |
| 08:14 | PI: M4 adjudication of P06-C via blind Gemini; frozen M2 analysis unchanged. |
| 08:17 | Gemini blind coding of 30 rows received (pasted by the PI; model and version unrecorded). category6 agreement 29/30, κ 0.90. |
| 08:21 | **PI Decision 13:** Gate 5 CLOSED — PASS; P06-C = FABRICATED_OR_INCORRECT; second-rater requirement satisfied; limitations retained; Gate 6 not authorised. |

## 10. Gate 6 main run and review (16 Nov 2026)
| Time (CET) | Entry |
|---|---|
| 08:31 | Pre-launch checks (Claude): dataset hash, `pipeline/` vs freeze tag (engineering guards only), `run_main.command` identical to the bundle copy, no `modal_out/main/`. All pass. |
| 08:33 | PI authorises the Gate 6 main run under the frozen configuration. |
| 08:37–08:41 | Main run `ap-2j3QT7VD8SPdnIPWPOInwI`, one run, exit 0, commit `5db0e05` (pipeline identical to `9be369f`). 84 items; no integrity failures; runner error null. Device reported **"NVIDIA A10"** (requested A10G). Estimated cost $0.072 (billed amount not read). |
| 08:47 | Claude's first-coder codes for the four UNMATCHED M4 rows and the D03 flag sealed before any second rating. |
| 08:52–08:54 | Two 30-row ratings pasted (Gemini, Grok) were of the pilot packet; not imported. |
| 08:58 | Gemini blind rating of the 168-row main packet received; category6 163/168, κ 0.92. |
| 09:03 | **PI Decision 14:** Grok added as supplementary blind rater; Gemini remains of record. Grok's 168 rows: category6 identical to Gemini's on every row. |
| 09:05 | **PI Decision 15:** five M4 codes adjudicated (M23-C, D10, D03 no-demo FABRICATED_OR_INCORRECT; D02 no-demo NONANSWER; D03 three-shot CORRECT_REJECTION). Frozen raw codes unchanged. |
| 09:18 | Qualam Gate 6 integrity review (existing chat, PI-confirmed free of the day's results): CONDITIONAL PASS; statistics independently reproduced; P1 inconclusive confirmed; five wording/provenance corrections, applied. Correction 1 was a stale report in the review packet (Claude upload error). |
| 09:21 | **PI Decision 16:** 9A GPU "hardware identity unresolved", no rerun; 9B post hoc series breakdown retained as a labelled exploratory limitation. |
