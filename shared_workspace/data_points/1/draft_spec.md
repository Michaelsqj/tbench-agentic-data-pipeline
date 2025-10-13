Idea #2:
- Title: Release Zip Extraction with Verification Hooks
- Core Skill Match: Still revolves around using the unzip utility from the terminal while adding checks and structured output handling.
- Difficulty: medium
- Why Different: Places the extraction inside a release promotion workflow that requires dependency checks, logs, and idempotent behavior.
- Tech Stack: Bash, unzip, GNU coreutils
- Task Type: build/setup

Task: Automate the extraction of a signed release bundle so deploy jobs can unpack it into a staging directory with traceable output.
Instructions:
- Provide an executable script at `scripts/extract_release.sh` that unpacks `artifacts/current_release.zip` into `releases/current/`.
- Before extraction, the script must verify that `unzip` exists and exit with guidance on how to install it if missing.
- After extraction, generate `logs/extraction_report.txt` summarizing the number of files unpacked, the destination path, and a checksum of the bundle (`sha256sum`).
- Validate that a `manifest.json` exists inside the bundle and exit with a non-zero status if it is missing.
- The script should be safe to rerun: it must clear `releases/current/` only after confirming the new archive can be read, and then perform a clean extraction.

Environment Setup: Ubuntu 22.04 with Bash, coreutils, and unzip available (builder will preinstall unzip in Dockerfile if needed).
Testing:
- Tests will place a synthetic `current_release.zip`, run the script, and assert that files appear under `releases/current/` with the expected tree structure.
- Another test will read `logs/extraction_report.txt` to confirm it records the SHA256 checksum, file count, and path, and that rerunning regenerates the report without stale data.
- Failure-path tests will remove `manifest.json` from the archive to ensure the script exits non-zero with a clear message.
Difficulty: medium
Core Skills Tested: Command-line archive handling, preflight validation, idempotent scripting, logging
Key Technologies: Bash, unzip, sha256sum, GNU coreutils
title: How to unzip a zip file from the Terminal?
question_text: <p>Just downloaded a .zip file from the internet. I want to use the terminal to unzip the file. What is the correct way to do this?</p>

answer_text: <p>If the <code>unzip</code> command isn't already installed on your system (use <code>which unzip</code> to check), then run:</p>
<pre><code>sudo apt-get install unzip
</code></pre>
<p>After installing the unzip utility, if you want to extract to a particular destination folder, you can use:</p>
<pre><code>unzip file.zip -d destination_folder
</code></pre>
<p>If you want to extract to a directory with the same name as the zip in your current working directory, you can simply do:</p>
<pre><code>unzip file.zip
</code></pre>

