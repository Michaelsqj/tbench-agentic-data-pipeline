Task: Extract tar.gz Compressed Archives Using tar Command

Instructions: You are managing a remote Linux server where compressed .tar.gz archive files have been uploaded and need to be extracted. Your task is to: (1) correctly identify that .tar.gz files require the tar command (not unzip), (2) extract the contents of one or more .tar.gz archives to the current directory using appropriate tar flags, (3) extract a .tar.gz archive to a specific custom destination directory, and (4) verify that the extracted files and directory structures are intact and accessible. Demonstrate understanding of tar command options including compression format specification, extraction mode, and verbose output.

Environment Setup: Ubuntu-based Docker container (Ubuntu 18.04 or newer) with tar utility pre-installed. The container should have several .tar.gz archive files placed in predefined locations containing various file types (images, text files, subdirectories) with realistic directory structures. Include at least one large archive with nested directories to simulate real-world scenarios.

Testing: Python tests will verify: (1) that the agent uses the tar command (not unzip) for .tar.gz files, (2) that extraction uses appropriate flags (-xvzf or equivalent) to handle gzip-compressed tar archives, (3) that files are successfully extracted with correct directory structure preserved, (4) that extraction to a custom directory using the -C flag works correctly, (5) that extracted files maintain proper permissions and are readable, (6) that all expected files and subdirectories from the archive are present after extraction, and (7) that the agent demonstrates understanding of tar flags (x for extract, z for gzip, v for verbose, f for file).

Difficulty: medium

Core Skills Tested: Linux archive management, tar command proficiency, understanding compression formats, command-line flags and options, file extraction, directory management, distinguishing between archive formats

Key Technologies: tar, gzip, bash, Linux file system operations, compressed archives

title: What command do I need to unzip/extract a .tar.gz file?

question_text: <p>I received a huge .tar.gz file from a client that contains about 800 mb of image files (when uncompressed.) Our hosting company's ftp is seriously slow, so extracting all the files locally and sending them up via ftp isn't practical. I was able to ftp the .tar.gz file to our hosting site, but when I ssh into my directory and try using unzip, it gives me this error:</p>

<pre><code>[esthers@clients locations]$ unzip community_images.tar.gz
Archive:  community_images.tar.gz
  End-of-central-directory signature not found.  Either this file is not a zipfile, or it constitutes one disk of a multi-part archive.  In the latter case the central directory and zipfile comment will be found on the last disk(s) of this archive.
note:  community_images.tar.gz may be a plain executable, not an archive
unzip:  cannot find zipfile directory in one of community_images.tar.gz or community_images.tar.gz.zip, and cannot find community_images.tar.gz.ZIP, period.
</code></pre>

<p>What command do I need to use to extract all the files in a .tar.gz file?</p>

answer_text: <p>Type <code>man tar</code> for more information, but this command should do the trick:</p>
<pre><code>tar -xvzf community_images.tar.gz
</code></pre>
<p>To explain a little further, <code>tar</code> collected all the files into one package, <code>community_images.tar</code>. The gzip program applied compression, hence the <code>gz</code> extension. So the command does a couple things:</p>
<ul>
<li><code>f</code>: this must be the last flag of the command, and the tar <strong>f</strong>ile must be immediately after. It tells tar the name and path of the compressed file.</li>
<li><code>z</code>: tells tar to decompress the archive using g<strong>z</strong>ip</li>
<li><code>x</code>: tar can collect files or e<strong>x</strong>tract them. <code>x</code> does the latter.</li>
<li><code>v</code>: makes tar talk a lot. <strong>V</strong>erbose output shows you all the files being extracted.</li>
</ul>
<p>To extract into a <strong>c</strong>ustom folder, add the <code>-C</code> option with a folder name of your choice:</p>
<pre><code>tar -xvzf community_images.tar.gz -C some_custom_folder_name
</code></pre>
