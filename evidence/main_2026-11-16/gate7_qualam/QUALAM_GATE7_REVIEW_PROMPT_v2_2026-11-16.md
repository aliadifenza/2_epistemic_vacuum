# Qualam — Gate 7 methodology review (Experiment 2)

Gate 7 is executed. Please conduct the scientific-methodology review. Work only from the attached `QUALAM_GATE7_PACKET_v2_2026-11-16.zip` (different from the two Gate 6 packets). Your round-2 Gate 6 confirmation (corrections 1–5, CANNOT VERIFY items) is still open; if you have not sent it, include it at the top of your reply.

Start with the original plan (`protocol/Exp2_Research_Agenda_Original.docx`, `protocol/Exp2_Protocol_V0_4_Approved.docx`, Amendment A2), then `docs/GATE7_ANALYSIS_REPORT_2026-11-16.md`, then the evidence in `evidence/main_2026-11-16/gate7/` and the script `analysis/gate7/gate7_analysis.py`.

Check, each with PASS / FAIL / CANNOT VERIFY and evidence:
1. **Fidelity to V0.4 §6–7:** every pre-registered analysis present and computed as specified (paired differences, 10,000-resample percentile bootstrap, sign-flip tests, P2 two-sample procedure, Holm across P2/P3, five inconclusive conditions); no procedure changed.
2. **Reproducibility:** the script uses only frozen Gate 6 outputs and the frozen analysis functions; reported numbers match the tables and `analysis.json`.
3. **Evidence labelling:** pre-registered, descriptive, exploratory and interpretive statements are kept apart; nothing exploratory is presented as confirmatory; no interpretation is attributed to the PI.
4. **Completeness:** condition summaries, behavioural frequencies, Istanbul supplementary, robustness checks, uncertainty assessment, null/negative/unexpected findings and limitations all present.
5. **Figures:** each figure is faithful to the data and correctly labelled.
6. **Decisions for the PI** (report §5): are they the right ones, and is anything missing?

Return: a table of the six checks, a numbered list of required corrections (if any), and your recommendation to the PI on whether Gate 7 can pass. Be concise.
