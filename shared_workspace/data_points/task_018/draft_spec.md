Task: Fix Hostname Resolution Error in sudo Configuration

Instructions: You are troubleshooting a Linux system where sudo commands produce "unable to resolve host" errors and experience delays. Your task is to: (1) diagnose the hostname resolution issue by examining the /etc/hostname and /etc/hosts files, (2) identify the mismatch between the system hostname and the hosts file entries, (3) fix the /etc/hosts file to include the correct hostname mapping to 127.0.1.1 (or 127.0.0.1), (4) ensure the /etc/hostname file contains the proper system hostname, and (5) verify that sudo commands execute without the "unable to resolve host" error after the fix. Demonstrate understanding of Linux hostname resolution and the relationship between /etc/hostname and /etc/hosts.

Environment Setup: Ubuntu-based Docker container (Ubuntu 18.04 or newer) with a deliberately misconfigured hostname setup that causes the "sudo: unable to resolve host" error. The /etc/hostname file should contain a hostname (e.g., "my-machine" or "test-host"), but the /etc/hosts file should be missing the corresponding entry mapping that hostname to a loopback address (127.0.1.1). The container should have sudo configured and allow file editing. Include the standard localhost entry (127.0.0.1 localhost) in /etc/hosts but omit the machine-specific hostname entry.

Testing: Python tests will verify: (1) that the agent examines /etc/hostname to determine the system hostname, (2) that the agent checks /etc/hosts for hostname entries, (3) that the agent correctly identifies the missing or incorrect hostname mapping, (4) that /etc/hosts is modified to include the correct entry mapping the hostname to 127.0.1.1 (or adds it if missing), (5) that the /etc/hostname file contains the proper hostname, (6) that after the fix, sudo commands execute without the "unable to resolve host" error, and (7) that the agent demonstrates understanding of the relationship between these configuration files and hostname resolution.

Difficulty: medium

Core Skills Tested: System troubleshooting, hostname configuration, understanding /etc/hosts and /etc/hostname, sudo configuration issues, DNS/hostname resolution basics, file editing, diagnostic thinking

Key Technologies: /etc/hostname, /etc/hosts, sudo, hostname resolution, Linux system configuration, text file editing, Ubuntu/Debian administration

title: Error message "sudo: unable to resolve host (none)"

question_text: <p>When I run <code>sudo</code> the terminal is stuck for a few seconds and then outputs an error message. My terminal looks like this:</p>

<pre><code>ubuntu@(none):~$ sudo true
sudo: unable to resolve host (none)
</code></pre>

<p>What can I do to solve it?</p>

answer_text: <p>Two things to check (assuming your machine is called <code>my-machine</code>, you can change this as appropriate):</p>

<ol>
<li><p>That the <code>/etc/hostname</code> file contains just the name of the machine.</p></li>
<li><p>That <code>/etc/hosts</code> has an entry for <code>localhost</code>. It should have something like:</p>

<pre>
 127.0.0.1    localhost.localdomain localhost
 127.0.1.1    my-machine
</pre></li>
</ol>

<p>If either of these files aren't correct (since you can't sudo), you may have to reboot the machine into recovery mode and make the modifications, then reboot to your usual environment.</p>
