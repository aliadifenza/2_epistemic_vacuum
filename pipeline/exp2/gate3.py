"""Gate 3 engineering checks (V0.4 s8). Every check is recorded; any failure makes status FAIL, and the Modal runner then
exits nonzero and withholds results (Qualam 1.1, 1.3, 1.8)."""
import hashlib, math, torch
from transformers import LogitsProcessorList, StoppingCriteriaList
from .backend_hf import MaskPaddedVocab, StopAtNewline
from .measure import entropy_bits
from . import config as C

SANITY_PROMPTS = ["Q: Which city is the capital of France?\nA:", "Q: Which city is the capital of Peru?\nA:", "Q: a\nA:"]

def gate3_record(be, tokenizer_json_path=None, toy=False):
    rec, fails = {}, []
    def check(name, ok, detail=None):
        rec[name] = dict(ok=bool(ok), detail=detail)
        if not ok: fails.append(name)
    # 1 checkpoint identity
    check("checkpoint_revision", toy or be.commit_hash == C.MODEL_REVISION, dict(expected=C.MODEL_REVISION, found=be.commit_hash, toy=toy))
    if tokenizer_json_path:
        full = hashlib.sha256(open(tokenizer_json_path, "rb").read()).hexdigest()
        check("tokenizer_sha256_prefix", full.startswith(C.TOKENIZER_JSON_SHA256_PREFIX), dict(full=full, recorded_prefix=C.TOKENIZER_JSON_SHA256_PREFIX))
    elif not toy:
        check("tokenizer_sha256_prefix", False, "tokenizer.json path not supplied")
    # 2 vocabulary
    check("vocab_padding_consistent", be.lm_head_rows >= be.vocab_size, dict(tokenizer=be.vocab_size, lm_head_rows=be.lm_head_rows, padded_rows=be.lm_head_rows - be.vocab_size))
    # 3 logits and probabilities
    lg = be.logits_next(SANITY_PROMPTS[0]); H, pm = entropy_bits(lg, be.vocab_size)
    check("logits_finite", bool(torch.isfinite(torch.tensor(lg[:be.vocab_size])).all()), None)
    check("entropy_in_range", 0.0 <= H <= math.log2(be.vocab_size) + 1e-6, dict(H_bits=H, p_max=pm))
    lg2 = be.logits_next(SANITY_PROMPTS[0])
    check("repeat_logits_bitwise_equal", (lg == lg2).all(), dict(max_abs_diff=float(abs(lg - lg2).max())))
    s1 = be.seq_logprob(SANITY_PROMPTS[0], " Paris"); s2 = be.seq_logprob(SANITY_PROMPTS[0], " Paris")
    check("repeat_seq_logprob_equal", s1 == s2, dict(logp_paris=s1))
    if not toy:
        g = be.greedy(SANITY_PROMPTS[0])
        check("sanity_greedy_paris", g["text"].strip().startswith("Paris"), dict(greedy=g["text"], H_bits=H, p_max=pm))
    # 4 attention-mask correction on the actual model: explicit all-ones mask vs no mask
    with torch.no_grad():
        diffs, same_gen = [], []
        for p in SANITY_PROMPTS:
            ids = be._enc(p)
            a = be.model(ids).logits; b = be.model(ids, attention_mask=torch.ones_like(ids)).logits
            diffs.append(float((a - b).abs().max()))
            gc = be.gen_configs["m4"]; be.model.generation_config = gc
            kw = dict(generation_config=gc, logits_processor=LogitsProcessorList([MaskPaddedVocab(be.vocab_size)]),
                      stopping_criteria=StoppingCriteriaList([StopAtNewline(be.tok, ids.shape[1])]))
            o1 = be.model.generate(ids, **kw); o2 = be.model.generate(ids, attention_mask=torch.ones_like(ids), **kw)
            same_gen.append(bool(torch.equal(o1, o2)))
    check("mask_forward_identical", max(diffs) == 0.0, dict(max_abs_diff_per_prompt=diffs))
    check("mask_greedy_identical", all(same_gen), dict(per_prompt=same_gen))
    # 5 generation: padded rows never generated; seeded sampling reproducible; stop at newline
    outs = [be.greedy(p) for p in SANITY_PROMPTS] + [be.sample(p, C.m2_seed("GATE3", k)) for k, p in enumerate(SANITY_PROMPTS)]
    check("no_padded_tokens_generated", all(o["max_new_id"] is None or o["max_new_id"] < be.vocab_size for o in outs), [o["max_new_id"] for o in outs])
    r1 = be.sample(SANITY_PROMPTS[0], 12345); r2 = be.sample(SANITY_PROMPTS[0], 12345)
    check("seeded_sampling_reproducible", r1["ids"] == r2["ids"], dict(a=r1["raw"], b=r2["raw"]))
    def stopped_ok(o):   # newline absent from the answer, and if a newline was generated it is in the final token
        if "\n" in o["text"]: return False
        return "\n" not in o["raw"] or "\n" not in be.tok.decode(o["ids"][:-1], skip_special_tokens=True)
    check("stops_at_newline", all(stopped_ok(o) for o in outs), [o["raw"] for o in outs])
    check("generation_config_explicit", be.effective_generation["call_settings"]["model_generation_config_replaced_by_explicit_config"], be.effective_generation)
    return dict(status="PASS" if not fails else "FAIL", failures=fails, checks=rec)
