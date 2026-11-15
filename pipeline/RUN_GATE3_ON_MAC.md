# Gate 3 on the Mac — corrected pipeline (15 Nov 2026, 20:30)

```bash
cd ~/AlignedLab/exp2_v12/pipeline && source .venv/bin/activate
zip -qr ../pipeline_backup_1935.zip . -x '.venv/*'                       # keep the previous version
unzip -o ~/Downloads/Exp2_pipeline_corrected_2026-11-15.zip -d .         # overwrites code; keeps .venv and modal_out
rm -rf modal_out/validate modal_out/gate3 ../AlignedLab_Experiment_2_Dataset_V1_2_QWENVALIDATED.xlsx   # outputs of the old code

# 1. validate (replacement-pair distractors; now records the dataset hash)
modal run modal_run.py --dataset ../AlignedLab_Experiment_2_Dataset_V1_2_CANDIDATE.xlsx --stage validate
python3 diagnose_validate.py modal_out/validate/validate.json > diagnose.txt; cat diagnose.txt

# 2. apply, per PI decision 11 (choose one)
python3 apply_validate.py ../AlignedLab_Experiment_2_Dataset_V1_2_CANDIDATE.xlsx modal_out/validate/validate.json ../AlignedLab_Experiment_2_Dataset_V1_2_QWENVALIDATED.xlsx --exclude R05
#   if diagnose.txt shows Kyoto short:  ... --exclude R02 R05

# 3. gate3 (only if step 2 printed "all remaining pairs pass")
modal run modal_run.py --dataset ../AlignedLab_Experiment_2_Dataset_V1_2_QWENVALIDATED.xlsx --stage gate3
```

`gate3` prints `stage gate3: PASS` or exits with an error. On failure it writes only `modal_out/gate3/gate3_record.json`, listing the failed checks.
`pilot` and `main` refuse to start without `--authorised`. Do not use it until the PI authorises the pilot after Gate 4.

Upload to the chat afterwards: `modal_out/validate/validate.json`, `diagnose.txt`, everything in `modal_out/gate3/`, and the QWENVALIDATED xlsx.
