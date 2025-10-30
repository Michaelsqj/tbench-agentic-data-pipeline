Task: Extract Various Compressed Tar Archives with Automatic Format Detection

Instructions: You are working with a Linux system that has multiple compressed tar archives in different formats (.tar.xz, .tar.gz, .tar.bz2, and plain .tar). Your task is to: (1) extract each type of compressed tar archive using GNU tar's automatic format detection feature (tar xf), (2) verify that xz-utils and other necessary compression utilities are installed on the system, (3) demonstrate that the same tar xf command works across all compression formats without needing to specify compression flags explicitly, and (4) verify that the extracted contents from each archive are correct and accessible. Show understanding that modern GNU tar can automatically detect compression formats.

Environment Setup: Ubuntu-based Docker container (Ubuntu 18.04 or newer) with GNU tar pre-installed. The container should have multiple tar archives in different compression formats placed in predefined locations: .tar.xz (xz compressed), .tar.gz (gzip compressed), .tar.bz2 (bzip2 compressed), and plain .tar files. Each archive should contain test files and directories. Initially, xz-utils may or may not be installed to test the agent's ability to detect and install missing compression utilities when needed.

Testing: Python tests will verify: (1) that xz-utils and other necessary compression utilities are installed on the system, (2) that tar xf command successfully extracts .tar.xz archives without explicit compression flags, (3) that the same tar xf syntax works for .tar.gz, .tar.bz2, and plain .tar files, (4) that extracted files and directories from all archive formats are present and correct, (5) that the agent demonstrates understanding of GNU tar's automatic format detection by not unnecessarily specifying -z, -j, or -J flags, and (6) that appropriate error handling occurs if compression utilities are missing (with installation of required packages).

Difficulty: medium

Core Skills Tested: Modern tar usage, understanding automatic compression detection, working with multiple archive formats, dependency management for compression utilities, command-line proficiency, cross-format archive handling

Key Technologies: GNU tar, xz-utils, gzip, bzip2, various compression formats (.xz, .gz, .bz2), Ubuntu/Debian package management, bash

title: How do I uncompress a tarball that uses .xz?

question_text: <p>I'm used to extracting tarballs with a <code>-xfz</code> flag, which handles gzip and bzip2 archives.</p>

<p>Recently I've run into a <code>.tar.xz</code> file and I would like to uncompress it in one step using <code>tar</code>, how can I do that?</p>

answer_text: <p>Ubuntu includes GNU tar, which recognizes the format by itself! One command works with any supported compression method, per <a href="http://www.gnu.org/software/tar/manual/tar.html#SEC131" rel="noreferrer">the manual</a>.</p>
<pre class="lang-bash prettyprint-override"><code># The same command handles any compression format! Ex:

tar xf archive.tar.xz  # for .tar.xz files
tar xf archive.tar.gz  # for .tar.gz files
tar xf archive.tar     # for .tar files
</code></pre>
<p>etc. If tar gives a <code>Cannot exec</code> error, you may need to <code>sudo apt install xz-utils</code> first.</p>
