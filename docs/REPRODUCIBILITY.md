# Reproducibility guide

## 1. Verify the archive
```bash
shasum -a 256 -c MANIFEST.sha256          # every line must say OK
shasum -a 256 dataset/AlignedLab_Experiment_2_Dataset_V1_2_QWENVALIDATED.xlsx
# expected 1d3552f2e5aa325cd1590d8b73b2968825d9838788c944e89a631f66ecbfd5de
```

## 2. Deterministic tests (no GPU, about 15 s)
```bash
cd pipeline
python3 -m venv .venv && source .venv/bin/activate
pip install torch==2.5.1 transformers==4.46.3 numpy scipy openpyxl pytest
python3 -m pytest -q tests        # expected: 46 passed
```
The tests use a random-weight toy model and verify code paths only, not Qwen behaviour.

## 3. Real-model gates on Modal (from a Mac)
```bash
pip install modal && modal setup
export MODAL_IMAGE_BUILDER_VERSION=2025.06   # Modal workaround used for every real-Qwen run (PI instruction: preserve)
cd pipeline
modal run modal_run.py --dataset ../dataset/history/AlignedLab_Experiment_2_Dataset_V1_2_CANDIDATE.xlsx --stage validate
python3 apply_validate.py ../dataset/history/AlignedLab_Experiment_2_Dataset_V1_2_CANDIDATE.xlsx modal_out/validate/validate.json /tmp/QV.xlsx --exclude R02 R05
# compare the R06/R10 distractors and R02/R05 exclusions with the frozen file; the xlsx bytes may differ (file metadata), so the frozen sha256 is the reference
modal run modal_run.py --dataset ../dataset/AlignedLab_Experiment_2_Dataset_V1_2_QWENVALIDATED.xlsx --stage gate3
```
`gate3` prints `PASS` or exits 1 and writes only `modal_out/gate3/gate3_record.json`. Expected values are in `evidence/gate3/gate3_record.json`.

## 4. Pilot and main (NOT AUTHORISED at freeze)
```bash
modal run modal_run.py --dataset ../dataset/AlignedLab_Experiment_2_Dataset_V1_2_QWENVALIDATED.xlsx --stage pilot --authorised   # only after written PI authorisation
```
Without `--authorised`, `pilot` and `main` refuse to start.

## Determinism

- **Seeds:** M2 per-sample seed = 20261116 + 100·(sha256(item ID) mod 10⁵) + sample index.
- **Statistics:** bootstrap seed 20261116.
- **GPU:** TF32 off; deterministic algorithms on; `CUBLAS_WORKSPACE_CONFIG=:4096:8`.

Gate 3 verified bitwise-identical repeat logits on the A10G.
