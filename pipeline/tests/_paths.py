import os
_P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def data(*cands):
    """First existing path among candidates (repo layout first, then the original workspace layout)."""
    for c in cands:
        p = os.path.normpath(os.path.join(_P, c))
        if os.path.exists(p): return p
    raise FileNotFoundError(cands)
V12 = data("../dataset/history/AlignedLab_Experiment_2_Dataset_V1_2_CANDIDATE.xlsx", "../out/v12/AlignedLab_Experiment_2_Dataset_V1_2_CANDIDATE.xlsx")
V07 = data("../dataset/history/AlignedLab_Experiment_2_Dataset_V0_7.xlsx", "../state/AlignedLab_Experiment_2_Dataset_V0_7.xlsx")
VAL = data("../evidence/validate/validate_run2_superseded_pools.json", "../out/validate_run2_1916.json")
