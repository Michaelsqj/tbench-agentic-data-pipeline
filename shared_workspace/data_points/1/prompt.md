Operations needs an idempotent extraction step for staged releases. Write an executable Bash script at `scripts/extract_release.sh` that unpacks `artifacts/current_release.zip` into `releases/current/` and records what happened.

The script must:
- Verify that the `unzip` command is available; if not, exit non-zero with a clear message describing how to install it.
- Refuse to proceed if `artifacts/current_release.zip` is missing or unreadable.
- Extract the archive into a fresh `releases/current/` directory. The script should only remove the previous directory after confirming the archive can be read.
- Ensure a `manifest.json` file exists inside the archive; abort with a descriptive error if it is missing.
- After a successful extraction, write `logs/extraction_report.txt` containing the SHA256 of the zip, the number of files extracted, and the absolute path to the destination directory (one item per line).
- Make the script safe to rerun: running it twice should produce identical results without leftover files from prior runs.
