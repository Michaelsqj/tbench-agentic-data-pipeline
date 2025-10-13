Idea #11:
- Title: Chroot-Based User Lifecycle Orchestrator
- Core Skill Match: Covers listing, adding, deleting, and modifying users exactly as in the original Q&A, but within a scripted automation context.
- Difficulty: extremely hard
- Why Different: Demands a full lifecycle workflow that reads desired state, applies it to a chroot environment with standard user management commands, and produces an audit trail.
- Tech Stack: Bash, useradd/userdel/usermod, awk, jq
- Task Type: systems automation

Task: Design a user management orchestrator that applies declarative account changes to an isolated chroot and emits an auditable report of all account operations.
Instructions:
- Create `admin/apply_user_state.sh` that reads `config/user_operations.yaml` describing users to create, delete, modify, or group-assign within the provided `mock_root/` chroot.
- Use standard tools (`useradd`, `userdel`, `usermod`, `chsh`, etc.) with the `--root mock_root` flag so changes only affect the simulated environment.
- After applying the desired state, regenerate `reports/user_audit.json` summarizing existing accounts (username, shell, primary group, supplemental groups) and noting which actions were taken in this run.
- The script must support dry-run mode (`--plan-only`) that prints the actions it would execute without modifying the chroot, and it should be idempotent when run repeatedly with the same config.
- Handle home directory management: create homes under `mock_root/home/` for new users, and delete homes for users removed when `remove_home: true` is set in the YAML.

Environment Setup: Ubuntu 22.04 with Bash, coreutils, GNU user management tools, and Python available for tests; builder will provide a seeded `mock_root/` hierarchy and an example YAML file.
Testing:
- Tests will seed desired user operations, run the script, and inspect the simulated `/etc/passwd` and `/etc/group` under `mock_root` to validate changes.
- Another test exercises the `--plan-only` mode to ensure no files change while the planned actions are reported.
- Audit JSON output is parsed to confirm it lists actions taken and accurately reflects the final state of all accounts.
Difficulty: extremely hard
Core Skills Tested: User lifecycle management, declarative automation, chroot-safe scripting, idempotency
Key Technologies: Bash, useradd, userdel, usermod, chsh, jq, yq or python for YAML parsing
title: Is there a command to list all users? Also to add, delete, modify users, in the terminal?
question_text: <p>I need a command to list all users as well as commands to add, delete and modify users from terminal - any commands that could help in administrating user accounts easily by terminal.</p>

answer_text: <h3>To list</h3>

<p>To list all <strong><em>local</em></strong> users you can use:</p>

<pre><code>cut -d: -f1 /etc/passwd
</code></pre>

<p>To list all users capable of authenticating (in some way), including non-local, see <a href="https://askubuntu.com/a/414561/571941">this reply</a>.</p>

<p>Some more useful user-management commands (also limited to <strong><em>local</em></strong> users):</p>

<h3>To add</h3>

<p>To add a new user you can use:</p>

<pre><code>sudo adduser <em>new_username</em></code></pre>

<p>or:</p>

<pre><code>sudo useradd <em>new_username</em></code></pre>

<p>See also: <a href="https://askubuntu.com/q/345974/147044">What is the difference between adduser and useradd?</a></p>

<h3>To remove/delete</h3>

<p>To remove/delete a user, first you can use:</p>

<pre><code>sudo userdel <em>username</em></code></pre>

<p>Then you may want to delete the home directory for the deleted user account :</p>

<pre>sudo rm -r /home/<em>username</em></pre>

<p><sup>Please use with caution the above command!</sup></p>

<h3>To modify</h3>

<p>To modify the username of a user:</p>

<pre><code>usermod -l <em>new_username</em> <em>old_username</em></code></pre>

<p>To change the password for a user:</p>

<pre><code>sudo passwd <em>username</em></code></pre>

<p>To change the shell for a user:</p>

<pre><code>sudo chsh <em>username</em></code></pre>

<p>To change the details for a user (for example real name):</p>

<pre><code>sudo chfn <em>username</em></code></pre>

<p>To add a user to the <code>sudo</code> group: </p>

<pre><code>adduser <em>username</em> sudo</code></pre>

<p>or</p>

<pre><code>usermod -aG sudo <em>username</em></code></pre>

<p>And, of course, see also: <code>man adduser</code>, <code>man useradd</code>, <code>man userdel</code>... and so on.</p>

