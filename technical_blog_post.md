# Building a CPU-Friendly ASR Pipeline for Six East African Languages

*Flora Ugo — AfriVoices East Africa ASR Hackathon*

## The Challenge

AfriVoices East Africa: ASR Hackathon asks competitors to transcribe ~41,733 audio clips spanning six East African languages — Swahili, Kikuyu, Luo, Somali, Maasai, and Kalenjin — under a strict edge-deployment constraint: under 1 billion parameters, and capable of running on a device with 8GB RAM or less.

## Model Choice

I chose OpenAI's Whisper `tiny` (~39M parameters), used as-is with no fine-tuning. Whisper's strong multilingual pretraining made it a reasonable zero-shot baseline for low-resource East African languages, and its small footprint comfortably satisfies the edge-device requirement.

## Engineering Challenges

**Disk limits.** The full test set (`digitalumuganda/anv-test-data-nt`) totals roughly 50GB across 94 parquet files — well beyond Kaggle's ~19.5GB working-directory limit. Bulk-downloading the dataset caused a "No space left on device" crash. The fix was to stream one parquet file at a time via the Kaggle API, transcribe it, then delete it before moving to the next file.

**Session instability.** Kaggle sessions reset unpredictably, wiping `/kaggle/working`. I addressed this by checkpointing progress every 100 rows to a permanent Kaggle dataset, with a resume sequence that reconstructs the environment (including a `dataset-metadata.json` file, without which checkpoint pushes silently fail) at the start of every new session.

**GPU quota exhaustion.** With GPU hours exhausted for the week, the pipeline runs entirely on CPU (`fp16=False`), resetting weekly. This slows throughput but doesn't block progress.

**Submission format.** Early submissions failed with null-value errors. The root cause was a column naming mismatch — the script wrote a `transcription` column when the competition expects `prediction`, alongside `id` and `language`.

## Compliance Notes

No manual transcription or correction of test audio was used at any stage. Inference latency and RAM usage were logged throughout the run (`[perf]` / `[perf summary]` output) to support the accompanying hardware validation report.

## What's Next

With more GPU quota, a natural next step would be lightweight fine-tuning on the language-specific training data to improve Word Error Rate beyond the zero-shot baseline, while staying within the parameter and memory budget.
