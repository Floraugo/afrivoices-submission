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

> ⚠️ **PLACEHOLDER — replace before submitting.** The figures below need to come from the `[perf]` / `[perf summary]` lines your instrumented script is printing. Send over your full timing log (not just a snippet) once the run completes, or a recent batch of `[perf]` lines, and I'll calculate the real averages here.

| Metric | Value |
|---|---|
| Average inference time per clip | `[INSERT avg_time]` s |
| Peak RAM usage during inference | `[INSERT peak_ram]` MB |
| Estimated total inference time (41,733 clips) | `[avg_time × 41,733]` |
| Rows timed this session | `[INSERT count]` |

## Edge Device Compliance (Rule 9)

Whisper `tiny` has ~39M parameters and a memory footprint well under 8GB RAM even accounting for runtime overhead, meaning it is compatible with edge devices such as a Raspberry Pi 4 or a modern smartphone. Peak RAM recorded during this CPU-only Kaggle run (see table above) reflects the notebook environment; on a dedicated edge device with no other processes competing for memory, footprint would be equal or lower.

## Note on Compute

No CPU-only rule is imposed by the competition — GPU was unavailable due to exhausted weekly quota during this run, not a submission requirement. The latency figures above reflect CPU inference; the model itself is equally capable of GPU inference, which would only reduce these numbers.
