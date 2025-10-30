Task: Extract Tar Archives to Specific Target Directories

Instructions: You are managing file archives on a Linux system where tar files need to be extracted to specific destination directories rather than the current working directory. Your task is to: (1) create target directories if they don't already exist, (2) extract one or more tar archives to specified target directories using the -C (or --directory) option with tar, (3) verify that the extracted contents are in the correct target locations, and (4) handle multiple archives being extracted to different destination directories. Demonstrate understanding of tar's directory specification and the importance of creating target directories before extraction.

Environment Setup: Ubuntu-based Docker container (Ubuntu 18.04 or newer) with tar utility pre-installed. The container should have several tar archive files (both compressed and uncompressed: .tar, .tar.gz, .tar.xz) placed in predefined locations. The file system should have various potential target directory locations. The container should allow directory creation and file extraction to different paths.

Testing: Python tests will verify: (1) that target directories are created using mkdir before extraction if they don't exist, (2) that tar archives are extracted using the -C or --directory option to specify target locations, (3) that extracted files and directories appear in the correct target locations (not the current directory), (4) that the -C option works with various archive formats (.tar, .tar.gz, .tar.xz), (5) that directory structures within archives are preserved in the target location, (6) that multiple archives can be extracted to different target directories, and (7) that the agent demonstrates proper sequencing (create directory, then extract to it).

Difficulty: medium

Core Skills Tested: Tar command proficiency, directory management, understanding tar extraction options, file system navigation, command-line flags usage, prerequisite checking (directory existence)

Key Technologies: tar, mkdir, bash, Linux file system operations, directory creation and management

title: How to extract files to another directory using 'tar' command?

question_text: <p>I thought <code>tar archive.tar /users/mylocation</code> would work, but it doesn't. How can I do that? </p>

answer_text: <p>To extract an archive to a directory different from the current, use the <code>-C</code>, or <code>--directory</code>, tar option, as in</p>

<pre><code>tar -xf archive.tar -C /target/directory
</code></pre>

<p>Note that the target directory has to exist before running that command (it can be created by <code>mkdir /target/directory</code>).</p>

<p>Read the <a href="http://manpages.ubuntu.com/tar.1">manual page</a> (command: <code>man tar</code>) for other options.</p>
