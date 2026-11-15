"""Qwen-dependent item validation (Dataset V0.5 rules, recorded in the V0.7 README):
 - question token length: |tokens(C) - tokens(B)| <= 2
 - distractors: same Qwen token count as the answer; |logp(answer) - logp(distractor)| <= 1 nat under the neutral prefix "The city of"
Usage (inside modal_run stage 'validate' or locally with a real backend):
   validate_pairs(backend, pairs) -> dict per pair; select_distractors(backend, answer, pool) -> 3 chosen + table"""
NEUTRAL_PREFIX = "The city of"

def ntok(be, s): return len(be.tok(s, add_special_tokens=False).input_ids)

def prominence(be, city): return be.seq_logprob(NEUTRAL_PREFIX, " " + city)

def select_distractors(be, answer, pool, max_delta=1.0):
    ta, pa = ntok(be, " " + answer), prominence(be, answer)
    rows = []
    for c in pool:
        tc, pc = ntok(be, " " + c), prominence(be, c)
        rows.append(dict(city=c, tokens=tc, logp=pc, delta=pc - pa, token_pass=(tc == ta), prom_pass=(abs(pc - pa) <= max_delta)))
    ok = [r for r in rows if r["token_pass"] and r["prom_pass"]]
    ok.sort(key=lambda r: abs(r["delta"]))
    return dict(answer=answer, answer_tokens=ta, answer_logp=pa, chosen=[r["city"] for r in ok[:3]], enough=len(ok) >= 3, table=rows)

def validate_pairs(be, pairs):
    out = {}
    for pid, pr in pairs.items():
        b, c = pr["B"], pr["C"]
        tb, tc = ntok(be, b["Question"]), ntok(be, c["Question"])
        res = dict(tokens_B=tb, tokens_C=tc, diff=tc - tb, token_pass=abs(tc - tb) <= 2)
        if b.get("Distractor 1") and not str(b["Distractor 1"]).startswith(("PENDING", "None")):
            res["distractors"] = select_distractors(be, b["Reference Answer"], [b["Distractor 1"], b["Distractor 2"], b["Distractor 3"]])
        out[pid] = res
    return out
