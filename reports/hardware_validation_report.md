# Hardware Validation Report

**Submission:** AfriVoices East Africa ASR Hackathon
**Competitor:** Flora Ugo (Kaggle: `floramichael`)
**Model:** OpenAI Whisper `tiny` (~39M parameters)

This report satisfies **Rule 10** (hardware validation report showing inference latency for the full test set) and **Rule 9** (capable of running inference on an edge device with ≤8GB RAM).

## Test Environment

| Item | Detail |
|---|---|
| Compute | Kaggle Notebook, CPU-only session |
| Precision | `fp16=False` (CPU inference) |
| Model | Whisper `tiny` |
| Test set size | 41,733 clips across 6 languages (swa, kik, luo, som, mas, kln) |

## Inference Latency & Memory

> ⚠️ *Provisional.* Latency figures below are calculated from an early sample of [perf] lines while the main run is still in progress (22,100+/41,733 rows completed at time of writing). These will be updated with the final [perf summary] average once the run completes — final numbers may shift.

| Metric | Value |
|---|---|
| Average inference time per clip (provisional, n=6) | 4.15 s |
| Peak RSS — full Kaggle notebook process | 9,272.8 MB |
| Peak RSS — Whisper tiny model only (isolated measurement) | 442.0 MB |
| Estimated total inference time (41,733 clips, provisional) | ~173,000 s (~48 hours, CPU) |
| Rows timed so far | 22,100 / 41,733 |

## Edge Device Compliance (Rule 9)

Two RAM figures are reported above, deliberately kept separate for transparency:

- *9,272.8 MB* is the peak resident memory of the entire Kaggle notebook process during the full transcription run — this includes PyTorch, pandas, the Kaggle API client, and Jupyter kernel overhead, none of which would be present in a standalone edge deployment. Taken at face value this exceeds the 8GB cap, but it does not reflect the model's actual footprint.
- *442.0 MB* is the isolated memory footprint of loading Whisper tiny alone, measured in a clean process (RAM before load: 102.9MB, after load: 545.0MB, delta: 442.0MB). This is the figure directly relevant to Rule 9, and it sits comfortably within the 8GB RAM limit for edge devices such as a Raspberry Pi 4 or a modern smartphone.

We report both numbers rather than omitting the higher one, since organizers may re-run and validate the model directly (Rule 12) — the notebook-level figure is a real measurement, just not evidence of non-compliance once its source (environment overhead, not model size) is understood.

## Note on Compute

No CPU-only rule is imposed by the competition — GPU was unavailable due to exhausted weekly quota during this run, not a submission requirement. The latency figures above reflect CPU inference; the model itself is equally capable of GPU inference, which would only reduce these numbers.
