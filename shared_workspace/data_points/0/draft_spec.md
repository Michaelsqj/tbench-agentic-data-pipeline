Idea #1:
- Title: Automated Debian Package Inventory for Compliance Snapshots
- Core Skill Match: Requires capturing the full list of installed packages via apt/dpkg tooling and exporting it deterministically, just like the seed task's focus on listing installed software.
- Difficulty: medium
- Why Different: Frames the task around generating an auditable compliance report with metadata, adding sorting, tagging, and timestamping requirements beyond just dumping package names.
- Tech Stack: Bash, dpkg-query, apt-mark, GNU coreutils
- Task Type: configuration automation

Task: Produce a reproducible inventory report of all installed Debian packages so a compliance bot can snapshot the container state without human intervention.
Instructions:
- Create an executable Bash script at `tools/generate_package_inventory.sh` that inspects the current system and writes `artifacts/package_inventory.csv`.
- The CSV must include a header `package,version,installation_state,recorded_at` and one row per installed package, using `dpkg-query`/`apt` data to populate the name and version.
- Mark each row's `installation_state` as `manual` if the package is currently marked as manually installed (`apt-mark showmanual`), otherwise `auto`.
- Set `recorded_at` to a single ISO-8601 timestamp (UTC) that is identical for every row and also echoed to stdout so the pipeline can capture it.
- Ensure the CSV rows are strictly sorted alphabetically by package name and that rerunning the script overwrites previous reports deterministically.
- If required tooling is missing, the script should fail with a clear error message rather than attempting installation.

Environment Setup: Ubuntu 22.04 base image with standard apt tooling; Bash, coreutils, and dpkg already available. No extra packages should be installed in setup.
Testing:
- Tests will run the script, then parse `artifacts/package_inventory.csv` to confirm the header, ordering, and presence of known base packages such as `bash` and `coreutils`.
- A separate test will verify that manual packages listed in a seeded `manual-packages.list` appear with the `installation_state` set to `manual`.
- Another test captures stdout to confirm the ISO-8601 timestamp format and checks that every row shares that exact value.
Difficulty: medium
Core Skills Tested: Linux package inspection, Bash scripting, deterministic file generation, data formatting
Key Technologies: Bash, dpkg-query, apt-mark, GNU coreutils
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

