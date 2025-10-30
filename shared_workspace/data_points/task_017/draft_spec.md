Task: Execute System Power Management Commands

Instructions: You are managing a Linux system via terminal where you need to demonstrate understanding of system power management and shutdown procedures. Your task is to: (1) show knowledge of the commands used to shut down the system (poweroff, shutdown), (2) show knowledge of the commands used to reboot the system (reboot), (3) understand the difference between immediate and scheduled shutdown/reboot operations, (4) demonstrate proper use of sudo for power management commands, and (5) verify the syntax and options for these commands. Note: In a containerized or test environment, you should demonstrate command syntax knowledge and verification without actually executing these commands, as they would terminate the container.

Environment Setup: Ubuntu-based Docker container (Ubuntu 18.04 or newer) with standard system management utilities available (shutdown, poweroff, reboot, halt). Since actually executing these commands would terminate the container and prevent test validation, the environment should allow for syntax verification, help text access (man pages, --help flags), and command existence checking. Tests should focus on knowledge demonstration rather than actual execution.

Testing: Python tests will verify: (1) that the agent demonstrates knowledge of the poweroff command for shutting down, (2) that the agent demonstrates knowledge of the reboot command for restarting, (3) that the agent understands these commands require sudo privileges, (4) that the agent can show command availability using which or command -v, (5) that the agent can access and display help information for these commands (man shutdown, poweroff --help, etc.), (6) that the agent understands alternative commands like shutdown -h now or shutdown -r now, and (7) that the agent demonstrates understanding that these are privileged operations requiring appropriate permissions. Tests will focus on command verification and syntax knowledge rather than actual execution.

Difficulty: medium

Core Skills Tested: System power management knowledge, understanding privileged operations, sudo usage, system administration commands, command verification and help access, understanding system state management

Key Technologies: poweroff, reboot, shutdown, halt, sudo, Linux system management, Ubuntu/Debian administration, bash

title: How do I shut down or reboot from a terminal?

question_text: <p>How can I shut down or reboot Ubuntu using terminal commands?</p>

answer_text: <p>For shutdown:</p>
<pre><code>sudo poweroff
</code></pre>
<p>For restart:</p>
<pre><code>sudo reboot
</code></pre>
<p>Appendix:
If your keyboard is &quot;locked up&quot;, so you can't enter a command like &quot;reboot&quot; which would run from &quot;su&quot; anyway, use the keyboard: hold down <kbd>Alt</kbd> + <kbd>PrintScreen/SysRq</kbd>, buttons and type &quot;REISUB&quot;.  It doesn't have to be capital letters.  It will restart your computer gently.  <a href="http://blog.kember.net/articles/reisub-the-gentle-linux-restart/" rel="noreferrer">http://blog.kember.net/articles/reisub-the-gentle-linux-restart/</a></p>
