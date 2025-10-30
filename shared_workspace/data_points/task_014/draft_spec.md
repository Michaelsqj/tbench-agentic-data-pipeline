Task: Create User with Sudo Privileges and Manage Administrative Groups

Instructions: You are setting up a Linux system where you need to create new user accounts with administrative privileges. Your task is to: (1) create a new user account using adduser, (2) add the newly created user to the sudo group to grant sudo privileges, (3) verify that the user is a member of the sudo group, (4) optionally add the user to other common administrative groups (adm, lpadmin, sambashare) as appropriate for an administrator account, (5) verify that the /etc/sudoers configuration grants sudo permissions to the sudo group members, and (6) test that the new user has functional sudo access. Demonstrate understanding of Linux group-based permission management and the relationship between group membership and sudo privileges.

Environment Setup: Ubuntu-based Docker container (Ubuntu 18.04 or newer) with standard user management utilities (adduser, usermod) and sudo pre-configured. The /etc/sudoers file should have the standard configuration granting permissions to the sudo group (%sudo ALL=(ALL:ALL) ALL). The container should allow creation of users and group modifications. Include utilities to test sudo access and verify group membership (groups command, id command).

Testing: Python tests will verify: (1) that a new user account is successfully created using adduser, (2) that the user is added to the sudo group using adduser <username> sudo or usermod -aG sudo <username>, (3) that the user's group membership includes sudo (verifiable via groups command or /etc/group), (4) that /etc/sudoers contains the standard sudo group permission line, (5) that the user is optionally added to other administrative groups (adm, lpadmin, sambashare) if appropriate, (6) that the user can execute sudo commands (by testing with a simple sudo command execution), and (7) that the agent demonstrates understanding that group changes take effect on next login.

Difficulty: medium

Core Skills Tested: Linux user administration, sudo configuration, group-based permissions, understanding /etc/sudoers, user privilege management, system security basics, administrative account setup

Key Technologies: adduser, usermod, sudo, Linux groups, /etc/sudoers, /etc/group, Ubuntu/Debian user management, bash

title: How can I add a user as a new sudoer using the command line?

question_text: <p>After I add a user using <code>adduser</code>, I can't see it via <strong>System > Administration > Users and Groups</strong> unless I log out and then log in again. Is that normal?</p>

<p>Also, can I set a newly added user as a <code>sudo</code>er or do I have to change that only after adding it? How can I do that via the shell?</p>

<p>Finally, can I delete the original user that was created upon initial installation of Ubuntu, or is this user somehow 'special'?</p>

answer_text: <p>Just <a href="https://help.ubuntu.com/community/RootSudo#Allowing_other_users_to_run_sudo">add the user to the <code>sudo</code> group</a>:</p>

<pre><code>sudo adduser &lt;username&gt; sudo
</code></pre>

<p>The change will take effect the next time the user logs in.</p>

<p>This works because <code>/etc/sudoers</code> is pre-configured to grant permissions to all members of this group (You should not have to make any changes to this):</p>

<pre><code># Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) ALL
</code></pre>

<p>As long as you have access to a user that is in the same groups as your "original" user, you can delete the old one.</p>

<hr>

<p>Realistically, there are also other groups your new user should be a member of. If you set the Account type of a user to Administrator in Users Settings, it will be placed in at least all of these groups:</p>

<pre><code>adm sudo lpadmin sambashare
</code></pre>

<p>Because your system configuration may vary, I suggest taking a look at the output of <code>groups &lt;username&gt;</code> to see what groups are normally in use.</p>
