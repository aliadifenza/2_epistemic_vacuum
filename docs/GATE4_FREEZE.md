# Gate 4 freeze record — 15 November 2026

Executed by Claude (engineering) on the PI's FREEZE instruction. No hypothesis, measurement, sample, threshold, control or analysis rule was changed. Pilot and main experiment are **NOT AUTHORISED**.

## 1. Implementation verified on the PI's Mac (`~/AlignedLab/exp2_v12/pipeline`)

Read directly from the Mac copy on 15 Nov. Every `.py` and `.json` file in it is byte-identical to the engineering workspace copy.

| Correction | What the Mac copy shows | Evidence |
|---|---|---|
| Stage dispatch | `stages.py` registers `validate` (main+pilot), `gate3` (pilot), `pilot`, `main`; `modal_run.py` dispatches exactly those four; `exp2.run` rejects `validate` | regression tests `test_every_modal_stage_registered`, `test_run_rejects_validate_stage` |
| Model loading | exactly one `HFBackend.load` in `modal_run.py`; both runner calls pass `backend=be` | regression tests `test_single_model_load_in_modal_run`, `test_runner_reuses_supplied_backend` |
| GPU execution | `gate3` PASS on A10G, 67.7 s, estimated $0.021, no OOM | `evidence/gate3/gate3_record.json` |

## 2. Real-Qwen Gate 3 (Mac file time 20:03 CET)

**Status: PASS.** 14/14 checks, no failures:

- checkpoint revision; tokenizer sha256; vocabulary padding (151 665 / 151 936 / 271);
- finite logits; entropy range;
- bitwise-identical repeat logits; equal repeat sequence log-probabilities;
- greedy " Paris" for the capital of France (p = 0.68);
- attention mask: forward pass and greedy output identical with and without it;
- no padded tokens generated; seeded sampling reproducible; newline stopping;
- explicit generation configuration.

End-to-end run on 3 pilot items (with M2): integrity failures = none. Coding lookup sha256 `d1456fe9…`, the same table as every stage. Dataset sha256 checked at run time: `1d3552f2…bfd5de`.

## 3. Dataset provenance

- **`validate`** (Mac 19:54) ran on V1.2 CANDIDATE, sha256 `42df54a2…058b`, which the run checked:
  - all 36 pairs pass token matching;
  - every pre-existing distractor set passes;
  - Vienna pool → Kiev, Istanbul, Venice;
  - Hyderabad pool → Chennai, Bangalore, Mumbai;
  - Kyoto → none (0/3); Sydney → Wellington only (1/3).
- **`apply_validate.py --exclude R02 R05`** (PI Decision 11) produced QWENVALIDATED (Mac 19:55).
- **Cell-level diff, CANDIDATE vs QWENVALIDATED:** exactly the 8 rows R02/R05/R06/R10 B and C changed; nothing else.
- **Frozen composition:** main 30 B/C pairs, 12 A, 12 D; pilot 4 pairs, 4 A, 3 D. No included pair has a pending distractor.

## 4. Hash verification

| File | Recorded by PI | Computed on the Mac | Computed in the archive |
|---|---|---|---|
| Dataset QWENVALIDATED | `1d3552f2…bfd5de` | identical | identical |
| `Exp2_Gate3_evidence_2026-11-15.zip` | — | `ff3ae308…f8ab` | identical |

The full manifest is `MANIFEST.sha256`, verified with `shasum -a 256 -c` after the final commit.

## 5. Deterministic suite at freeze

46/46 pass, run inside this repository's layout (`evidence/tests/deterministic_suite_freeze.txt`).

The only change to the frozen code in this repository: two test files now locate their fixture data through `tests/_paths.py`, so the tests run in the repository layout. Pipeline modules are unchanged from the Mac copy that passed Gate 3.

## 6. Missing evidence (not reconstructed)

1. **Gemini Gate 4 review** (reported CONDITIONAL): the text is not in any location available to engineering. See `reviews/GEMINI_GATE4_REVIEW_MISSING.md`.
2. **PI Decision 12, full written text** (residual verification risks accepted): only the PI's one-line statement is recorded. The list of accepted risks is not in the archive.
3. **Human 10 % spot-check** of the dataset verification: not performed (already disclosed as a deviation in the log).
4. **Raw Modal console logs** for validate and gate3: not saved; the JSON records are the evidence.

## 7. Records corrected at freeze

- Decision numbering: the 19:32 methodological clarifications had been logged as "PI decisions 12–15". They are relabelled C1–C4, because the PI numbers the risk-acceptance decision as Decision 12. Content unchanged.
- Engineering timestamps written in the workspace were approximate. The Mac file times above are authoritative.
- `pipeline/MAC_RUNBOOK.md` and `RERUN.md` on the Mac are superseded by `RUN_GATE3_ON_MAC.md` and `docs/REPRODUCIBILITY.md`. They are not copied into the repository and remain on the Mac.
