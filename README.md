# AfriVoices East Africa ASR Pipeline

A speech-to-text pipeline built for the **AfriVoices East Africa: ASR Hackathon**, transcribing audio clips across six East African languages using OpenAI's Whisper (`tiny`).

## Overview

This repository contains the full inference pipeline used to generate the competition submission, covering:

- Swahili (`swa`)
- Kikuyu (`kik`)
- Luo (`luo`)
- Somali (`som`)
- Maasai (`mas`)
- Kalenjin (`kln`)

## Model

- **Base model:** OpenAI Whisper `tiny` (~39M parameters), used unmodified (no fine-tuning)
- **Parameter count:** well under the 1 billion parameter cap (**Rule 8**)
- **Precision:** `fp16=False`, CPU inference
- **Edge compatibility:** capable of running on devices with ≤8GB RAM, such as a Raspberry Pi 4 or a modern smartphone (**Rule 9**)

## Dataset

Test data sourced from `digitalumuganda/anv-test-data-nt` (94 parquet files, ~50GB), structured as `/{lang_code}/Scripted/` and `/{lang_code}/Unscripted/`. The dataset and any accompanying model/data cards are included per **Rule 7**.

## Pipeline

Because the full 50GB test set exceeds Kaggle's working-directory disk limit, files are streamed and processed **one parquet file at a time**:

1. Download a single parquet file via the Kaggle Python API (`api.dataset_download_file`)
2. Transcribe each row with Whisper `tiny`
3. Delete the file once processed
4. Move to the next file

Progress checkpoints every 100 rows to a permanent Kaggle dataset, so the run can resume cleanly after session interruptions.

Submission CSV columns: `id`, `language`, `prediction`.

## No Manual Transcription

All transcriptions are model-generated. No manual transcription or human correction of test audio was performed, in compliance with **Rule 3**.

## Reproducibility

No trained model weights are distributed separately, since this submission uses the unmodified, publicly available Whisper `tiny` checkpoint rather than a fine-tuned model. Training/inference logs are captured via the `[perf]` and `[perf summary]` print statements in the script and reproduced in the hardware validation report, in compliance with **Rule 6**.

## License

Released under the MIT License — see [`LICENSE`](./LICENSE) — in compliance with the competition's permissive open-source licensing requirement (**Rule 4**).

## Additional Deliverables

- [Hardware Validation Report](./reports/hardware_validation_report.md) — inference latency and RAM usage across the full test set (**Rule 10**)
- [Technical Blog Post](./technical_blog_post.md) — approach writeup (**Rule 5**)

## Author

Flora Ugo — Kaggle: `floramichael`
