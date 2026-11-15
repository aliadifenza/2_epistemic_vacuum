"""One regression test per defect corrected on 15 Nov after the Qualam Gate 3 review (finding numbers in brackets).
Toy-model tests verify code paths only, not Qwen behaviour."""
import numpy as np, torch, sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from exp2 import config as C
from exp2.backend_hf import toy_backend, MaskPaddedVocab, StopAtNewline
from exp2.measure import knownness_class
from exp2.analysis import secondary_tests, inconclusive_conditions, nonanswer_bounds, pilot_feasibility, group_entropy_bits
from exp2.stages import split_for
from exp2.gate3 import gate3_record

be = toy_backend()

# [1.2] padded vocabulary rows are never generated, even when they carry the largest logits
def test_padded_rows_masked_in_generation():
    V = be.vocab_size
    h = be.model.get_output_embeddings().register_forward_hook(lambda m, i, o: o.index_add(-1, torch.arange(V, o.shape[-1]), torch.full((o.shape[-1] - V,), 1e4).expand(*o.shape[:-1], -1)))
    try:
        ids = be._enc("Q: a\nA:")
        raw = be.model.generate(ids, attention_mask=torch.ones_like(ids), max_new_tokens=3, do_sample=False, pad_token_id=be.tok.eos_token_id)
        assert (raw[0, ids.shape[1]:] >= V).all(), "hook did not make padded rows dominant (test is not exercising the risk)"
        g = be.greedy("Q: a\nA:"); s = be.sample("Q: a\nA:", 7)
        assert g["max_new_id"] < V and s["max_new_id"] < V
    finally:
        h.remove()

# [1.7] the complete effective generation configuration is recorded, and every sampling field is explicit
def test_generation_config_complete():
    eg = be.effective_generation
    for k, spec in (("m2", C.M2_GEN), ("m4", C.M4_GEN)):
        full = eg[k]["_full"]
        for f, v in {**C.GEN_NEUTRAL, **spec}.items(): assert full[f] == v, (k, f)
    assert eg["call_settings"]["model_generation_config_replaced_by_explicit_config"]
    be.greedy("Q: a\nA:"); assert be.model.generation_config.top_k == be.gen_configs["m4"].top_k

# [1.8] each stage has exactly one split; unknown stages are rejected; pilot/main need authorisation
def test_stage_split_locked():
    assert split_for("main") == "main" and split_for("pilot") == "pilot" and split_for("gate3") == "pilot"
    try: split_for("mian"); assert False
    except ValueError: pass
    from exp2.stages import AUTHORISATION_REQUIRED; assert AUTHORISATION_REQUIRED == {"pilot", "main"}

# [1.1/1.3/1.8] Gate 3 fails hard: a wrong revision or nondeterministic logits make status FAIL
def test_gate3_fails_on_wrong_revision_and_nondeterminism():
    r = gate3_record(be, toy=True); assert r["status"] == "PASS", r["failures"]
    real = gate3_record(be, toy=False)   # toy commit hash is 'TOY', not the pinned revision
    assert real["status"] == "FAIL" and "checkpoint_revision" in real["failures"]
    orig = be.logits_next; calls = {"n": 0}
    def noisy(p):
        calls["n"] += 1; return orig(p) + (1e-6 if calls["n"] % 2 == 0 else 0)
    be.logits_next = noisy
    try: assert "repeat_logits_bitwise_equal" in gate3_record(be, toy=True)["failures"]
    finally: be.logits_next = orig

# [4.3] attention-mask correction: explicit all-ones mask gives identical logits (checked on Qwen inside gate3_record)
def test_mask_check_present_in_gate3():
    r = gate3_record(be, toy=True); assert r["checks"]["mask_forward_identical"]["ok"] and r["checks"]["mask_greedy_identical"]["ok"]

# [2.6] Holm uses the all-pairs P3 p-value; a missing test is not replaced by p = 1
def test_holm_uses_all_pairs_p3():
    out = secondary_tests({"p": 0.04}, {"perm": {"p": 0.01}})
    assert out["P3_all_pairs"] == 0.01 and abs(out["adjusted"]["P3"] - 0.02) < 1e-12 and abs(out["adjusted"]["P2"] - 0.04) < 1e-12
    assert secondary_tests({"p": 0.04}, {})["adjusted"] is None

