"""Explain every distractor-selection result in validate.json: for each answer, each pool city's Qwen token count,
prominence delta (nats, "The city of" prefix) and the reason it passes or fails (TOKENS, NAT, BOTH).
Usage: python3 diagnose_validate.py modal_out/validate/validate.json"""
import json, sys
V = json.load(open(sys.argv[1]))
for ans, d in V.get("new_distractors", {}).items():
    print(f"\n== {ans}: answer tokens {d['answer_tokens']}, logp {d['answer_logp']:.3f}; chosen {d['chosen']} ({'OK' if d['enough'] else 'SHORT'})")
    rows = sorted(d["table"], key=lambda r: abs(r["delta"]))
    n_tok = sum(r["token_pass"] for r in rows); n_nat = sum(r["prom_pass"] for r in rows)
    print(f"   pool {len(rows)}: equal tokens {n_tok}, within +-1 nat {n_nat}, both {sum(r['token_pass'] and r['prom_pass'] for r in rows)}")
    for r in rows[:12]:
        why = "OK" if r["token_pass"] and r["prom_pass"] else ("BOTH" if not r["token_pass"] and not r["prom_pass"] else ("TOKENS" if not r["token_pass"] else "NAT"))
        print(f"   {r['city']:<14} tok {r['tokens']}  delta {r['delta']:+.3f}  {why}")
