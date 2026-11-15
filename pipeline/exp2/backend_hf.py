"""HF transformers backend for Qwen2.5-3B Base (and the toy model used for code-path tests).
Corrections 15 Nov (Qualam review): padded vocabulary rows masked during generation; every generation call uses one explicit
GenerationConfig (logged in full); generation stops at the first newline; question surprisal uses the M1 tokenisation."""
import copy, hashlib, numpy as np, torch
from transformers import (AutoModelForCausalLM, AutoTokenizer, GenerationConfig, LogitsProcessor, LogitsProcessorList,
                          StoppingCriteria, StoppingCriteriaList)
from . import config as C

class MaskPaddedVocab(LogitsProcessor):
    """Rows of the LM head beyond the tokenizer vocabulary are implementation padding (V0.4 M1 step 4); never generate them."""
    def __init__(self, vocab_size): self.V = vocab_size
    def __call__(self, input_ids, scores):
        if scores.shape[-1] > self.V: scores[:, self.V:] = float("-inf")
        return scores

class StopAtNewline(StoppingCriteria):
    def __init__(self, tok, start): self.tok, self.start = tok, start
    def __call__(self, input_ids, scores, **kw):
        done = "\n" in self.tok.decode(input_ids[0, self.start:], skip_special_tokens=True)
        return torch.full((input_ids.shape[0],), done, dtype=torch.bool, device=input_ids.device)

def make_gen_config(tok, kind):
    base = dict(C.GEN_NEUTRAL, pad_token_id=tok.eos_token_id, eos_token_id=tok.eos_token_id, bos_token_id=getattr(tok, "bos_token_id", None))
    spec = C.M2_GEN if kind == "m2" else C.M4_GEN
    if not spec["do_sample"]: base.update(temperature=1.0, top_p=1.0, top_k=50)   # library defaults; unused when do_sample=False
    return GenerationConfig(**dict(base, **spec))

