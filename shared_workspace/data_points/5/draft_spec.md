Idea #6:
- Title: Command Transcript Logger for Incident Response
- Core Skill Match: Directly exercises redirecting stdout/stderr from terminal commands into files, matching the seed concept.
- Difficulty: medium
- Why Different: Transforms the simple redirect into a reusable logging harness that captures multiple commands with structured summaries.
- Tech Stack: Bash, tee, coreutils
- Task Type: tooling

Task: Build a lightweight harness that executes a sequence of incident commands and captures their combined stdout/stderr into timestamped transcripts and a summary report.
Instructions:
- Implement `tools/run_and_capture.sh` that reads command lines from `commands/sequence.txt` (one per line, skipping blanks and comments).
- For each command, execute it, streaming stdout/stderr to the console while simultaneously logging both streams to `logs/<timestamp>_<command_index>.log` using `tee` or equivalent redirection.
- After all commands finish, create `logs/summary.md` documenting each command, its exit code, and the path to the corresponding log file.
- The script should stop execution if any command exits non-zero unless `ALLOW_FAILURES=true` is set in the environment, in which case it records the failure but continues.
- Ensure timestamps are monotonic (ISO-8601) so the summary can be diffed across runs.

Environment Setup: Ubuntu 22.04 with Bash and coreutils; no additional packages required.
Testing:
- Tests will seed commands that produce both stdout and stderr, run the harness, and assert the logs contain both streams in order.
- Another test toggles `ALLOW_FAILURES` to confirm the script continues on error and records the failure in `summary.md`.
- A determinism test reruns the harness to verify timestamps update and old log files are not overwritten unintentionally.
Difficulty: medium
Core Skills Tested: Shell redirection, robust script control flow, log organization, failure handling
Key Technologies: Bash, tee, date, coreutils
title: How do I save terminal output to a file?
question_text: <p>How do I save the output of a command to a file?</p>

<p>Is there a way without using any software? I would like to know how.</p>

answer_text: <p>Yes it is possible, just redirect the output (AKA <a href="https://en.wikipedia.org/wiki/Standard_streams#Standard_input_(stdin)" rel="noreferrer"><code>stdout</code></a>) to a file:</p>
<pre><code>SomeCommand &gt; SomeFile.txt  
</code></pre>
<p>Or if you want to append data:</p>
<pre><code>SomeCommand &gt;&gt; SomeFile.txt
</code></pre>
<p>If you want <a href="https://en.wikipedia.org/wiki/Standard_streams#Standard_error_.28stderr.29" rel="noreferrer"><code>stderr</code></a> as well use this:</p>
<pre><code>SomeCommand &amp;&gt; SomeFile.txt  
</code></pre>
<p>or this to append:</p>
<pre><code>SomeCommand &amp;&gt;&gt; SomeFile.txt  
</code></pre>
<p>if you want to have both <a href="https://en.wikipedia.org/wiki/Standard_streams#Standard_error_.28stderr.29" rel="noreferrer"><code>stderr</code></a> and output <em>displayed on the console <strong>and</strong> in a file</em> use this:</p>
<pre><code>SomeCommand 2&gt;&amp;1 | tee SomeFile.txt
</code></pre>
<p>(If you want the output only, drop the <code>2</code> above)</p>

