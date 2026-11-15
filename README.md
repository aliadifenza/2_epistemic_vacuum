# AlignedLab — Experiment 2: The "I Don't Know" Vacuum Test

**PI:** Dr. Ali A. Di Fenza · **Scientific coordinator:** Qualam (GPT-6) · **Engineering:** Claude · **Independent reviewer:** Gemini/Grook
**Status (15 Nov 2026): Gate 4 freeze. Pilot and main experiment NOT authorised.**

## Question

The PI's hypothesis: a base language model is truth-indifferent, because its space of continuations has no "gaps or cliffs". It cannot natively register "I don't know". Experiment 2 asks whether Qwen2.5-3B Base nevertheless shows a measurable boundary between two kinds of question:

- questions about a **real event it does not know** (B), and
- matched questions about a **plausible event that never happened** (C).

## Design (Protocol V0.4, PI-approved 14 Nov 2026; authoritative)

- **Items:** matched B/C pairs built on named international congress series (ICM, IBC, IGC). Familiar-answer controls (A) and impossible-premise items (D).
- **M1:** first-token entropy (bits), three-shot and no-demo formats.
- **M2:** semantic entropy over 10 samples.
- **M3a:** knownness of each B item (paraphrases vs three matched distractor cities).
- **M3b:** rejection preference ("No such event ever took place." vs "It was").
- **M4:** coded greedy answers, with a second rater.
- **Hypotheses:**
  - P1: H(C) − H(B) on Unknown pairs, with a floor of 10 pairs.
  - P2: C vs A.
  - P3: rejection preference C vs B, two-sided.
- **Analysis:** bootstrap and sign-flip tests, Holm over P2/P3, and five pre-registered inconclusive conditions.

The full protocol is in `protocol/`, together with the original Research Agenda; both are authoritative.

## Frozen sample

`dataset/AlignedLab_Experiment_2_Dataset_V1_2_QWENVALIDATED.xlsx` (sha256 `1d3552f2e5aa325cd1590d8b73b2968825d9838788c944e89a631f66ecbfd5de`):

| Split | B/C pairs | A | D |
|---|---|---|---|
| main | 30 | 12 | 12 |
| pilot | 4 | 4 | 3 |

R02 (Kyoto) and R05 (Sydney) are excluded by PI Decision 11.

## Model

Qwen/Qwen2.5-3B, revision `3aab1f1954e9cc14eb9509a215f9e5ca08227a9b`, float32, Modal A10G.

## Layout

| Folder | Contents |
|---|---|
| `protocol/` | Protocol V0.4, original Research Agenda, Independent Verification Protocol, Amendment A2, Section 7 additions |
| `dataset/` | Frozen dataset; `history/` holds V0.7 → V1.2 candidates and verification logs |
| `pipeline/` | Frozen code and tests (`modal_run.py` is the entry point) |
| `evidence/` | Gate 3 (real Qwen), validate, NumPy/HF reference check, test results, toy cold run (code paths only, not evidence about Qwen), source captures |
| `reviews/` | Adversarial, Qualam and earlier Gemini reviews. The Gemini Gate 4 review is missing (see the file there) |
| `decisions/` | Decision/deviation log, Gate 3 corrections change log |
| `docs/` | Gate 4 freeze record, reproducibility guide, environment, handoff |

`MANIFEST.sha256` lists every file. Verify with `shasum -a 256 -c MANIFEST.sha256`.

## Integrity rules

- AI review is never presented as human verification.
- Negative results, AI errors and deviations are preserved.
- No scientific change without PI approval.

## Gate 4 archival update (15 November 2026)

The original freeze remains at tag `gate4-freeze-2026-11-15`. Gemini's conditional review and PI Decision 12 have since been added. See `docs/GATE4_CLOSURE_2026-11-15.md` for the verified archival status and accepted limitations. Pilot and main experiment are **not authorized**.
