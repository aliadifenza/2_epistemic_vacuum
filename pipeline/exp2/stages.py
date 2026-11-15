"""Stage -> split mapping (Qualam 1.8). Each stage has exactly one fixed scope; nothing is defaulted.
'validate' covers both splits (it checks every included pair) and takes no measurements."""
STAGE_SPLIT = {"validate": "main+pilot", "gate3": "pilot", "pilot": "pilot", "main": "main",
               "coldrun_main": "main", "coldrun_pilot": "pilot"}
MODAL_STAGES = ("validate", "gate3", "pilot", "main")          # every stage modal_run.py dispatches
MEASUREMENT_STAGES = ("gate3", "pilot", "main", "coldrun_main", "coldrun_pilot")   # stages exp2.run accepts
AUTHORISATION_REQUIRED = {"pilot", "main"}   # Modal refuses these without an explicit --authorised flag

def split_for(stage: str) -> str:
    if stage not in STAGE_SPLIT:
        raise ValueError(f"unknown stage {stage!r}; allowed: {sorted(STAGE_SPLIT)}")
    return STAGE_SPLIT[stage]
