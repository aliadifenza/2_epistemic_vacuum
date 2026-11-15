from .config import DEMOS

def three_shot(question: str) -> str:
    """V0.4 s2.5 primary format. Ends immediately after 'A:' with no trailing space."""
    body = "".join(f"Q: {q}\nA: {a}\n\n" for q, a in DEMOS)
    return body + f"Q: {question}\nA:"

def zero_shot(question: str) -> str:
    return f"Q: {question}\nA:"

def knownness_prompt(paraphrase: str) -> str:
    """V0.4 M3a: declarative completion ending immediately before the answer; no demonstrations.
    The dataset paraphrases end with 'was held in' / 'was'; the answer continuation carries its own leading space."""
    return paraphrase.rstrip()
