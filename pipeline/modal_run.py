"""Modal GPU runner for Experiment 2 — Qwen2.5-3B Base at the pinned revision. Run from the Mac:
    modal run modal_run.py --dataset <xlsx> --stage validate
    modal run modal_run.py --dataset <QWENVALIDATED xlsx> --stage gate3
    modal run modal_run.py --dataset <frozen xlsx> --stage pilot --authorised     (only after PI authorisation)
Each stage has exactly one split (exp2/stages.py). gate3 exits nonzero and withholds results if any check fails;
the failure record is still written so it can be audited."""
import modal, os, hashlib, json, pathlib, time, sys
app = modal.App("alignedlab-exp2")
image = (modal.Image.debian_slim(python_version="3.12")
         .pip_install("torch==2.5.1", "transformers==4.46.3", "accelerate", "openpyxl", "numpy", "scipy", "safetensors", "huggingface_hub")
         .env({"CUBLAS_WORKSPACE_CONFIG": ":4096:8"})
         .add_local_dir("exp2", remote_path="/root/exp2"))
vol = modal.Volume.from_name("exp2-hf-cache", create_if_missing=True)
MODEL_ID, REV = "Qwen/Qwen2.5-3B", "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
GPU = "A10G"            # 24 GB; Qwen2.5-3B float32 needs ~12 GB
GPU_USD_PER_H = 1.10    # assumed list price for the cost estimate; the Modal dashboard has the billed figure

@app.function(image=image, gpu=GPU, timeout=3 * 3600, volumes={"/root/.cache/huggingface": vol})
def run(dataset_bytes: bytes, stage: str, limit: int, expected_sha: str):
    import sys; sys.path.insert(0, "/root"); os.chdir("/root"); t0 = time.time()
    import torch
    torch.use_deterministic_algorithms(True, warn_only=True)
    from huggingface_hub import snapshot_download
    from exp2.stages import split_for
    split = split_for(stage)
    path = snapshot_download(MODEL_ID, revision=REV); vol.commit()
    shas = {f: hashlib.sha256(open(f"{path}/{f}", "rb").read()).hexdigest() for f in sorted(os.listdir(path)) if f.endswith((".json", ".safetensors", ".txt"))}
    ds_sha = hashlib.sha256(dataset_bytes).hexdigest()
    open("/tmp/ds.xlsx", "wb").write(dataset_bytes)
    from exp2.backend_hf import HFBackend
    be = HFBackend.load(MODEL_ID, REV, "cuda", torch.float32)   # the only model load in this function; reused by every stage
    ident = dict(stage=stage, split=split, limit=limit, model_id=MODEL_ID, revision=REV, commit_hash=be.commit_hash, snapshot_path=path,
                 file_sha256=shas, dataset_sha256=ds_sha, gpu=GPU, device_name=torch.cuda.get_device_name(0), torch=torch.__version__,
                 cuda=torch.version.cuda, tf32_matmul=torch.backends.cuda.matmul.allow_tf32, deterministic_algorithms=True)
    out = f"/tmp/out_{stage}"; os.makedirs(out, exist_ok=True); status = "PASS"
    if expected_sha and expected_sha != ds_sha: status = "FAIL"; ident["dataset_hash_mismatch"] = dict(expected=expected_sha, found=ds_sha)
    if stage == "validate":
        from exp2.run import load_dataset
        from exp2.validate_items import validate_pairs, select_distractors
        pairs, _, _ = load_dataset("/tmp/ds.xlsx", "main"); pp, _, _ = load_dataset("/tmp/ds.xlsx", "pilot"); pairs.update(pp)
        res = dict(identity=ident, dataset_sha256=ds_sha, pairs=validate_pairs(be, pairs))
        if os.path.exists("/root/exp2/pools.json"):
            pools = json.load(open("/root/exp2/pools.json")); res["pools_sha256"] = hashlib.sha256(open("/root/exp2/pools.json", "rb").read()).hexdigest()
            res["new_distractors"] = {k: select_distractors(be, k, v) for k, v in pools.items()}
        json.dump(res, open(f"{out}/validate.json", "w"), indent=1)
    if stage == "gate3":
        from exp2.gate3 import gate3_record
        g = gate3_record(be, tokenizer_json_path=f"{path}/tokenizer.json", toy=False)
        if g["status"] != "PASS": status = "FAIL"
        if status == "PASS":
            from exp2.run import main as run_main
            res = run_main(["--dataset", "/tmp/ds.xlsx", "--out", out, "--stage", "gate3", "--device", "cuda", "--limit", str(limit or 3),
                            "--pools", "/root/exp2/pools.json"] + (["--expected-dataset-sha256", expected_sha] if expected_sha else []), backend=be)
            meta = json.load(open(f"{out}/run_meta.json"))
            if meta["integrity_failures"]: status = "FAIL"; g["end_to_end_integrity_failures"] = meta["integrity_failures"]
        ident["gate3"] = g
    if stage in ("pilot", "main"):
        from exp2.run import main as run_main
        run_main(["--dataset", "/tmp/ds.xlsx", "--out", out, "--stage", stage, "--device", "cuda", "--pools", "/root/exp2/pools.json"]
                 + (["--expected-dataset-sha256", expected_sha] if expected_sha else []), backend=be)
    ident["status"] = status; ident["runtime_s"] = round(time.time() - t0, 1); ident["gpu_cost_usd_estimate"] = round(ident["runtime_s"] / 3600 * GPU_USD_PER_H, 3)
    json.dump(ident, open(f"{out}/{stage}_record.json", "w"), indent=1, default=str)
    files = {p.name: p.read_bytes() for p in pathlib.Path(out).iterdir()}
    if status != "PASS": files = {f"{stage}_record.json": files[f"{stage}_record.json"]}   # withhold results on failure
    return status, files

@app.local_entrypoint()
def main(dataset: str, stage: str, limit: int = 0, expected_sha: str = "", authorised: bool = False):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from exp2.stages import split_for, AUTHORISATION_REQUIRED, MODAL_STAGES
    if stage not in MODAL_STAGES: raise SystemExit(f"unknown stage {stage!r}; allowed: {MODAL_STAGES}")
    split_for(stage)
    if stage in AUTHORISATION_REQUIRED and not authorised:
        raise SystemExit(f"stage {stage!r} requires PI authorisation; rerun with --authorised once it is given")
    status, files = run.remote(open(dataset, "rb").read(), stage, limit, expected_sha)
    d = pathlib.Path("modal_out") / stage; d.mkdir(parents=True, exist_ok=True)
    for name, b in files.items(): (d / name).write_bytes(b)
    print(f"stage {stage}: {status}; wrote", sorted(files))
    if status != "PASS": raise SystemExit(1)
