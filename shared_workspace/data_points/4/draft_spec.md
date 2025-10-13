Idea #5:
- Title: Offline .deb Installer with Health Check
- Core Skill Match: Still hinges on using `dpkg -i` and handling dependencies just like the original answer describes.
- Difficulty: medium
- Why Different: Frames the installation as part of an offline rollout pipeline that must detect missing dependencies and publish status artifacts.
- Tech Stack: Bash, dpkg, apt-get
- Task Type: deployment

Task: Deliver a deploy script that installs a local `.deb` payload, heals dependency issues, and records installation status for downstream jobs.
Instructions:
- Add an executable script `deploy/install_internal_tool.sh` that installs `artifacts/internal-tool_1.4.2.deb` using `dpkg -i`.
- On failure due to dependencies, the script must run `apt-get install -f` (or equivalent) and retry the installation once before giving up.
- After a successful install, query the system to confirm the package version and write `reports/internal_tool_status.json` with keys `package`, `version`, and `source` (set to `local-artifact`).
- The script must be safe to rerun: if the requested version is already installed, it should emit a message and exit 0 without reinstalling.
- Log all key actions to stdout so CI logs clearly show each step.

Environment Setup: Ubuntu 22.04 with Bash, dpkg, and apt tooling; the `.deb` artifact will be staged under `artifacts/` by the builder.
Testing:
- Tests will provide a fake `.deb`, execute the script, and then verify via `dpkg-query` that the package is installed and the JSON report contains the expected data.
- Dependency failure is simulated to confirm the script attempts `apt-get install -f` and retries exactly once.
- A final test runs the script twice to ensure the second invocation exits cleanly without reinstalling.
Difficulty: medium
Core Skills Tested: dpkg usage, dependency remediation, idempotent deployment scripting, status reporting
Key Technologies: Bash, dpkg, apt-get, jq (for tests to validate JSON)
title: How do I install a .deb file via the command line?
question_text: <p>How do I install a <code>.deb</code> file via the command line?</p>

answer_text: <p>Packages are <strong>manually</strong> installed via the <strong><code>dpkg</code></strong> command (Debian Package Management System). <code>dpkg</code> is the backend to commands like <code>apt-get</code> and <code>aptitude</code>, which in turn are the backend for GUI install apps like the Software Center and Synaptic.</p>

<p>Something along the lines of:</p>

<p><code>dpkg</code> --> <code>apt-get</code>, <code>aptitude</code> --> Synaptic, Software Center</p>

<p>But of course the easiest ways to install a package would be, first, the GUI apps (Synaptic, Software Center, etc..), followed by the terminal commands <code>apt-get</code> and <code>aptitude</code> that add a very nice user friendly approach to the backend dpkg, including but not limited to packaged dependencies, control over what is installed, needs update, not installed, broken packages, etc.. Lastly the <code>dpkg</code> command which is the base for all of them.</p>

<p>Since dpkg is the base, you can use it to install packaged directly from the command line.</p>

<h3>Install a package</h3>

<pre><code>sudo dpkg -i DEB_PACKAGE
</code></pre>

<p>For example if the package file is called <code>askubuntu_2.0.deb</code> then you should do <code>sudo dpkg -i askubuntu_2.0.deb</code>. If <code>dpkg</code> reports an error due to dependency problems, you can run <code>sudo apt-get install -f</code> to download the missing dependencies and configure everything. If that reports an error, you'll have to sort out the dependencies yourself by following for example <a href="https://askubuntu.com/questions/140246/how-do-i-resolve-unmet-dependencies">How do I resolve unmet dependencies after adding a PPA?</a>.</p>

<h3>Remove a package</h3>

<pre><code>sudo dpkg -r PACKAGE_NAME
</code></pre>

<p>For example if the package is called <code>askubuntu</code> then you should do <code>sudo dpkg -r askubuntu</code>.</p>

<h3>Reconfigure an existing package</h3>

<pre><code>sudo dpkg-reconfigure PACKAGE_NAME
</code></pre>

<p>This is useful when you need to reconfigure something related to said package. Some useful examples it the <code>keyboard-configuration</code> when you want to enable the <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Backspace</kbd> in order to reset the X server, so you would the following:</p>

<pre><code>sudo dpkg-reconfigure keyboard-configuration
</code></pre>

<p>Another great one is when you need to set the Timezone for a server or your local testing computer, so you use use the <code>tzdata</code> package:</p>

<pre><code>sudo dpkg-reconfigure tzdata
</code></pre>