# [2.13] inconclusive conditions 3 and 5 come from data, not constants
def test_conditions_3_and_5_computed():
    na = lambda lo, un, n=20: dict(n=n, nonanswer=lo, unmatched=un, lower=lo / n, upper=(lo + un) / n)
    assert inconclusive_conditions(12, 1, 2, na(6, 0), na(0, 0), False, [])["3_nonanswers_over_25pct"] is True
    assert inconclusive_conditions(12, 1, 2, na(2, 0), na(1, 0), False, [])["3_nonanswers_over_25pct"] is False
    assert inconclusive_conditions(12, 1, 2, na(4, 3), na(1, 0), False, [])["3_nonanswers_over_25pct"] is None   # straddles; needs adjudication
    assert inconclusive_conditions(12, 1, 2, na(0, 0), na(0, 0), False, ["x"])["5_integrity_defect"] is True
    assert inconclusive_conditions(0, 1, float("nan"), na(0, 0), na(0, 0), False, [])["2_positive_control_fails"] is None
    codes = [dict(category6="NONANSWER")] * 2 + [dict(category6="UNMATCHED")] + [dict(category6="CORRECT_ANSWER")] * 7
    b = nonanswer_bounds(codes); assert b["lower"] == 0.2 and abs(b["upper"] - 0.3) < 1e-12

# [2.7] M2 seeds depend on the item, not on row order; generation stops at the first newline
def test_m2_seed_order_independent():
    assert C.m2_seed("M01-C", 3) == C.m2_seed("M01-C", 3) and C.m2_seed("M01-C", 3) != C.m2_seed("M02-C", 3)
    assert len({C.m2_seed(f"M{i:02d}-C", k) for i in range(1, 40) for k in range(10)}) == 390
    assert all(C.m2_seed("M01-C", k) < 2 ** 32 for k in range(10))
def test_stop_at_newline_criterion():
    ids = be._enc("Q: a\nA:"); start = ids.shape[1]
    nl = be._enc("\n"); x = be._enc(" It")
    sc = StopAtNewline(be.tok, start)
    assert not bool(sc(torch.cat([ids, x], 1), None)[0]) and bool(sc(torch.cat([ids, x, nl], 1), None)[0])
    for k in range(5):
        s = be.sample("Q: a\nA:", k); assert "\n" not in s["text"]
        if "\n" in s["raw"]: assert "\n" not in be.tok.decode(s["ids"][:-1], skip_special_tokens=True)

# [2.10] question surprisal uses the same tokenisation as the M1 prompt
def test_surprisal_uses_m1_tokenisation():
    from exp2.prompts import three_shot
    q = "Which city hosted the 1904 International Congress of Mathematicians?"; p = three_shot(q)
    s = p.rindex("Q: " + q) + 3
    val, n = be.question_surprisal(p, s, s + len(q))
    enc = be.tok(p, return_offsets_mapping=True, add_special_tokens=False)
    idx = [i for i, (a, b) in enumerate(enc["offset_mapping"]) if i > 0 and a < s + len(q) and b > s]
    ids = torch.tensor([enc["input_ids"]])
    with torch.no_grad(): lp = torch.log_softmax(be.model(ids).logits[0, :, :be.vocab_size], -1)
    manual = float(np.mean([-float(lp[i - 1, ids[0, i]]) for i in idx]))
    assert n == len(idx) and abs(val - manual) < 1e-5
    assert be.tok(p, add_special_tokens=False).input_ids == enc["input_ids"]   # same ids as M1 uses

# [2.4] knownness: strictly highest; ties do not qualify and are recorded; all eight scores retained
class Stub:
    def __init__(self, table): self.t = table
    def seq_logprob(self, prompt, cont): return self.t[(prompt, cont.strip())]
def test_knownness_strict_and_ties():
    t = {("p1", "A"): -1.0, ("p1", "x"): -1.0, ("p1", "y"): -5, ("p1", "z"): -5,
         ("p2", "A"): -1.0, ("p2", "x"): -3, ("p2", "y"): -5, ("p2", "z"): -5}
    cls, forms = knownness_class(Stub(t), "p1", "p2", "A", ["x", "y", "z"])
    assert cls == "Uncertain" and forms[0]["tie_at_top"] and not forms[0]["first"] and forms[1]["first"]
    assert sum(len(f["scores"]) for f in forms) == 8

