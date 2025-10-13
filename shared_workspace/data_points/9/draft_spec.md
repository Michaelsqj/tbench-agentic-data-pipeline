Idea #10:
- Title: Node Runtime Upgrade Automation with `n`
- Core Skill Match: Uses the npm `n` module to manage Node versions, exactly like the original solution path.
- Difficulty: hard
- Why Different: Wraps the manual upgrade into a repeatable script that reads target versions from config, applies them, and validates PATH fixes.
- Tech Stack: Bash, npm, n, Node.js
- Task Type: runtime management

Task: Automate Node.js upgrades for CI runners by reading a desired version, orchestrating `n` installations, and validating the resulting runtime environment.
Instructions:
- Implement `runtime/upgrade_node.sh` that reads a semantic version (e.g., `18.17.1`) from `config/node_version.txt` and ensures that version is active using the `n` module.
- If `n` is not installed globally, the script must install it via npm. It should also repair the legacy `/usr/bin/node` symlink when required.
- After switching versions, run `node --version` and `npm --version`, capturing both outputs in `reports/node_upgrade.log` together with the actions taken.
- Provide a rollback flag `--rollback <version>` that switches back to the specified version if present in the `n` cache and records the reversal in the same log.
- The script should verify that the active version matches the requested one and exit non-zero with guidance if it cannot be met (e.g., due to missing cache entries in rollback mode).

Environment Setup: Ubuntu 22.04 with npm and Node preinstalled; the builder will layer the base image so the agent can install/execute `n`.
Testing:
- Tests will set target versions, execute the script, and assert via `node --version` that the runtime matches the requested version, also verifying log contents.
- Additional tests cover fresh installs (ensuring `n` gets installed) and rollback flows where a cached version is restored.
- Error handling is validated by requesting a missing rollback version and checking the script exits non-zero with a helpful message.
Difficulty: hard
Core Skills Tested: Runtime version management, scripting with npm/n, rollback planning, log generation
Key Technologies: Bash, npm, n, Node.js
title: How can I update my nodeJS to the latest version?
question_text: <p>I have installed nodeJS on Ubuntu with following code </p>

<pre><code>sudo apt-get install nodejs
</code></pre>

<p>Since I am a new user for ubuntu I also ran this code too</p>

<pre><code>sudo apt-get install npm
</code></pre>

<p>Now when I type </p>

<pre><code> nodejs --version
</code></pre>

<p>It shows </p>

<pre><code>v0.6.19
</code></pre>

<p>I checked and saw latest nodeJS version is <code>0.10.26</code> </p>

<p>How can I update my version of nodeJS to <code>0.10.26</code>?</p>

<p>I tried with </p>

<pre><code> sudo apt-get install &lt;packagename&gt;
 sudo apt-get install --only-upgrade &lt;packagename&gt;
</code></pre>

<p>but no luck.</p>

answer_text: <p>Use <a href="https://www.npmjs.com/package/n" rel="noreferrer">n module from npm</a> in order to upgrade node</p>
<pre><code>sudo npm cache clean -f
sudo npm install -g n
sudo n stable
</code></pre>
<p>To upgrade to latest version (and not current stable) version, you can use</p>
<pre><code>sudo n latest
</code></pre>
<ul>
<li><p>Fix PATH:</p>
<pre><code>  sudo apt-get install --reinstall nodejs-legacy     # fix /usr/bin/node
</code></pre>
</li>
<li><p>To undo:</p>
<pre><code>  sudo n rm 6.0.0     # replace number with version of Node that was installed
  sudo npm uninstall -g n
</code></pre>
</li>
</ul>
<p>You may need to restart your terminal to see the updated node version.</p>
<p>Found in <a href="http://davidwalsh.name/upgrade-nodejs" rel="noreferrer">David Walsh blog</a></p>

