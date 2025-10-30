Task: Extract and Document System Package Inventory

Instructions: You are given a Linux system with various packages installed. Your task is to extract a comprehensive list of all installed packages on the system, filter out any deinstalled packages, and save this inventory to a specific output file location. The output should be in a format that can be easily reviewed and potentially used for replicating the package setup on another system. Additionally, demonstrate the ability to search for and extract information about specific packages by name pattern.

Environment Setup: Ubuntu-based Docker container (Ubuntu 18.04 or newer) with a variety of pre-installed packages including system utilities, development tools, and application packages. The container should have dpkg and apt package management tools available.

Testing: Python tests will verify: (1) that a complete package list file is created at the specified output location with proper formatting, (2) that the output correctly excludes deinstalled packages, (3) that the output contains expected system packages (like bash, coreutils, etc.), (4) that a separate query can successfully filter and identify specific packages by name pattern (e.g., finding all Python-related packages), and (5) that the output format is parseable and contains standard dpkg package information fields.

Difficulty: medium

Core Skills Tested: Linux system administration, package management understanding, command-line proficiency, file I/O operations, text filtering and processing, grep and shell piping, understanding package states

Key Technologies: Ubuntu/Debian Linux, dpkg, apt, bash, grep, file redirection

title: How to list all installed packages

question_text: <p>I'd like to output a list of all installed packages into a text file so that I can review it and bulk-install on another system.  How would I do this?</p>

answer_text: <h1>Ubuntu 14.04 and above</h1>
<p>The <code>apt</code> tool on Ubuntu 14.04 and above makes this very easy.</p>
<pre><code>apt list --installed
</code></pre>
<hr />
<h1>Older Versions</h1>
<p>To get a list of packages installed locally do this in your terminal:</p>

<pre class="lang-bash prettyprint-override"><code>dpkg --get-selections | grep -v deinstall
</code></pre>
<p><sup>(The <code>-v</code> tag &quot;inverts&quot; grep to return non-matching lines)</sup></p>
<p>To get a list of a specific package installed:</p>
<pre class="lang-bash prettyprint-override"><code>dpkg --get-selections | grep postgres
</code></pre>
<p>To save that list to a text file called <code>packages</code> on your desktop do this in your terminal:</p>
<pre class="lang-bash prettyprint-override"><code>dpkg --get-selections | grep -v deinstall &gt; ~/Desktop/packages
</code></pre>
<p>Alternatively, simply use</p>
<pre class="lang-bash prettyprint-override"><code>dpkg -l
</code></pre>
<p><em>(you don't need to run any of these commands as the superuser, so no <code>sudo</code> or any other variants necessary here)</em></p>
