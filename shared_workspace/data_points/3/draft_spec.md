Idea #4:
- Title: PPA Retirement Automation with Downgrade Strategy
- Core Skill Match: Centers on removing PPAs and reversing their package changes using the same tooling highlighted in the source Q&A.
- Difficulty: hard
- Why Different: Expands the task into a controlled decommission workflow that inventories affected packages and documents the cleanup.
- Tech Stack: Bash, add-apt-repository, ppa-purge, apt-cache
- Task Type: maintenance automation

Task: Create an automation script that disentangles a deprecated vendor PPA, purges its packages, and leaves an auditable downgrade report.
Instructions:
- Write `maintenance/remove_vendor_ppa.sh` that reads the PPA reference from `config/vendor_ppa.txt` and removes it using `add-apt-repository --remove`.
- The script must ensure `ppa-purge` is installed (install it if absent), use it against the target PPA, and capture any packages that were downgraded or removed.
- Generate `reports/ppa_retirement_report.md` summarizing the actions, including the original `.list` file name, packages reverted, and commands executed.
- After purging, refresh apt metadata (`apt-get update`) and list any residual packages still installed from the PPA so operators know what manual steps remain.
- The script should be idempotent: rerunning it after the PPA is gone should produce a short report noting there was nothing to do.

Environment Setup: Ubuntu 22.04 with sudo access, apt tools, and network available to install `ppa-purge`. Builder will seed a dummy PPA entry under `etc/apt/sources.list.d/` for testing.
Testing:
- Tests will place a mock `.list` file, run the script, and then assert that file is removed and the report logs the downgrade commands.
- Another test seeds packages marked as coming from the PPA and verifies the report lists them after the purge.
- Idempotency is checked by rerunning the script and confirming the report reflects a no-op state.
Difficulty: hard
Core Skills Tested: Repository management, safe rollback planning, Bash automation, audit documentation
Key Technologies: Bash, add-apt-repository, ppa-purge, apt-cache
title: How can PPAs be removed?
question_text: <p>I've added many PPAs using the <code>add-apt-repository</code> command. Is there a simple way to remove these PPAs? I've checked in <code>/etc/apt/sources.list</code> for the appropriate deb lines but they aren't there. </p>

<p>This is on a server system so a command line solution would be great!</p>

answer_text: <p>There are a number of options:</p>
<ol>
<li><p>Use the <code>--remove</code> flag, similar to how the PPA was added:</p>
<pre><code>sudo add-apt-repository --remove ppa:whatever/ppa
</code></pre>
</li>
<li><p>You can also remove PPAs by deleting the <code>.list</code> files from <code>/etc/apt/sources.list.d</code> directory.</p>
</li>
<li><p>As a safer alternative, you can install ppa-purge:</p>
<pre><code>sudo apt-get install ppa-purge
</code></pre>
<p>And then remove the PPA, downgrading gracefully packages it provided to packages provided by official repositories:</p>
<pre><code>sudo ppa-purge ppa:whatever/ppa
</code></pre>
<p>Note that this will uninstall packages provided by the PPA, but not those provided by the official repositories. If you want to remove them, you should tell it to apt:</p>
<pre><code>sudo apt-get purge package_name
</code></pre>
</li>
<li><p>Last but not least, you can also disable or remove PPAs from the &quot;Software Sources&quot; section in Ubuntu Settings with a few clicks of your mouse (no terminal needed).</p>
</li>
</ol>

