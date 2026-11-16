# AlignedLab — Experiment 2: The "I Don't Know" Vacuum Test

**A preregistered feasibility study of plausible fiction, obscure fact, and uncertainty in a base language model**

**Principal investigator:** Dr. Ali A. Di Fenza (AlignedLab, Berlin)  
**Research collaborators:** Qualam (ChatGPT/GPT-6: scientific coordination and methodological review), Claude (engineering and analysis), Gemini and Grok (AI review and behavioral rating). The PI retained scientific authority and interpretation.  
**Status — November 16, 2026:** Main experiment complete; Gate 7 analysis and Gate 8 independent AI critiques complete. **Primary test formally inconclusive.** Gate 9 reporting and public evidence archive in progress.

## Why this experiment exists

This work belongs to *Aligning Latent Spaces: From Possibility to Power*. Its philosophical starting point is a question, **not an established finding**: might a language model's learned representations be investigated as a structured space of possibility, in which statistical proximity is not the same as historical actuality?

The provocative thesis *"Hallucination is all I have"* asks us to consider whether accurate statements and plausible inventions emerge from a shared generative process. Could that same capacity eventually be harnessed for conceptual exploration, scenario construction, or verifiable scientific discovery? This experiment does **not** test the geometry or ontology of latent space. Instead, it asks one narrow empirical question: **Does a pretrained base model express different uncertainty about plausible fictional events versus obscure real events it cannot recall?**

The point is to move from philosophical conjecture to falsifiable investigation without prematurely declaring the conjecture true.

## Design and frozen scientific authority

