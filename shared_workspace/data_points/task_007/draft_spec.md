Task: Calculate and Report Directory Disk Usage with du Command

Instructions: You are analyzing disk space usage on a Linux system with multiple directories containing various files and subdirectories. Your task is to: (1) calculate the total disk usage of specific directories using the du command with human-readable output, (2) generate a summary report showing the aggregate size of directories without listing individual files recursively, (3) create a sorted list of subdirectories by size to identify the largest space consumers, and (4) use the --max-depth parameter to control the level of detail in directory size reporting. Save the results to output files for review.

Environment Setup: Ubuntu-based Docker container (Ubuntu 18.04 or newer) with a pre-configured directory structure containing multiple levels of nested directories and files of varying sizes (ranging from small text files to larger binary files). Create a realistic file system hierarchy with directories of different sizes (KB, MB, GB scale) to simulate real-world disk usage scenarios.

Testing: Python tests will verify: (1) that the du command is used with appropriate flags (-h for human-readable, -s for summary), (2) that the output correctly shows total directory sizes in human-readable format (KB, MB, GB), (3) that when sorting is applied, directories are correctly ordered by size using sort -h, (4) that --max-depth parameter is used appropriately to limit recursion depth and show subdirectory sizes, (5) that the reported sizes are accurate within a reasonable margin (accounting for filesystem overhead), and (6) that output is saved to files with proper formatting for analysis.

Difficulty: medium

Core Skills Tested: Linux disk usage analysis, du command proficiency, understanding human-readable output formatting, sorting and filtering command output, piping commands, filesystem analysis, report generation

Key Technologies: du command, sort, bash piping, Linux filesystem utilities, command-line output formatting

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
