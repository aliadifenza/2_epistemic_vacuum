# Environment and model specification (as recorded by the Gate 3 run)

## Model

| Field | Value |
|---|---|
| Model | Qwen/Qwen2.5-3B (Base) |
| Revision | `3aab1f1954e9cc14eb9509a215f9e5ca08227a9b` (checked against `config._commit_hash`) |
| Precision | float32 |
| Tokenizer | `tokenizer.json` sha256 `c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539` |
| Vocabulary | 151 665 tokens; LM head has 151 936 rows (271 padded rows, masked to −∞ in generation) |

The sha256 of every checkpoint file, including both safetensors shards, is in `evidence/validate/validate_record.json` (`file_sha256`). The weights are **not** stored in this repository.

## Runtime (Modal)

- **Image:** `debian_slim`, Python 3.12.10.
- **Pinned packages:** torch 2.5.1+cu124, transformers 4.46.3. Accelerate, numpy, scipy, safetensors, huggingface_hub and openpyxl are unpinned; the numpy version actually used is recorded in each `run_meta.json`.
- **CUDA:** 12.4.
- **GPU:** A10G (24 GB).
  - `gate3` recorded device name "NVIDIA A10G".
  - `validate` recorded "NVIDIA A10". Both runs requested the same GPU type, so the difference is the reported device name only.
- **Determinism settings:** TF32 matmul off, deterministic algorithms on, `CUBLAS_WORKSPACE_CONFIG=:4096:8`.
- **Modal builder workaround:** run with `MODAL_IMAGE_BUILDER_VERSION=2025.06` in the shell environment. It is not set in the code.

## Attention-mask warning and equivalence check

Transformers warns when `generate` is called without an `attention_mask`. The pipeline now passes an explicit all-ones mask on every forward and generation call. All sequences are single and unpadded, so this should change nothing. That was first argued, then **tested on Qwen** in Gate 3 on three sanity prompts:

| Check | Result |
|---|---|
| `mask_forward_identical` | max absolute logit difference with vs without the mask = 0.0, 0.0, 0.0 |
| `mask_greedy_identical` | greedy outputs identical on all three prompts |

## Known reproducibility risk

The unpinned secondary packages could resolve to newer versions if the Modal image is rebuilt. Recommendation for the pilot run, which needs no PI decision: before the pilot, pin them to the versions installed in the cached image and record them in the run manifest.
