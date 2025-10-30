Task: Manage Linux User Accounts via Command Line

Instructions: You are administering a Linux system and need to perform comprehensive user account management tasks. Your task is to: (1) list all local users on the system by parsing the /etc/passwd file, (2) add one or more new user accounts with appropriate home directories, (3) modify user properties such as username, group membership (including adding users to sudo group), and user details, (4) change passwords for specific users, and (5) remove/delete user accounts along with their home directories. Demonstrate understanding of various user management commands (adduser, useradd, userdel, usermod, passwd, chsh, chfn) and their differences.

Environment Setup: Ubuntu-based Docker container (Ubuntu 18.04 or newer) with standard user management utilities pre-installed. The system should start with a few existing user accounts to list, and provide a realistic /etc/passwd file. The container should have sudo privileges configured for the primary user to perform administrative tasks. Include the necessary utilities: adduser, useradd, userdel, usermod, passwd, chsh, chfn, and cut.

Testing: Python tests will verify: (1) that the agent can correctly list all local users by parsing /etc/passwd (using cut or similar), (2) that new users are successfully created with proper home directories in /home/, (3) that user modifications work correctly (username changes, group additions, particularly sudo group membership), (4) that password changes are applied (verifiable through shadow file or authentication tests), (5) that user deletion removes accounts from /etc/passwd, and (6) that home directories are properly deleted when users are removed. Tests should also verify the agent demonstrates understanding of when to use adduser vs useradd and proper handling of user group associations.

Difficulty: medium

Core Skills Tested: Linux user administration, understanding /etc/passwd structure, user management commands, sudo group management, file system operations for home directories, system security basics, command-line proficiency

Key Technologies: Linux user management tools (adduser, useradd, userdel, usermod, passwd, chsh, chfn), /etc/passwd, /etc/shadow, sudo, bash, Ubuntu/Debian system administration

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