# [3.2] pilot familiar-answer check: at least 3 of 4 correct
def test_pilot_feasibility():
    ok = [dict(category6="CORRECT_ANSWER")] * 3 + [dict(category6="FABRICATED_OR_INCORRECT")]
    assert pilot_feasibility(ok, [0.9, 0.8, 0.7, 0.2])["passes"] is True
    bad = [dict(category6="CORRECT_ANSWER")] * 2 + [dict(category6="FABRICATED_OR_INCORRECT")] * 2
    assert pilot_feasibility(bad, [0.9, 0.8, 0.7, 0.2])["passes"] is False
    pend = [dict(category6="CORRECT_ANSWER")] * 2 + [dict(category6="UNMATCHED"), dict(category6="ABSTENTION")]
    assert pilot_feasibility(pend, [0.9] * 4)["passes"] is None

# [2.8] M2 entropy over coded groups (rejection / abstention / non-answer distinct; aliases merged)
def test_m2_grouped_entropy():
    from exp2.coding import build_lookup, code_response, m2_group
    it = dict(cond="B", series="IBC", year=1905, twin_series=None, answer="Vienna", aliases=["Vienna", "Wien"], distractors=[])
    lk = build_lookup([it])
    texts = ["Vienna", "Wien.", " vienna, Austria", "There was no such congress.", "I don't know", "Q: next", "Paris", "Vienna"]
    g = [m2_group(code_response(t, it, lk), t) for t in texts]
    assert g.count("CITY:Vienna") == 4 and "REJECTION" in g and "ABSTENTION" in g and "NONANSWER" in g and "CITY:Paris" in g
    groups = {}
    for x in g: groups[x] = groups.get(x, 0) + 1
    assert abs(group_entropy_bits({"a": 5, "b": 5}) - 1.0) < 1e-12 and group_entropy_bits(groups) > 0

# [engineering, 15 Nov] one frozen coding lookup per dataset file: identical for main and pilot
def test_lookup_same_for_all_stages():
    from exp2.run import dataset_lookup
    from _paths import V12
    pools = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "exp2", "pools.json")
    assert dataset_lookup(V12, pools).sha256() == dataset_lookup(V12, pools).sha256()
    lk = dataset_lookup(V12, pools); assert "Leningrad" in lk.gazetteer or lk.canonical("leningrad") == "Saint Petersburg"
    assert {"Heidelberg", "Trier", "Kiev", "Helsinki"} <= lk.gazetteer

# [regression 15 Nov 19:49] every stage modal_run.py dispatches is accepted by the stage dispatcher
def test_every_modal_stage_registered():
    import re
    from exp2.stages import MODAL_STAGES, MEASUREMENT_STAGES, STAGE_SPLIT
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "modal_run.py")).read()
    used = set(re.findall(r'stage == "(\w+)"', src))
    for grp in re.findall(r'stage in \(([^)]*)\)', src): used |= set(re.findall(r'"(\w+)"', grp))
    assert used == set(MODAL_STAGES), (used, MODAL_STAGES)
    for st in used: assert split_for(st)
    assert split_for("validate") == "main+pilot" and "validate" not in MEASUREMENT_STAGES
    assert set(MEASUREMENT_STAGES) | {"validate"} == set(STAGE_SPLIT)
def test_run_rejects_validate_stage():
    from exp2.run import main
    try: main(["--dataset", "x.xlsx", "--out", "/tmp/nope", "--stage", "validate", "--toy"]); assert False
    except ValueError as e: assert "takes no measurements" in str(e)

# [regression 15 Nov 19:57] one resident model: modal_run loads Qwen once and passes it to the runner (OOM on A10G otherwise)
def test_single_model_load_in_modal_run():
    import re
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "modal_run.py")).read()
    assert len(re.findall(r"HFBackend\.load\(", src)) == 1
    calls = re.findall(r"run_main\((.*?)\)\s*\n", src, re.S)
    assert len(re.findall(r"run_main\(", src)) == 2 and src.count("backend=be)") == 2
def test_runner_reuses_supplied_backend():
    import exp2.backend_hf as bh, exp2.run as R, tempfile
    from _paths import V12
    def boom(*a, **k): raise AssertionError("runner tried to load a second model")
    orig_load, orig_toy = bh.HFBackend.load, bh.toy_backend
    bh.HFBackend.load = boom; bh.toy_backend = boom
    try:
        out = R.main(["--dataset", V12, "--out", tempfile.mkdtemp(), "--stage", "coldrun_pilot", "--toy", "--limit", "1", "--skip-m2"], backend=be)
        assert out["n_pairs"] == 1
    finally:
        bh.HFBackend.load, bh.toy_backend = orig_load, orig_toy
