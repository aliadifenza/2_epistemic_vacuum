# Experiment 2 — Gate 3 corrections after the Qualam review (15 Nov 2026, 19:35–20:30 CET)

Engineer: Claude. Baseline: Protocol V0.4 and the original Research Agenda. Amendment A2 and every earlier PI decision unchanged.
No dataset change, no threshold change, no measurement substitution. Previous pipeline preserved as `pipeline_pre_qualam_fix_1935`.

**Evidence levels used below.** VERIFIED = deterministic test or computation run here. TOY = verified on the random-weight toy model only (code path, not Qwen). PENDING QWEN = will be verified by the Modal `validate` / `gate3` runs, not yet run. ASSERTED = reasoning, not tested.

## A. Implementation corrections (defects; no change in what V0.4 asks for)

| # | Qualam | Defect | Correction | Evidence |
|---|---|---|---|---|
| A1 | 1.2 | Padded vocabulary rows could be generated in M2/M4. | `MaskPaddedVocab` sets rows ≥ tokenizer length to −∞ at every generation step. With top-p 1, top-k 0, T 1 this equals sampling from the renormalised valid distribution. | TOY: test forces padded rows to dominate; raw `generate` picks them, the backend never does. PENDING QWEN: `no_padded_tokens_generated`. |
| A2 | 1.7 | Only five inherited generation fields were logged; others could be inherited. | One explicit `GenerationConfig` per kind (M2 sampling, M4 greedy) with every sampling field set; the model's own config is replaced by it before each call; full dict, checkpoint config and call settings (mask, processors, stopping) logged in `run_meta.json`. | TOY: every field asserted. |
| A3 | 1.8 | `--stage main` with the default split ran pilot items; run identity incomplete. | `stages.py`: one split per stage, no split argument; unknown stages rejected; `pilot`/`main` refuse to start without `--authorised`. `run_meta.json` logs stage, split, limit, M2 status. | VERIFIED (test). |
| A4 | 1.1, 1.3, 1.8 | Gate 3 checks were recorded but never enforced. | `gate3.py`: 15 named checks; any failure → status FAIL, Modal exits 1, only the failure record is written. | TOY: wrong revision and injected nondeterminism both produce FAIL. PENDING QWEN. |
| A5 | 3.3 | `apply_validate.py` did not check the dataset hash; missing records passed silently. | `validate.json` now carries the dataset sha256; `apply_validate.py` refuses a mismatch and requires a passing record for every included pair. | VERIFIED: hash mismatch, missing pair, short replacement each exit 2 with nothing written. |
| A6 | 4.4 | The NumPy/HF comparison output was not saved. | `refcheck_numpy_hf.py`; output in `evidence/refcheck/`. | VERIFIED: 73 distinct cities, max abs diff 0.00035 nats, no token mismatch. Scope: city prominence only. |
| A7 | 4.3 | Mask correction verified on toy only. | `gate3` compares logits and greedy outputs with and without the explicit mask on Qwen. | TOY passes. PENDING QWEN. |
| A8 | 2.6 | Holm took the Unknown-only P3 p-value; a missing test became p = 1. | Holm uses the all-pairs P3 sign-flip p-value (V0.4 §7.2); Unknown-only P3 kept as descriptive; a missing test is reported as missing. | VERIFIED (test). |
| A9 | 2.13 | Inconclusive conditions 3 and 5 were hard-coded as passing. | (3) Non-answer share of B and of C greedy answers (three-shot), with a lower bound (coded non-answers) and upper bound (plus unmatched strings awaiting adjudication); undetermined if the bounds straddle 25 %. (5) Integrity checks: dataset hash, model revision, LM-head size, unvalidated distractors, non-finite values, M2 sample count, padded tokens. | VERIFIED (tests); TOY cold run flags the four unvalidated replacement pairs under (5). |
| A10 | 2.8 | M2 grouped raw strings; no aliases, rejection, abstention or non-answer groups. | Shared coder (section B3): groups are canonical city (aliases merged), REJECTION, ABSTENTION, NONANSWER, or the exact normalised unmatched string. | VERIFIED (test). |
| A11 | 2.7 | M2 seeds depended on row order; generation did not stop at the newline. | Seed = 20261116 + 100·(sha256(item ID) mod 10⁵) + sample index, logged per sample. `StopAtNewline` stops after the token that contains the newline; raw output kept. | VERIFIED (390 distinct seeds; criterion test). TOY. |
| A12 | 2.10 | Surprisal tokenised prefix and question separately. | Tokenises the full M1 prompt once; question tokens chosen by character offsets. Grouped summary by condition and paired C−B added. | TOY: equals manual computation; identical token IDs to M1. |
| A13 | 2.4 | Knownness discarded the eight scores; ties silently favoured the answer. | All eight scores, margins and ties recorded; ties do not count as first (PI decision). | VERIFIED (stub test). |
| A14 | 3.2 | Pilot familiar-answer check not computed. | `pilot_feasibility`: ≥ 3 of 4 A items correct (greedy, three-shot); median top-token probability against the 0.5 diagnostic; undetermined while unmatched strings are pending. | VERIFIED (test). |
| A15 | 2.12 | Condition 2 flagged when no Unknown pairs existed. | Reported as undetermined (condition 1 already applies). | VERIFIED (test). |
| A16 | — (found during this work) | Coding lookup table differed between main and pilot runs. | One table per dataset file (all splits, all answers and distractors, plus pools); its hash is logged and goes into the freeze manifest. | VERIFIED: identical hash for both stages. |

