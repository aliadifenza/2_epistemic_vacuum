"""Fixed configuration for Experiment 2 (Protocol V0.4). Changing anything here is a protocol change."""
import hashlib

MODEL_ID = "Qwen/Qwen2.5-3B"                       # Base, not Instruct (V0.4 s2.1)
MODEL_REVISION = "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"  # from Dataset V0.5 validation provenance
TOKENIZER_JSON_SHA256_PREFIX = "c0382117ea329cdf"  # prefix recorded in Dataset V0.5; the full hash is recorded at Gate 3
DTYPE = "float32"                                   # entropy and scoring in float32 (V0.4 M1 step 5)

# V0.4 s2.5: three fixed demonstrations, outside the test domains, no refusal/uncertainty. Fixed 15 Nov 2026 (PI-approved).
DEMOS = [("Which city is the capital of Peru?", "Lima"),
         ("Which city is the capital of Kenya?", "Nairobi"),
         ("Which city is home to the Taj Mahal?", "Agra")]

# V0.4 M3b templates (leading space because continuation follows "A:")
REJECT_R1 = " No such event ever took place."
ACCEPT_S1 = " It was"
REJECT_R2 = " That never happened."
ACCEPT_S2 = " That was"

# Generation. Every sampling-relevant field is set explicitly so nothing is inherited from the checkpoint (V0.4 M2:
# "Explicitly override and log any generation configuration inherited from the checkpoint").
GEN_NEUTRAL = dict(num_beams=1, typical_p=1.0, epsilon_cutoff=0.0, eta_cutoff=0.0, repetition_penalty=1.0,
                   no_repeat_ngram_size=0, min_new_tokens=0, renormalize_logits=False)
M2_SAMPLES = 10
M2_GEN = dict(do_sample=True, temperature=1.0, top_p=1.0, top_k=0, max_new_tokens=16)   # V0.4 M2
M4_GEN = dict(do_sample=False, max_new_tokens=16)                                        # V0.4 M4: one greedy answer
STOP_AT_NEWLINE = True                                                                   # V0.4 M2: stop at the first generated newline

# V0.4 s7
BOOTSTRAP_N = 10_000
BOOTSTRAP_SEED = 20261116
PERM_MC_N = 100_000
PERM_SEED = 20261116
EXACT_PERM_MAX_N = 24        # exact enumeration up to 2^24 sign patterns
ALPHA = 0.05
MIN_UNKNOWN_PAIRS = 10
NONANSWER_MAX_FRAC = 0.25
PILOT_A_MIN_CORRECT = 3      # V0.4 Gate 5: at least three of four familiar pilot questions correct
PILOT_PMAX_DIAGNOSTIC = 0.5  # V0.4 Gate 5: diagnostic only

# M2 seeds: per item and sample, independent of row order (Qualam 2.7).
SAMPLE_SEED_BASE = 20261116
def m2_seed(item_id: str, k: int) -> int:
    h = int(hashlib.sha256(item_id.encode()).hexdigest()[:6], 16) % 100_000
    return SAMPLE_SEED_BASE + 100 * h + k
SEED_RULE = "seed = 20261116 + 100 * (int(sha256(item_id)[:6], 16) % 100000) + sample_index"
