"""
AfriVoices East Africa ASR Hackathon — Transcription Pipeline
Competitor: Flora Ugo (Kaggle: floramichael)

Downloads test parquet files one at a time (avoids Kaggle's ~19.5GB disk
limit), transcribes with Whisper `tiny` on CPU, checkpoints every 100 rows,
and logs per-clip inference latency + RAM usage for the hardware
validation report (Rule 10).
"""

import os
import io
import time
import json
import psutil
import whisper
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DATASET = "digitalumuganda/anv-test-data-nt"
CHECKPOINT_DATASET = "floramichael/afrivoices-checkpoint-v3"
CHECKPOINT_PATH = "/kaggle/working/checkpoint_v3.csv"
WORKING_DIR = "/kaggle/working"
LANG_MAP = {"swa": "sw", "kik": "sw", "luo": "sw", "som": "so", "mas": "sw", "kln": "sw"}

api = KaggleApi()
api.authenticate()

model = whisper.load_model("tiny")

# ---------------------------------------------------------------------------
# Resume from checkpoint if it exists
# ---------------------------------------------------------------------------
if os.path.exists(CHECKPOINT_PATH):
    results_df = pd.read_csv(CHECKPOINT_PATH)
    done_ids = set(results_df["id"])
    print(f"Resuming from checkpoint: {len(done_ids)} rows already done")
else:
    results_df = pd.DataFrame(columns=["id", "language", "prediction"])
    done_ids = set()

timing_log = []

# ---------------------------------------------------------------------------
# Discover all parquet files (os.walk — glob is unreliable on this path)
# ---------------------------------------------------------------------------
files = api.dataset_list_files(DATASET, page_size=200).files
parquet_files = [f.name for f in files if f.name.endswith(".parquet")]
print(f"Found {len(parquet_files)} parquet files")

# ---------------------------------------------------------------------------
# Main loop: one file at a time to avoid disk overflow
# ---------------------------------------------------------------------------
row_counter = 0

for pq_name in parquet_files:
    local_path = os.path.join(WORKING_DIR, os.path.basename(pq_name))
    api.dataset_download_file(DATASET, pq_name, path=WORKING_DIR, force=True)

    df = pd.read_parquet(local_path)
    lang = pq_name.split("/")[0]

    for _, row in df.iterrows():
        row_id = row["id"]
        if row_id in done_ids:
            continue

        start = time.time()
        audio_bytes = row["audio"]["bytes"]

        tmp_wav = "/kaggle/working/_tmp.wav"
        with open(tmp_wav, "wb") as f:
            f.write(audio_bytes)

        try:
            result = model.transcribe(tmp_wav, language=LANG_MAP.get(lang, "sw"), fp16=False)
            prediction = result["text"].strip()
        except Exception as e:
            print(f"[warn] failed on {row_id}: {e}")
            prediction = ""

        elapsed_seconds = time.time() - start
        ram_mb = psutil.Process(os.getpid()).memory_info().rss / (1024 ** 2)
        timing_log.append({"id": row_id, "elapsed_seconds": elapsed_seconds, "ram_mb": ram_mb})

        results_df.loc[len(results_df)] = [row_id, lang, prediction]
        done_ids.add(row_id)
        row_counter += 1

        if row_counter % 25 == 0:
            print(f"[perf] rows={row_counter} last_elapsed={elapsed_seconds:.3f}s ram={ram_mb:.1f}MB")

        if row_counter % 100 == 0:
            results_df.to_csv(CHECKPOINT_PATH, index=False)
            os.makedirs(WORKING_DIR, exist_ok=True)
            with open(os.path.join(WORKING_DIR, "dataset-metadata.json"), "w") as f:
                json.dump({
                    "title": "afrivoices-checkpoint-v3",
                    "id": CHECKPOINT_DATASET,
                    "licenses": [{"name": "CC0-1.0"}]
                }, f)
            os.system(f"kaggle datasets version -p {WORKING_DIR} -m 'checkpoint update' --dir-mode skip")
            print(f"[checkpoint] pushed at {row_counter} rows")

    os.remove(local_path)  # delete parquet immediately — avoids disk overflow

# ---------------------------------------------------------------------------
# Final save + perf summary
# ---------------------------------------------------------------------------
results_df.to_csv(CHECKPOINT_PATH, index=False)
results_df.to_csv("/kaggle/working/submission.csv", index=False)

if timing_log:
    avg_time = sum(t["elapsed_seconds"] for t in timing_log) / len(timing_log)
    peak_ram = max(t["ram_mb"] for t in timing_log)
    print(f"[perf summary] avg_time_per_clip={avg_time:.3f}s peak_ram={peak_ram:.1f}MB rows={len(timing_log)}")

print(f"Done. Total rows transcribed: {len(results_df)}")
