Idea #7:
- Title: Tarball Expansion Workflow with Target Overrides
- Core Skill Match: Requires using `tar` with the correct flags to unpack `.tar.gz` archives, just like the original problem.
- Difficulty: medium
- Why Different: Adds requirements for destination control, integrity checks, and reporting to support remote deployment workflows.
- Tech Stack: Bash, tar, coreutils
- Task Type: deployment support

Task: Create a reusable extraction utility that expands large `.tar.gz` artifacts into configurable staging directories while validating integrity and documenting results.
Instructions:
- Write `scripts/extract_dataset.sh` that accepts optional `--archive` and `--dest` flags (defaulting to `artifacts/media_bundle.tar.gz` and `staging/media/`).
- The script must verify the archive exists, unpack it with `tar -xvzf`, and ensure the destination directory is created fresh before extraction.
- After extraction, compute a SHA256 checksum for every extracted file and write them to `staging/media_checksums.txt` relative to the destination root.
- Produce `logs/extraction_summary.json` capturing the archive path, destination path, total file count, and total extracted size (in bytes) using `du` or similar.
- On failure, clean up any partially extracted directories so reruns start from a clean state.

Environment Setup: Ubuntu 22.04 with Bash, tar, coreutils, and sha256sum available.
Testing:
- Tests will supply sample archives, run the script with defaults and overrides, and verify extracted files and checksum manifests exist.
- Another test corrupts the archive to ensure the script aborts and cleans the destination directory.
- JSON summary contents will be validated for accurate size and file counts via Python tests.
Difficulty: medium
Core Skills Tested: Tar usage, defensive scripting, checksum generation, command-line argument parsing
Key Technologies: Bash, tar, sha256sum, du
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

