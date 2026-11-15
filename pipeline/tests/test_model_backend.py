"""Backend checks on the TOY random-weight model. They verify code paths (sequence scoring, generation settings, determinism),
NOT Qwen correctness."""
import numpy as np, torch, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from exp2.backend_hf import toy_backend
from exp2.measure import entropy_bits, knownness_class, rejection_pref
from exp2 import config as C
be = toy_backend()
def test_vocab_padding_present():
    assert be.lm_head_rows > be.vocab_size
def test_seq_logprob_manual():
    p, c = "Q: a\nA:", " Lima"
    ids = be.tok(p + c, add_special_tokens=False).input_ids; np_ = len(be.tok(p, add_special_tokens=False).input_ids)
    with torch.no_grad(): lp = torch.log_softmax(be.model(torch.tensor([ids])).logits[0, :, :be.vocab_size].float(), -1)
    manual = sum(float(lp[i - 1, ids[i]]) for i in range(np_, len(ids)))
    assert abs(be.seq_logprob(p, c) - manual) < 1e-4
def test_entropy_matches_torch():
    lg = be.logits_next("Q: a\nA:"); H, _ = entropy_bits(lg, be.vocab_size)
    p = torch.softmax(torch.tensor(lg[:be.vocab_size]), 0); assert abs(H - float(-(p * torch.log2(p)).sum())) < 1e-3
def test_knownness_logic_and_determinism():
    cls, f = knownness_class(be, "The X was held in", "In Y, the host was", "Lima", ["Agra", "Nairobi", "Heidelberg"])
    assert cls in ("Known", "Unknown", "Uncertain") and len(f) == 2
    assert be.logits_next("Q: a\nA:").tolist() == be.logits_next("Q: a\nA:").tolist()
def test_sampling_seeded_and_greedy_fixed():
    p = "Q: a\nA:"
    assert be.sample(p, 5)["ids"] == be.sample(p, 5)["ids"] and be.greedy(p)["ids"] == be.greedy(p)["ids"]
def test_rejection_pref_finite():
    assert np.isfinite(rejection_pref(be, "Q: a\nA:", C.REJECT_R1, C.ACCEPT_S1))