## B. Approved methodological clarifications (PI, 15 Nov 19:32)

- B1. P3 is tested two-sided; the predicted direction (positive) is reported beside the estimate.
- B2. Knownness "ranks first" means strictly highest; ties do not qualify and are recorded.
- B3. One shared M2/M4 coder, built before Gate 3. It follows verification protocol §4: three fields (premise status, content class, correctness) plus V0.4's six M4 categories. Lookup table from the captured organiser chronologies plus the dataset's answers, aliases and distractors. Priority rule for mixed outputs, which V0.4 requires: non-answer test first, then denial (a denial with a city counts as a rejection with correction, as in the protocol's worked example), then abstention, then a named city, else UNMATCHED.
- B4. Second rater: Gemini, blind to the first coder's labels (`second_rater.py export` / `import`): Cohen's κ per field; disagreements and unmatched strings go to `pi_adjudication.csv` for the PI. V0.4 asks only for "a second independent rater", so Gemini is not a substitution.

**Engineering interpretations inside V0.4, for visibility (no PI decision needed unless you object):** the 1893 Chicago precursor is counted as an ICM host and Yokohama as the 1993 IBC venue in the content classes; unmatched strings are grouped by exact normalised text in M2; four Olympic aliases (Rio, Torino, München, Ciudad de México).

## C. Corrected measurements and conditions against V0.4

| V0.4 element | V0.4 requires | Implementation now | Evidence |
|---|---|---|---|
| M1 | Entropy in bits over the valid vocabulary, float32, three-shot and no-demo | Unchanged; float32 enforced on GPU (TF32 off) | VERIFIED synthetic; PENDING QWEN sanity |
| M2 | 10 samples, T 1.0, top-p 1.0, no top-k, rep. 1.0, 16 tokens, stop at newline, per-item seeds, overrides logged, grouping with distinct rejection/abstention/non-answer categories | All of these, explicitly | VERIFIED / TOY |
| M3a | Two paraphrases, three alternatives, complete-sequence scores; Known/Unknown/Uncertain | Plus strict-first rule and full score record | VERIFIED |
| M3b | R1/S1 primary, R2/S2 robustness, paired RΔ | Unchanged | VERIFIED (earlier tests) |
| M4 | Greedy answer, six exclusive categories, priority rule, second rater, κ | Coder + rater workflow; human adjudication of unmatched strings by the PI (verification protocol §4) | VERIFIED (tests); no real outputs yet |
| Surprisal | Mean −log p of question tokens, B and C separately | M1-consistent tokenisation; grouped summary | TOY |
| P1 | Unknown pairs, bootstrap 10,000, sign-flip, median, share positive | Unchanged | VERIFIED |
| P2 | C vs A, bootstrap + permutation | Unchanged | VERIFIED |
| P3 + Holm | Paired RΔ across B/C pairs; Holm over P2 and P3 | All-pairs P3 into Holm; two-sided | VERIFIED |
| §7.4 (1) | < 10 Unknown pairs | Unchanged | VERIFIED |
| §7.4 (2) | median H(A) not below median H(B-Unknown) | Undetermined when either is missing | VERIFIED |
| §7.4 (3) | > 25 % non-answers in B or C, controlled format | From coded greedy answers, with bounds | VERIFIED |
| §7.4 (4) | Formats clearly opposite in sign | Unchanged | VERIFIED |
| §7.4 (5) | Integrity or implementation defect | From the integrity checks | VERIFIED |
| Gate 5 | ≥ 3/4 familiar pilot items correct; median top-token probability vs 0.5 | Implemented | VERIFIED |

## D. Record corrections

- The 19:35 log entry said "128 prominence scores"; the saved comparison counts **73 distinct cities** (128 was the number of score pairs including repeats). Max difference 0.00035 nats stands.
- Cold-run coverage: the earlier statement that "every measurement" was produced overstated it. The toy cold run now produces every measurement and every condition, but on random weights every generated answer is unmatched, so M4, M2 grouping, condition 3 and the pilot check are exercised only as code paths.
- Sydney: the earlier wording "no pool city meets" is wrong. Wellington met the rule; no complete set of three did. Now reads "fewer than three pool cities meet".
- Attention mask: the claim that no Qwen generation changed was reasoning, not a test. It becomes a test in the Gate 3 run (A7).

## E. Verified here vs pending

VERIFIED here: 42/42 deterministic and toy tests (`results/tests.txt`); NumPy/HF comparison; toy cold runs on V1.2 main and pilot. **Not evidence about Qwen.**
PENDING QWEN (Modal on the Mac): replacement-pair distractors (`validate`); checkpoint revision, tokenizer hash, vocabulary, logits sanity, repeat determinism, mask equivalence, padded-token exclusion, seeded sampling, newline stopping, and a three-item end-to-end run (`gate3`).
Not done before the pilot by design: real M4 coding, Gemini second rating, PI adjudication.