class HFBackend:
    def __init__(self, model, tok, device="cpu"):
        self.model, self.tok, self.device = model.eval(), tok, device
        self.vocab_size = len(tok)          # valid tokenizer vocab; model rows beyond are padding
        self.lm_head_rows = model.get_output_embeddings().weight.shape[0]
        self.checkpoint_generation_config = model.generation_config.to_dict() if model.generation_config is not None else {}
        self.gen_configs = {k: make_gen_config(tok, k) for k in ("m4", "m2")}
        self.effective_generation = {k: v.to_diff_dict() | {"_full": v.to_dict()} for k, v in self.gen_configs.items()}
        self.effective_generation["call_settings"] = dict(attention_mask="all ones (single unpadded sequence)",
            logits_processors=["MaskPaddedVocab(vocab_size=%d)" % self.vocab_size], stopping_criteria=["StopAtNewline"] if C.STOP_AT_NEWLINE else [],
            model_generation_config_replaced_by_explicit_config=True)
    @classmethod
    def load(cls, model_id, revision, device="cpu", dtype=torch.float32):
        if device.startswith("cuda"):
            torch.backends.cuda.matmul.allow_tf32 = False; torch.backends.cudnn.allow_tf32 = False   # true float32 (V0.4 M1 step 5)
            torch.backends.cudnn.deterministic = True; torch.backends.cudnn.benchmark = False
        tok = AutoTokenizer.from_pretrained(model_id, revision=revision)
        model = AutoModelForCausalLM.from_pretrained(model_id, revision=revision, torch_dtype=dtype).to(device)
        be = cls(model, tok, device); be.commit_hash = getattr(model.config, "_commit_hash", None); return be
    def _enc(self, text):
        return self.tok(text, return_tensors="pt", add_special_tokens=False).input_ids.to(self.device)
    def _fwd(self, ids):
        return self.model(ids, attention_mask=torch.ones_like(ids)).logits
    @torch.no_grad()
    def logits_next(self, prompt):
        return self._fwd(self._enc(prompt))[0, -1].float().cpu().numpy()
    @torch.no_grad()
    def seq_logprob(self, prompt, continuation):
        p = self._enc(prompt); c = self._enc(continuation)
        assert c.shape[1] > 0, "empty continuation"
        ids = torch.cat([p, c], 1)
        lp = torch.log_softmax(self._fwd(ids)[0, :, :self.vocab_size].float(), -1)
        tgt = ids[0, p.shape[1]:]
        return float(lp[p.shape[1] - 1:-1].gather(1, tgt[:, None]).sum())
    @torch.no_grad()
    def question_surprisal(self, prompt, q_start, q_end):
        """Mean -log p (nats) of the question's tokens inside the M1 prompt, tokenised exactly as M1 tokenises it.
        A token belongs to the question if its character span overlaps [q_start, q_end) (Qualam 2.10)."""
        enc = self.tok(prompt, return_offsets_mapping=True, add_special_tokens=False)
        ids = torch.tensor([enc["input_ids"]], device=self.device)
        lp = torch.log_softmax(self._fwd(ids)[0, :, :self.vocab_size].float(), -1)
        idx = [i for i, (a, b) in enumerate(enc["offset_mapping"]) if i > 0 and a < q_end and b > q_start]
        assert idx, "no question tokens found"
        return float(np.mean([-float(lp[i - 1, ids[0, i]]) for i in idx])), len(idx)
    @torch.no_grad()
    def _generate(self, prompt, kind, seed=None):
        gc = self.gen_configs[kind]
        ids = self._enc(prompt); start = ids.shape[1]
        if seed is not None: torch.manual_seed(seed)
        self.model.generation_config = copy.deepcopy(gc)      # nothing left to inherit
        out = self.model.generate(ids, attention_mask=torch.ones_like(ids), generation_config=gc,
                                  logits_processor=LogitsProcessorList([MaskPaddedVocab(self.vocab_size)]),
                                  stopping_criteria=StoppingCriteriaList([StopAtNewline(self.tok, start)] if C.STOP_AT_NEWLINE else []))
        seq = out if torch.is_tensor(out) else out.sequences
        new = seq[0, start:].tolist()
        raw = self.tok.decode(new, skip_special_tokens=True)
        return dict(ids=new, raw=raw, text=raw.split("\n")[0], seed=seed, max_new_id=max(new) if new else None)
    def greedy(self, prompt):
        return self._generate(prompt, "m4")
    def sample(self, prompt, seed):
        return self._generate(prompt, "m2", seed)

def toy_backend(seed=0):
    """Tiny random-weight Qwen2-architecture model with a locally trained BPE tokenizer. Code-path tests only."""
    from transformers import Qwen2Config, PreTrainedTokenizerFast
    from tokenizers import Tokenizer, models, pre_tokenizers, decoders, trainers
    torch.manual_seed(seed)
    tk = Tokenizer(models.BPE(unk_token="<unk>")); tk.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False); tk.decoder = decoders.ByteLevel()
    tr = trainers.BpeTrainer(vocab_size=600, special_tokens=["<unk>", "<eos>"], initial_alphabet=pre_tokenizers.ByteLevel.alphabet())
    tk.train_from_iterator(["Which city hosted the 1904 International Congress of Mathematicians? Heidelberg Lima Nairobi Agra Q: A: It was That never happened No such event ever took place\n"], tr)
    tok = PreTrainedTokenizerFast(tokenizer_object=tk, eos_token="<eos>", unk_token="<unk>")
    cfg = Qwen2Config(vocab_size=len(tok) + 8, hidden_size=64, intermediate_size=128, num_hidden_layers=2, num_attention_heads=4, num_key_value_heads=2, max_position_embeddings=512)
    model = AutoModelForCausalLM.from_config(cfg)
    be = HFBackend(model, tok); be.commit_hash = "TOY"; return be

def sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()
