Author an executable Bash utility `scripts/extract_dataset.sh` that unpacks `.tar.gz` archives into staging directories with integrity reporting.

Requirements:
- Accept optional `--archive <path>` and `--dest <path>` arguments. Default to `artifacts/media_bundle.tar.gz` and `staging/media/` respectively.
- Abort with a clear message if the archive does not exist or is not readable.
- Before extracting, create a temporary directory and only replace the destination when the extraction succeeds. The final destination must not contain stale files from earlier runs.
- Use `tar -xvzf` to extract the archive. After extraction, generate `staging/media_checksums.txt` containing `sha256sum` values for every extracted file (paths relative to the destination root).
- Create `logs/extraction_summary.json` holding `archive`, `destination`, `file_count`, and `total_bytes` (sum of file sizes in bytes).
- On failure, clean up any partially extracted data and return a non-zero exit code.
