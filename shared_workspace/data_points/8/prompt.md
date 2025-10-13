Implement `infrastructure/setup_rootless_docker.sh`, an executable Bash script that makes it possible to run Docker commands without sudo by preferring rootless mode and falling back to the docker group when needed.

The script must:
- Detect whether rootless Docker is supported by checking for `dockerd-rootless-setuptool.sh` or a functional `systemctl --user status`. When supported, perform the rootless setup under `$HOME/.config/docker-rootless/` and ensure the necessary environment variables (e.g., `DOCKER_HOST`, `XDG_RUNTIME_DIR`, `PATH`) are documented.
- When rootless mode is unavailable, ensure a Unix group (default `docker`) exists and emit the `sudo groupadd`/`sudo gpasswd -a <user> docker` commands required to grant access. Allow overriding the username with `--user <name>`.
- Support a `--dry-run` flag that performs detection and writes documentation without making changes.
- Append a dated entry to `docs/rootless_docker_readiness.md` on every run summarising: detection path, commands executed (or required), environment variables to export, and next steps.
- Avoid duplicating setup work if run repeatedly; instead note that the system is already configured.
- Exit non-zero with a descriptive error if required tooling (e.g., `docker` client) is missing.
