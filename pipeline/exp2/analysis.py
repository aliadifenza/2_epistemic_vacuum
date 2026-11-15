"""Statistics and analysis (V0.4 s6-7). Corrections 15 Nov (Qualam review): Holm takes the all-pairs P3 p-value;
inconclusive conditions 3 and 5 computed from data; M2 entropy over coded semantic groups; pilot feasibility check."""
import numpy as np
from . import config as C

def paired_summary(d):
    d = np.asarray(d, float)
    return dict(n=len(d), mean=float(d.mean()), median=float(np.median(d)), prop_positive=float((d > 0).mean()))

def bootstrap_ci(d, n=C.BOOTSTRAP_N, seed=C.BOOTSTRAP_SEED, level=0.95):
    """95% percentile bootstrap of the mean, pair-level resampling (V0.4 s7.1)."""
    d = np.asarray(d, float); rng = np.random.default_rng(seed)
    means = rng.choice(d, size=(n, len(d)), replace=True).mean(axis=1)
    a = (1 - level) / 2
    return float(np.quantile(means, a)), float(np.quantile(means, 1 - a))

def signflip_perm_test(d, mc_n=C.PERM_MC_N, seed=C.PERM_SEED):
    """Two-sided paired sign-flip permutation test of mean = 0. Exact enumeration for n <= EXACT_PERM_MAX_N."""
    d = np.asarray(d, float); n = len(d); obs = abs(d.mean())
    if n <= C.EXACT_PERM_MAX_N:
        total = 0; count = 0; B = 1 << 16
        for start in range(0, 1 << n, B):
            idx = np.arange(start, min(start + B, 1 << n), dtype=np.int64)
            signs = ((idx[:, None] >> np.arange(n)) & 1) * 2 - 1
            m = np.abs((signs * d).mean(axis=1))
            count += int((m >= obs - 1e-12).sum()); total += len(idx)
        return dict(p=count / total, method="exact", n_perm=total, sided="two-sided")
    rng = np.random.default_rng(seed)
    signs = rng.choice([-1, 1], size=(mc_n, n))
    m = np.abs((signs * d).mean(axis=1))
    return dict(p=float(((m >= obs - 1e-12).sum() + 1) / (mc_n + 1)), method="monte-carlo", n_perm=mc_n, sided="two-sided")

def two_sample(x, y, n=C.BOOTSTRAP_N, seed=C.BOOTSTRAP_SEED):
    """Mean difference x - y, bootstrap CI and two-sided label-permutation test (V0.4 s7.2, P2)."""
    x, y = np.asarray(x, float), np.asarray(y, float); rng = np.random.default_rng(seed)
    obs = x.mean() - y.mean()
    bx = rng.choice(x, (n, len(x))).mean(1); by = rng.choice(y, (n, len(y))).mean(1)
    ci = (float(np.quantile(bx - by, .025)), float(np.quantile(bx - by, .975)))
    pooled = np.concatenate([x, y]); cnt = 0; n_perm = C.PERM_MC_N // 10
    for _ in range(n_perm):
        rng.shuffle(pooled); cnt += abs(pooled[:len(x)].mean() - pooled[len(x):].mean()) >= abs(obs) - 1e-12
    return dict(diff=float(obs), ci=ci, p=float((cnt + 1) / (n_perm + 1)), n_perm=n_perm, sided="two-sided")

def holm(pvals):
    idx = np.argsort(pvals); m = len(pvals); adj = np.empty(m); prev = 0.0
    for rank, i in enumerate(idx):
        prev = max(prev, (m - rank) * pvals[i]); adj[i] = min(1.0, prev)
    return list(adj)

def secondary_tests(p2_block, p3_all_block):
    """V0.4 s7.2: Holm across the two secondary tests. P3 is defined over all matched B/C pairs (not the Unknown subset).
    A missing test is reported as missing, never replaced by p = 1 (Qualam 2.6)."""
    p2 = p2_block.get("p"); p3 = p3_all_block.get("perm", {}).get("p")
    if p2 is None or p3 is None:
        return dict(P2=p2, P3_all_pairs=p3, adjusted=None, note="a secondary test is missing; Holm not computed")
    a = holm([p2, p3]); return dict(P2=p2, P3_all_pairs=p3, adjusted=dict(P2=a[0], P3=a[1]), method="Holm")

