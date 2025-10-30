Task: Upgrade Specific Packages Using apt-get with --only-upgrade

Instructions: You are managing a Linux system where several packages are installed at older versions, but you need to selectively upgrade only specific packages rather than performing a full system upgrade. Your task is to: (1) check the current version of specific installed packages, (2) update the apt package index to get information about available newer versions, (3) upgrade one or more specific packages using apt-get with the --only-upgrade flag to ensure packages are only upgraded if already installed, and (4) verify that the targeted packages have been upgraded to newer versions while other packages remain unchanged. Demonstrate understanding of selective package upgrades versus full system upgrades.

Environment Setup: Ubuntu-based Docker container (Ubuntu 18.04 or newer) with several packages installed at older versions and newer versions available in configured repositories. The container should have a realistic apt configuration with package sources that provide updates. Include at least 3-4 packages at older versions (e.g., curl, wget, git, vim) where newer versions are available for upgrade. The apt package manager should be fully configured and functional.

Testing: Python tests will verify: (1) that apt-get update is run first to refresh package indexes, (2) that specific packages are upgraded using apt-get install --only-upgrade <packagename> syntax, (3) that the targeted packages are successfully upgraded to newer versions (verifiable via dpkg -l or apt-cache policy), (4) that packages not specified for upgrade remain at their original versions, (5) that the --only-upgrade flag prevents installation of packages that aren't already installed (if a non-existent package is targeted), and (6) that the agent demonstrates understanding of when to use --only-upgrade versus regular install command.

Difficulty: medium

Core Skills Tested: Selective package management, apt-get command proficiency, understanding upgrade flags and options, version checking, system maintenance without full upgrades, package update strategy

Key Technologies: apt-get, apt package manager, dpkg, Ubuntu/Debian package management, command-line flags

title: How to upgrade a single package using apt-get?

question_text: <p>How do I update a single package? As far as <code>man apt-get</code> says <code>apt-get upgrade</code> doesn't take a package/list of packages as parameter:</p>

<blockquote>
  <p><strong>upgrade</strong></p>

  <p>upgrade is used to install the newest versions of all packages
  currently installed on the system from the sources enumerated in
  <code>/etc/apt/sources.list</code>. Packages currently installed with new
  versions available are retrieved and upgraded; under no circumstances
  are currently installed packages removed, or packages not already
  installed retrieved and installed. New versions of currently installed
  packages that cannot be upgraded without changing the install status
  of another package will be left at their current version. An update
  must be performed first so that apt-get knows that new versions of
  packages are available.</p>
</blockquote>

answer_text: <p>You just need to do <code>apt-get install --only-upgrade &lt;packagename&gt;</code>. This will upgrade only that single package, and only if it is installed.</p>

<p>If you wish to install the package if it doesn't exist, or upgrade it if it does, you may leave out <code>--only-upgrade</code>.</p>
