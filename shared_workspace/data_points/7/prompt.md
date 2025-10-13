Deliver an executable Bash script `reports/summarize_storage.sh` that profiles directory usage and raises alerts when soft quotas are exceeded.

Requirements:
- Read targets from `config/storage_targets.csv` (`path,quota_gb` with a header row). Paths may be absolute or relative to the repository root.
- For each path, gather its disk usage using `du` and produce `reports/storage_summary.tsv` containing columns: `path`, `human_usage`, `bytes_usage`, `quota_gb`.
- Sort the summary by descending `bytes_usage`.
- Generate `reports/storage_alerts.md` listing any paths exceeding their quota, including the overage amount in GB (one decimal) and the top three immediate subdirectories by size. Use `du --max-depth=<depth>` where `<depth>` defaults to 1 but can be overridden via the `MAX_DEPTH` environment variable.
- Exit non-zero if any configured path is missing, naming the offending path in the error output.
- Ensure reruns update both reports deterministically.