def group_entropy_bits(groups):
    counts = np.array(list(groups.values()), float); p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum())

def nonanswer_bounds(codes):
    """V0.4 s7.4(3) input. Lower bound counts coded NONANSWER; upper bound also counts UNMATCHED strings awaiting adjudication."""
    n = len(codes)
    if n == 0: return dict(n=0, lower=None, upper=None)
    lo = sum(c["category6"] == "NONANSWER" for c in codes); un = sum(c["category6"] == "UNMATCHED" for c in codes)
    return dict(n=n, nonanswer=lo, unmatched=un, lower=lo / n, upper=(lo + un) / n)

def inconclusive_conditions(n_unknown, medA, medBunk, na_B, na_C, fmt_signs_oppose, integrity_failures):
    """V0.4 s7.4. Each value is True (condition met: inconclusive), False, or None (undetermined) with a reason."""
    def c3():
        if na_B.get("n", 0) == 0 or na_C.get("n", 0) == 0: return None
        if max(na_B["lower"], na_C["lower"]) > C.NONANSWER_MAX_FRAC: return True
        if max(na_B["upper"], na_C["upper"]) <= C.NONANSWER_MAX_FRAC: return False
        return None   # depends on adjudication of UNMATCHED strings
    c2 = None if (medBunk is None or np.isnan(medBunk) or medA is None or np.isnan(medA)) else (not (medA < medBunk))
    return {"1_fewer_than_10_unknown_pairs": n_unknown < C.MIN_UNKNOWN_PAIRS,
            "2_positive_control_fails": c2,
            "3_nonanswers_over_25pct": c3(),
            "4_format_dependent": bool(fmt_signs_oppose),
            "5_integrity_defect": bool(integrity_failures),
            "details": {"2": "None = undetermined (no Unknown pairs or no A items)" if c2 is None else "median H(A) vs median H(B-Unknown), three-shot",
                        "3": dict(B=na_B, C=na_C, threshold=C.NONANSWER_MAX_FRAC, rule="lower bound = coded NONANSWER; upper bound adds UNMATCHED awaiting adjudication; None = straddles threshold"),
                        "5": integrity_failures}}

def pilot_feasibility(A_codes, A_pmax):
    """V0.4 Gate 5: at least three of four familiar pilot questions correct (greedy, three-shot); median top-token
    probability recorded against the 0.5 diagnostic."""
    n_correct = sum(c["category6"] == "CORRECT_ANSWER" for c in A_codes)
    pending = sum(c["category6"] == "UNMATCHED" for c in A_codes)
    med = float(np.median(A_pmax)) if A_pmax else None
    status = (n_correct >= C.PILOT_A_MIN_CORRECT) if (n_correct >= C.PILOT_A_MIN_CORRECT or n_correct + pending < C.PILOT_A_MIN_CORRECT) else None
    return dict(n_items=len(A_codes), n_correct=n_correct, n_unmatched_pending=pending, required=C.PILOT_A_MIN_CORRECT,
                passes=status, median_top_token_prob=med, diagnostic_threshold=C.PILOT_PMAX_DIAGNOSTIC,
                median_above_diagnostic=(med > C.PILOT_PMAX_DIAGNOSTIC) if med is not None else None)

def series_insensitive(c_codes_unknown):
    """Verification protocol s4 descriptive rate (PI decision 3): accepted C responses in Unknown pairs whose content class
    is TWIN or SAME-YEAR-OTHER-SERIES. >= 50% is labelled 'predominant'; descriptive only."""
    acc = [c for c in c_codes_unknown if c["premise_status"] == "ACCEPTED"]
    num = sum(c["content_class"] in ("TWIN", "SAME-YEAR-OTHER-SERIES") for c in acc)
    pct = (100.0 * num / len(acc)) if acc else None
    return dict(numerator=num, denominator=len(acc), percent=pct, label=("predominant" if pct is not None and pct >= 50 else None))
