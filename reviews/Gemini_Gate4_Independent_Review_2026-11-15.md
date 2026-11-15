# Independent Gate 4 Scientific Review — Experiment 2

**Reviewer:** Gemini (independent scientific reviewer)  
**Date:** 15 November 2026  
**Source:** Review text supplied by the PI in the AlignedLab conversation on 15 November 2026. This file is a structured preservation of its substantive findings; it is **not independently authenticated against a Gemini export** and is **not a claim of a verbatim transcript**.

## Executive verdict: CONDITIONAL

Gate 3 passed and is accepted as **engineering evidence only**. Protocol V0.4, the current pipeline, and dataset V1.2 QWENVALIDATED (after PI Decision 11 exclusions) are sufficiently specified to freeze **if the PI explicitly accepts residual verification-process risks and confirms the outstanding demonstrations**. Passing technical checks alone does not establish scientific fidelity.

## Checklist findings

- **P1–P3: PASS [HIGH].** Original hypotheses, definitions, controls and statistical analyses preserved. Primary estimand: mean delta = H(C) − H(B), Unknown matched pairs only. Seeded 10,000-replicate bootstrap and exact/Monte Carlo sign-flip tests; Holm correction for secondary tests; no equivalence margin.
- **M1, M2, M3a, M3b, M4 and question surprisal: PASS [HIGH].** First-token full-distribution float32 Shannon entropy; discrete semantic entropy from 10 samples (T=1, top-p=1, stop at newline, per-item seeds); two independent knownness paraphrases, strict ranking and ties handled; rejection preference R1/S1 primary, R2/S2 robustness; six-category greedy coding with second-rater path; surprisal on exact M1 prompt.
- **Divergences: CONDITIONAL [MED].** Most substantive changes explicitly documented and PI-authorized, including Amendment A2, Decision 11 and sample reductions; verification-process deviations remain material.
- **R02 Kyoto, R05 Sydney: PASS [HIGH].** Excluded after real-Qwen distractor matching failure. Final main n=30 matched B/C pairs, consistent with ledger and hash.
- **At least 10 Unknown pairs: PASS as an interpretation condition [HIGH].** An inconclusive-result rule, not a pre-run sample-size guarantee; do not relax.
- **Amendments/deviations: PASS [HIGH].** Decision/deviation log, A2, Section 7 additions, Gate 3 change log and verification log present.
- **Reproducibility: PASS [HIGH].** Qwen revision `3aab1f1954e9cc14eb9509a215f9e5ca08227a9b`; float32, full logits, tokenizer hash, dataset and file hashes, seeds, configuration overrides and Gate 3 records. The review describes Gate 3 as 15 named checks; the frozen engineering record describes 14/14. Both claims are preserved without silently resolving the discrepancy.
- **Scientific freeze: CONDITIONAL [MED].** Requires PI risk acceptance and demonstration confirmation.
- **PI authorization: PASS with caveat [MED].** V0.4 authoritative. Independent proof of approval of the specific `Exp2_Research_Agenda_Original.docx` file not established; agenda used as historical source.
- **Gate 3 diagnostic: PASS, correctly scoped [HIGH].** Three pairs, zero Unknown; cannot infer main Unknown rate or primary estimand.

## Material risks reported

**C-item fictionality verification:** Planned independent/human verification including a 10% human spot-check was replaced by Qualam full verification, Claude adjudication and Claude adversarial review; there were zero human row verdicts. Risk: possible systematic bias/circularity in the primary plausible-fiction condition. Recommendation: PI accepts disclosed risk or commissions a human check.

**Source archival completeness:** Organizer chronologies hashed; most additional evidence URLs not archived due to Wayback access failure. Auditability weaker than planned. Recommendation: accept and disclose, or archive decisive sources.

## Other conditional points and minor limitations

- Lima, Nairobi and Agra fixed demonstrations were marked as needing PI confirmation at Gate 4.
- Original agenda filename/hash or dated approval record was not independently established; V0.4 remains authoritative.
- Named-series/confusability interpretation evolved before A2 and was PI-authorized.
- Sample 32 to 30 matches approved exclusions. Repeated cities and prominence imbalance disclosed.
- D calendar/time contradictions retained as conventional, while pure 'no city' items dropped.
- Main run remains unauthorized; Gate 3 covered only three diagnostic pilot pairs.

## PI decisions sought in review

1. Accept or remediate AI-only verification process risks.
2. Confirm the three fixed demonstrations: Lima / Nairobi / Agra.
3. Optionally confirm the exact original agenda file; alternatively declare V0.4 the sole authoritative specification.

## Final recommendation

The experiment is **not ready for unconditional freeze or pilot authorization** until the PI explicitly accepts the verification-process risks and confirms the fixed demonstrations. There is **no unapproved change** to the central hypotheses, primary estimand or analysis rules. Gate 3's zero-Unknown diagnostic is neither support nor refutation of the main design.

## Epistemic provenance

The reviewer independently verified code–protocol alignment, dataset exclusion status, Gate 3 technical record, presence/content of deviation logs, and the 10-pair inconclusive rule. The adjudication rationale, timing of PI decisions, and assertion that all 16 implementation corrections were approved were **reported by Claude/Qualam**, not independently established in this review.

**See** `decisions/PI_DECISION_12_2026-11-15.md` for the PI's subsequent resolution of these conditions. This review's original CONDITIONAL verdict is preserved, not retrospectively changed to PASS.