The authoritative operational specification is **Protocol V0.4**, together with its approved amendment and recorded PI decisions in [protocol/](protocol/) and [decisions/](decisions/). The pre-run freeze tag is \`gate4-freeze-2026-11-15\`. It must not be silently rewritten to match later interpretations.

- **Model:** Qwen2.5-3B Base, pinned revision \`3aab1f1954e9cc14eb9509a215f9e5ca08227a9b\`; float32, TF32 disabled, deterministic algorithms. A10G was requested; the runtime reported "NVIDIA A10" and exact hardware identity remains unresolved.
- **Frozen dataset:** [84 questions](dataset/AlignedLab_Experiment_2_Dataset_V1_2_QWENVALIDATED.xlsx): A = 12 familiar Olympic host cities; B = 30 obscure real congress host cities; C = 30 matched plausible fictional congress events; D = 12 impossible premises. SHA-256: \`1d3552f2e5aa325cd1590d8b73b2968825d9838788c944e89a631f66ecbfd5de\`.
- **Measures:** M1 first-token entropy (primary); M2 rule-grouped response diversity; M3a forced-choice knownness; M3b rejection-versus-acceptance continuation preference; M4 coded greedy answers.
- **Preregistered tests:** P1 paired entropy difference H(C) − H(B) on operationally Unknown B/C pairs, **inconclusive if fewer than 10**; P2 C versus familiar A; P3 paired rejection preference C versus B. Bootstrap intervals, permutation tests, Holm adjustment for P2/P3, and inconclusive-result conditions were frozen before the main run.
- The run was completed once. The study reports design failures, negative results, and post-hoc analyses as such.

## What we found

| Test or finding | Observed result | Interpretation |
|---|---|---|
| **P1 primary: Unknown B/C pairs** | Only **2** eligible pairs; mean H(C) − H(B) = **−0.24 bits**, 95% CI [−1.22, +0.75], p = 1.0 | **Inconclusive by preregistered rule**; neither confirmation, refutation, nor equivalence |
| **P2: fiction C vs familiar A** | +5.32 bits, 95% CI [4.78, 5.83], Holm-adjusted p = 0.0002 | Unmatched Olympics/congress contrast; cannot isolate truth status |
| **P3: rejection preference C vs B** | +0.13, 95% CI [−0.58, +0.84], Holm-adjusted p ≈ 0.73 | No statistically supported difference |
| **M3a validation** | Forced-choice: 23 Known, 5 Uncertain, 2 Unknown; only **4/23** "Known" free-recall answers were correct | Recognition-like candidate preference did not adequately predict free generation |
| **M4 behavior** | In 168 greedy completions, one correct rejection and one nonanswer (both D); no C rejection | Prompt-conditioned observed behavior, not proof of absent internal knowledge |
| **Post-hoc congress-series analysis** | H(C) − H(B) varied strongly with whether B or C mentioned the mathematics congress | Exploratory **association**, not an established causal mechanism |

First-token entropy was low for familiar facts and high for both obscure real and plausible fictional events. The model often generated city names even for false premises. These observations **do not** demonstrate a native boundary—or a lack of one—between actuality and possibility.

**The scientific contribution is feasibility:** a reproducible pipeline plus a diagnosis of two design faults. First, a forced-choice knownness proxy selected only two cases for the primary test despite low free-recall accuracy. Second, constructing fictional questions by changing the congress series also changed topic/lexical features. The original philosophical question remains open.

## The AlignedLab Research Spiral

The research collaboration translated between intellectual levels rather than merely delegating tasks:

1. **Philosophical direction — Ali:** concepts, questions, hypotheses, and scientific authority.
2. **Conceptual translation and scientific formalization — Ali + Qualam (ChatGPT):** predictions, measurements, controls, and falsification criteria.
3. **Technical translation, engineering, and execution — Claude:** approved protocol to code, tests, and reproducible evidence.
4. **Empirical translation and criticism — Qualam, Gemini, and Grok; interpretation — Ali:** challenge the results, return to philosophy, and refine the next hypothesis.

These are documented roles **within one research case**, not evidence that this arrangement outperforms autonomous agents or other research teams. Observed costs included repeated AI review cycles, cross-model handoffs, limited human visibility into delegated code, and verification difficulties. The human–AI system is a **second, distinct future research question**.

## Moving forward

**Experimental V2:** Validate an Unknown filter against free recall, improve event and fictionality verification, match congress series and wording rather than swapping them, use a yield-tested pilot with prospectively justified sample size, and consider another domain and model. No V2 findings are claimed.

**Human–AI collaboration research:** Study epistemic reach, human scientific understanding, coordination costs, independence, errors, and verification quality using suitable comparators. This was not a controlled outcome of Experiment 2.

## Repository and evidence

- [protocol/](protocol/) — original research agenda, approved protocol, amendment, scientific controls.
- [dataset/](dataset/) — frozen 84-item workbook and development history.
- [pipeline/](pipeline/) — frozen implementation and tests.
- [decisions/](decisions/) — PI decisions and deviations.
- [evidence/](evidence/) — pre-run diagnostics, pilot-related archives and source captures currently committed.
- [reviews/](reviews/) — earlier reviews.
- [docs/](docs/) — reproducibility and freeze records.

**Archive completeness warning:** At the time of this README update, the default branch still requires the **main-run raw evidence, Gate 7 figures and analysis files, Gate 8 reviews, and final PDF/Word report** to be fully synchronized from the original execution archive. Do not mistake the Gate 4 contents or this narrative update for a complete reproducibility deposit. The local main-run evidence and report have been verified separately; they are not represented as committed until GitHub confirms their file paths.

## Scientific integrity and AI disclosure

The PI conceived the research and approved substantive scientific choices. Claude implemented and ran the experiment; Qualam (ChatGPT) independently checked the saved statistics and contributed to writing and methods; Gemini and Grok served as AI reviewers and second raters. Reviewer independence and provenance have stated limits. No AI critique is presented as human peer review. The main P1 result remains inconclusive, and neither the experiment nor its results establish a modal ontology of latent space.

**Citation:** Di Fenza, A. A. (2026). *The "I Don't Know" Vacuum Test: A preregistered feasibility study of plausible fiction, obscure fact, and uncertainty in a base language model.* AlignedLab, Berlin.
