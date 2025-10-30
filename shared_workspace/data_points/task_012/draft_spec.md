Task: Manage Persistent Processes Using tmux Terminal Multiplexer

Instructions: You are working on a remote Linux server via SSH where you need to run long-running processes that must continue executing even after your SSH session terminates. Your task is to: (1) install or verify that tmux is available on the system, (2) start a new tmux session, (3) launch one or more long-running processes within the tmux session, (4) detach from the tmux session while keeping processes running, (5) list all active tmux sessions, (6) reattach to a previously detached tmux session to check process status, and (7) demonstrate understanding of named sessions by creating and managing multiple tmux sessions with distinct names.

Environment Setup: Ubuntu-based Docker container (Ubuntu 18.04 or newer) with tmux installed or available for installation via apt. The container should simulate a remote server environment with processes that can run in the background (e.g., long-running scripts, monitoring tasks, or data processing). Include scripts or commands that produce periodic output to demonstrate that processes continue running when detached.

Testing: Python tests will verify: (1) that tmux is installed and available on the system, (2) that a tmux session can be created and started, (3) that processes launched inside tmux continue running after detachment (verifiable by checking process lists or output files), (4) that tmux list-sessions (or tmux ls) correctly shows active sessions, (5) that sessions can be named and identified properly, (6) that reattachment to existing sessions works correctly, (7) that the detach key sequence (Ctrl+b d) functionality is understood and properly used, and (8) that multiple named sessions can be managed independently.

Difficulty: medium

Core Skills Tested: Terminal multiplexer usage, process persistence, SSH session management, tmux command proficiency, understanding detached sessions, managing multiple sessions, remote server administration

Key Technologies: tmux, SSH, Linux process management, terminal session persistence, bash

title: How to keep processes running after ending ssh session?

question_text: <p>Let's say I launch a bunch of processes from a ssh session. Is it possible to terminate the ssh session while keeping those processes running on the remote machine?</p>

answer_text: <p>You should look for modern alternatives like <code>tmux</code>.</p>
<p><code>tmux</code> is superior to <code>screen</code> for many reasons, here are just some examples:</p>
<ul>
<li>Windows can be moved between session and even linked to multiple sessions</li>
<li>Windows can be split horizontally and vertically into panes</li>
<li>Support for UTF-8 and 256 colour terminals</li>
<li>Sessions can be controlled from the shell without the need to enter a session</li>
</ul>
<h1>Basic Functionality</h1>
<p>To get the same functionality as explained in the <a href="https://askubuntu.com/a/8657/53508">answer</a> recommending <code>screen</code>, you would need to do the following:</p>
<ul>
<li>ssh into the remote machine</li>
<li>start <code>tmux</code> by typing <code>tmux</code> into the shell</li>
<li>start the process you want inside the started <code>tmux</code> session</li>
<li>leave/detach the <code>tmux</code> session by typing <kbd>Ctrl</kbd>+<kbd>b</kbd> and then <kbd>d</kbd></li>
</ul>
<p>You can now safely log off from the remote machine, your process will keep running inside <code>tmux</code>. When you come back again and want to check the status of your process you can use <code>tmux attach</code> to attach to your <code>tmux</code> session.</p>
<p>If you want to have multiple sessions running side-by-side, you should name each session using <kbd>Ctrl</kbd>+<kbd>b</kbd> and <code>$</code>. You can get a list of the currently running sessions using <code>tmux list-sessions</code> or simply <code>tmux ls</code>, now attach to a running session with command <code>tmux attach-session -t &lt;session-name&gt;</code>.</p>
<p><code>tmux</code> can do much more advanced things than handle a single window in a single session. For more information have a look in <code>man tmux</code> or <a href="http://tmux.github.io/" rel="noreferrer">the tmux GitHub page</a>. In particular, <a href="https://github.com/tmux/tmux/wiki/FAQ" rel="noreferrer">here's an FAQ</a> about the main differences between <code>screen</code> and <code>tmux</code>.</p>
