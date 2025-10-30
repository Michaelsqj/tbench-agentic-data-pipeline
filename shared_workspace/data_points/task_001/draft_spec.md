Task: Extract Compressed Archive Files

Instructions: You are working on a system where multiple .zip archive files need to be extracted. Your task is to: (1) ensure the necessary extraction utilities are available on the system, (2) extract a given zip file to a specific destination directory, (3) extract another zip file to the current directory, and (4) verify the extracted contents are accessible. The system may or may not have the unzip utility pre-installed, so you'll need to check and install it if necessary.

Environment Setup: Ubuntu-based Docker container (Ubuntu 18.04 or newer) that may or may not have the unzip utility pre-installed. The container will have several .zip files placed in predefined locations with various directory structures and file types inside. The apt package manager should be available.

Testing: Python tests will verify: (1) that the unzip utility is installed and functional on the system, (2) that files from a zip archive are correctly extracted to a specified destination folder with proper directory structure preserved, (3) that extraction to the current directory works correctly, (4) that extracted files have correct permissions and are readable, (5) that nested directory structures within archives are properly maintained after extraction, and (6) that the system can handle zip files with various contents (text files, subdirectories, multiple files).

Difficulty: medium

Core Skills Tested: Linux command-line utilities, package installation, archive extraction, file system navigation, directory management, dependency checking, understanding extraction options and flags

Key Technologies: Ubuntu/Debian Linux, unzip utility, apt package manager, bash, file system operations

title: How to unzip a zip file from the Terminal?

question_text: <p>Just downloaded a .zip file from the internet. I want to use the terminal to unzip the file. What is the correct way to do this?</p>

answer_text: <p>If the <code>unzip</code> command isn't already installed on your system (use <code>which unzip</code> to check), then run:</p>
<pre><code>sudo apt-get install unzip
</code></pre>
<p>After installing the unzip utility, if you want to extract to a particular destination folder, you can use:</p>
<pre><code>unzip file.zip -d destination_folder
</code></pre>
<p>If you want to extract to a directory with the same name as the zip in your current working directory, you can simply do:</p>
<pre><code>unzip file.zip
</code></pre>
