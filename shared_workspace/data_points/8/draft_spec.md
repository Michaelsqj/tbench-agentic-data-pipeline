Idea #9:
- Title: Rootless Docker Enablement Checklist Generator
- Core Skill Match: Keeps the focus on enabling Docker usage without sudo by codifying the required group and rootless setup steps.
- Difficulty: extremely hard
- Why Different: Requires building an adaptive script that inspects the environment, chooses between rootless mode and group-based fallback, and documents the resulting actions.
- Tech Stack: Bash, getent, systemctl, docker userland tools
- Task Type: configuration automation

Task: Author a readiness tool that verifies whether the current user can run Docker commands without sudo, attempts rootless setup when possible, and produces an audited checklist for operators.
Instructions:
- Provide `infrastructure/setup_rootless_docker.sh` that first checks if the Docker daemon supports rootless mode (`dockerd-rootless-setuptool.sh` or `systemctl --user` availability); if supported, perform the necessary environment setup under `$HOME/.config/docker-rootless/`.
- When rootless prerequisites are missing, fall back to ensuring the `docker` Unix group exists and emit the commands needed to add a specified user (default `$USER`, override with `--user` flag) to that group without executing privileged steps when not running as root.
- Regardless of path taken, generate `docs/rootless_docker_readiness.md` documenting the detected scenario, commands executed (or still required), environment variables to export (e.g., `DOCKER_HOST`, `XDG_RUNTIME_DIR`), and a final checklist operators can follow.
- The script must re-run cleanly: subsequent executions should detect prior configuration, avoid duplicating steps, and append a new dated entry to the readiness log describing the current state.
- Include a `--dry-run` option that performs detection and documentation without modifying the system, while still signaling missing steps via the checklist.

Environment Setup: Ubuntu 22.04 with Bash, Docker CLI binaries preinstalled by the builder; tests will stub rootless tooling so the script can exercise both branches.
Testing:
- Tests will simulate environments with and without rootless support to ensure the script chooses the correct branch and that the readiness document lists the necessary commands.
- Another test will run the script twice (once real, once with `--dry-run`) and confirm the log accumulates timestamped entries without duplicating actions.
- Parameter handling is verified by invoking the script with `--user otherdev` and checking that the checklist references the alternate username.
Difficulty: extremely hard
Core Skills Tested: Privilege management, environment inspection, idempotent automation, documentation for operators
Key Technologies: Bash, dockerd-rootless-setuptool.sh, systemctl --user, groupadd, gpasswd
title: How can I use Docker without sudo?
question_text: <p>On Docker's documentation pages, all example commands are shown without <code>sudo</code>, like this one:</p>
<pre><code>docker ps
</code></pre>
<p>On Ubuntu, the binary is called <code>docker.io</code>. It also does not work without <code>sudo</code>:</p>
<pre><code>sudo docker.io ps
</code></pre>
<p>How can I configure Docker so that I don't need to prefix every Docker command with <code>sudo</code>?</p>

answer_text: <p>Good news: the new Docker version 19.03 (currently experimental) will be able to run rootless negating the problems that can occur using a root user. No more messing with elevated permissions, root, and anything that might open up your machine when you did not want to.</p>
<p>Video about this from <a href="https://www.slideshare.net/AkihiroSuda/dockercon-2019-hardening-docker-daemon-with-rootless-mode" rel="noreferrer">[DockerCon 2019] Hardening Docker daemon with Rootless mode</a></p>
<blockquote>
<p>A few Caveats to the rootless Docker mode</p>
<p>Docker engineers say the rootless mode cannot be considered a replacement for the complete suite of Docker engine features. Some limitation to the rootless mode include:</p>
<ul>
<li>cgroups resource controls, apparmor security profiles, checkpoint/restore, overlay networks etc. do not work on rootless mode.</li>
<li>Exposing ports from containers currently requires manual socat helper process.</li>
<li>Only Ubuntu-based distros support overlay filesystems in rootless mode.</li>
<li>Rootless mode is currently only provided for nightly builds that may not be as stable as you are used to.</li>
</ul>
</blockquote>
<hr />
<p>As of Docker 19.3 this is obsolete (and more dangerous than need be):</p>
<p>The <a href="https://docs.docker.com/engine/installation/linux/ubuntulinux/#/create-a-docker-group" rel="noreferrer">Docker manual</a> has this to say about it:</p>
<blockquote>
<p><strong>Giving non-root access</strong></p>
<p>The docker daemon always runs as the root user, and since Docker version 0.5.2, the docker daemon binds to a Unix socket instead of a TCP port. By default that Unix socket is owned by the user root, and so, by default, you can access it with sudo.</p>
<p>Starting in version 0.5.3, if you (or your Docker installer) create a Unix group called docker and add users to it, then the docker daemon will make the ownership of the Unix socket read/writable by the docker group when the daemon starts. The docker daemon must always run as the root user, but if you run the docker client as a user in the docker group then you don't need to add sudo to all the client commands. As of 0.9.0, you can specify that a group other than docker should own the Unix socket with the -G option.</p>
<p><strong>Warning: The docker group (or the group specified with -G) is root-equivalent; see <a href="https://docs.docker.com/engine/security/security/#/docker-daemon-attack-surface" rel="noreferrer">Docker Daemon Attack Surface details</a> and this blogpost on <a href="https://www.projectatomic.io/blog/2015/08/why-we-dont-let-non-root-users-run-docker-in-centos-fedora-or-rhel/" rel="noreferrer">Why we don't let non-root users run Docker in CentOS, Fedora, or RHEL </a></strong> (thanks michael-n).</p>
<p>In the recent release of the <a href="https://github.com/moby/moby/blob/master/docs/rootless.md" rel="noreferrer">experimental rootless mode on GitHub</a>, engineers mention rootless mode allows running dockerd as an unprivileged user, using user_namespaces(7), mount_namespaces(7), network_namespaces(7).</p>
<p>Users need to run dockerd-rootless.sh instead of dockerd.</p>
<pre><code>$ dockerd-rootless.sh --experimental
</code></pre>
<p>As Rootless mode is experimental, users need to always run dockerd-rootless.sh with –experimental.</p>
</blockquote>
<hr />
<p>Important to read: <a href="https://docs.docker.com/engine/installation/linux/linux-postinstall/" rel="noreferrer">post-installation steps for Linux</a> (it also links to <a href="https://docs.docker.com/engine/security/security/#/docker-daemon-attack-surface" rel="noreferrer">Docker Daemon Attack Surface details</a>).</p>
<blockquote>
<p><strong>Manage Docker as a non-root user</strong></p>
<p>The docker daemon binds to a Unix socket instead of a TCP port. By default that Unix socket is owned by the user root and other users can only access it using sudo. The docker daemon always runs as the root user.</p>
<p>If you don’t want to use sudo when you use the docker command, create a Unix group called docker and add users to it. When the docker daemon starts, it makes the ownership of the Unix socket read/writable by the docker group.</p>
</blockquote>
<hr />
<ul>
<li><p>Add the <code>docker</code> group if it doesn't already exist:</p>
<pre><code> sudo groupadd docker
</code></pre>
</li>
<li><p>Add the connected user &quot;$USER&quot; to the <code>docker</code> group. Change the user name to match your preferred user if you do not want to use your current user:</p>
<pre><code> sudo gpasswd -a $USER docker
</code></pre>
</li>
<li><p>Either do a <code>newgrp docker</code> or log out/in to activate the changes to groups.</p>
</li>
<li><p>You can use</p>
<pre><code> docker run hello-world
</code></pre>
<p>to check if you can run Docker without <code>sudo</code>.</p>
</li>
</ul>

