Create `tools/run_and_capture.sh`, an executable Bash harness that runs a sequence of shell commands listed in `commands/sequence.txt` and records transcripts for incident response.

Behaviour requirements:
- Read `commands/sequence.txt`, ignoring blank lines or lines beginning with `#`. Execute the remaining commands in order using the default shell.
- For each command, stream stdout/stderr to the console and simultaneously capture both streams to `logs/<ISO8601>_<index>.log` (timestamps should be unique per run). Indexing should start at 01.
- After executing the sequence, produce `logs/summary.md` that lists each command in order, its exit code, and the path to its log file.
- Stop on the first non-zero exit code unless the environment variable `ALLOW_FAILURES=true` is set, in which case continue while recording the failure in the summary.
- Ensure reruns create fresh log files and update the summary without truncating past log files from earlier runs.
- Exit non-zero if `commands/sequence.txt` is missing or contains no runnable commands.
