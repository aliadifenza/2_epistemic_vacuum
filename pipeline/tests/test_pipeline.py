import numpy as np, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from exp2 import config as C
from exp2.measure import entropy_bits, log_softmax
from exp2.analysis import *
from exp2.prompts import three_shot, zero_shot

def test_entropy_uniform_and_onehot():
    V = 1000
    H, pm = entropy_bits(np.zeros(V, np.float32), V); assert abs(H - math.log2(V)) < 1e-4 and abs(pm - 1 / V) < 1e-9
    x = np.full(V, -1e4, np.float32); x[3] = 0
    H, pm = entropy_bits(x, V); assert H < 1e-6 and pm > 0.9999
def test_entropy_two_point():
    x = np.full(50, -1e4, np.float32); x[0] = 0; x[1] = 0
    H, _ = entropy_bits(x, 50); assert abs(H - 1.0) < 1e-5
def test_padded_vocab_rows_removed():
    V = 100; x = np.zeros(V + 20, np.float32); x[V:] = 50.0
    H, _ = entropy_bits(x, V); assert abs(H - math.log2(V)) < 1e-4
def test_log_softmax_stable():
    lp = log_softmax(np.array([1e4, 1e4 - 1], np.float32)); assert abs(np.exp(lp).sum() - 1) < 1e-5
def test_prompt_format():
    p = three_shot("Which city hosted the 1904 International Congress of Mathematicians?")
    assert p.endswith("A:") and p.count("Q:") == 4 and p.count("\nA: ") == 3
    assert p.startswith("Q: Which city is the capital of Peru?\nA: Lima\n\n")
    assert three_shot("x")[:-len("Q: x\nA:")] == three_shot("y")[:-len("Q: y\nA:")]
    assert zero_shot("x") == "Q: x\nA:"
def test_bootstrap_and_perm_known_signal():
    rng = np.random.default_rng(1); d = rng.normal(1.0, 0.5, 23)
    lo, hi = bootstrap_ci(d); assert lo > 0.5 and hi < 1.5
    r = signflip_perm_test(d); assert r["method"] == "exact" and r["n_perm"] == 2 ** 23 and r["p"] < 1e-4 and r["sided"] == "two-sided"
def test_perm_null():
    rng = np.random.default_rng(2); assert signflip_perm_test(rng.normal(0.0, 1.0, 23))["p"] > 0.05
def test_perm_exact_small():
    assert abs(signflip_perm_test(np.array([1.0, 2.0, 3.0]))["p"] - 0.25) < 1e-12
def test_perm_mc_branch():
    rng = np.random.default_rng(3); assert signflip_perm_test(rng.normal(0, 1, 30), mc_n=2000)["method"] == "monte-carlo"
def test_bootstrap_reproducible():
    d = np.arange(10.0); assert bootstrap_ci(d, n=500) == bootstrap_ci(d, n=500)
def test_two_sample():
    rng = np.random.default_rng(4); r = two_sample(rng.normal(2, 1, 30), rng.normal(0, 1, 12)); assert r["ci"][0] > 0 and r["p"] < 0.01
def test_holm():
    assert holm([0.01, 0.04]) == [0.02, 0.04]; assert holm([0.04, 0.01]) == [0.04, 0.02]
