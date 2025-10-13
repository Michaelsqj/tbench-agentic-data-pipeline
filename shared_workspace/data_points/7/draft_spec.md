Idea #8:
- Title: Workspace Storage Budget Reporter
- Core Skill Match: Expands upon using `du` to compute directory sizes, keeping the same measurement skill at its core.
- Difficulty: hard
- Why Different: Turns a one-off check into a configurable reporting tool that aggregates multiple directories and enforces quota thresholds.
- Tech Stack: Bash, du, sort, awk
- Task Type: analytics/reporting

Task: Develop a reporting script that profiles configurable directories, calculates their disk usage, and flags any paths exceeding team quotas.
Instructions:
- Create `reports/summarize_storage.sh` that reads directory paths and soft quota limits (in GB) from `config/storage_targets.csv` (format: `path,quota_gb`).
- For each path, gather disk usage using `du` with human-readable output and a precise byte count, storing results in `reports/storage_summary.tsv` sorted from largest to smallest usage.
- Generate `reports/storage_alerts.md` listing any paths that exceed their quota, along with the overage amount and the top three largest immediate subdirectories (use `du --max-depth=1`).
- The script should allow overriding the max depth with an environment variable `MAX_DEPTH` and default to 1 when unset.
- Ensure the script exits non-zero if any configured path is missing, mentioning the offending path in stderr.

Environment Setup: Ubuntu 22.04 with Bash, coreutils, and GNU tools (`du`, `sort`, `awk`).
Testing:
- Tests will populate sample directories with files, run the script, and assert that the TSV is sorted and includes both human-readable and byte columns.
- Another test adjusts `MAX_DEPTH` to confirm the alert report uses the requested depth when sampling subdirectories.
- Missing-path handling is verified by pointing the config to a nonexistent directory and ensuring the script fails fast with a useful message.
Difficulty: hard
Core Skills Tested: Disk usage analysis, structured reporting, environment-aware scripting, error handling
Key Technologies: Bash, du, sort, awk, printf
title: How do I determine the total size of a directory (folder) from the command line?
question_text: <p>Is there a simple command to display the total aggregate size (disk usage) of all files in a directory (folder)?</p>

<p>I have tried these, and they don't do what I want:</p>

<ul>
<li><code>ls -l</code>, which only displays the size of the individual files in a directory, nor </li>
<li><code>df -h</code>, which only displays the free and used space on my disks.</li>
</ul>

answer_text: <p>The command <code>du</code> "summarizes disk usage of each FILE, recursively for directories," e.g.,</p>

<pre><code>du -hs /path/to/directory
</code></pre>

<ul>
<li><code>-h</code> is to get the numbers "human readable", e.g. get <code>140M</code> instead of <code>143260</code> (size in KBytes)</li>
<li><code>-s</code> is for summary (otherwise you'll get not only the size of the folder but also for everything <em>in</em> the folder separately)</li>
</ul>

<hr>

<p>As you're using <code>-h</code> you can sort the human readable values using</p>

<pre><code>du -h | sort -h
</code></pre>

<p>The <code>-h</code> flag on <code>sort</code> will consider "Human Readable" size values.</p>

<hr>

<p>If want to avoid recursively listing all files and directories, you can supply the <code>--max-depth</code> parameter to limit how many items are displayed. Most commonly, <code>--max-depth=1</code></p>

<pre><code>du -h --max-depth=1 /path/to/directory
</code></pre>

