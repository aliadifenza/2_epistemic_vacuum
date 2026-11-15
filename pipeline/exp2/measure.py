"""Model measurements (V0.4 s4). Backend interface: logits_next, seq_logprob, question_surprisal, greedy, sample, vocab_size."""
import numpy as np

def log_softmax(x):
    x = np.asarray(x, dtype=np.float32)
    z = x - x.max()
    return z - np.log(np.exp(z).sum(dtype=np.float32))

def entropy_bits(logits, vocab_size):
    """Shannon entropy in bits of the valid next-token distribution (V0.4 M1 steps 4-6). Returns (H, p_max)."""
    lp = log_softmax(np.asarray(logits, dtype=np.float32)[:vocab_size])
    p = np.exp(lp)
    return float(-(p * lp).sum() / np.log(2.0)), float(p.max())

def first_token_entropy(backend, prompt):
    return entropy_bits(backend.logits_next(prompt), backend.vocab_size)

def candidate_scores(backend, prompt, candidates):
    """V0.4 M3a step 6: complete-sequence log-probabilities of each candidate answer."""
    return {c: backend.seq_logprob(prompt, " " + c) for c in candidates}

def knownness_class(backend, p1, p2, answer, distractors):
    """V0.4 M3a. Known: verified answer ranks first in both formulations; Unknown: in neither; Uncertain: disagree.
    PI decision 15 Nov: 'ranks first' means strictly highest; an exact tie does not qualify. All eight scores and ties recorded."""
    forms = []
    for p in (p1, p2):
        s = candidate_scores(backend, p, [answer] + list(distractors))
        best_other = max(s[d] for d in distractors)
        forms.append(dict(prompt=p, scores=s, first=bool(s[answer] > best_other), tie_at_top=bool(s[answer] == best_other),
                          margin=s[answer] - best_other))
    firsts = [f["first"] for f in forms]
    cls = "Known" if all(firsts) else "Unknown" if not any(firsts) else "Uncertain"
    return cls, forms

def rejection_pref(backend, prompt, R, S):
    """V0.4 M3b: d(q) = log P(R|q) - log P(S|q)."""
    return backend.seq_logprob(prompt, R) - backend.seq_logprob(prompt, S)
