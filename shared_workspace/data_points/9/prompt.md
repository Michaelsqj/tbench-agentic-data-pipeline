Write an executable Bash script `runtime/upgrade_node.sh` that upgrades Node.js using the `n` module based on `config/node_version.txt`.

Behaviour requirements:
- Read the desired version from `config/node_version.txt`. Exit with an error if the file is missing or empty.
- Ensure `n` is installed globally (`npm list -g n` or similar). If missing, install it via `npm install -g n`.
- Activate the requested Node version using `n <version>` and repair the `/usr/bin/node` symlink when necessary (e.g., invoke `sudo apt-get install --reinstall nodejs-legacy` or equivalent command noted in the log).
- After switching, emit the active `node --version` and `npm --version` to stdout and append them to `reports/node_upgrade.log` along with a timestamp and the actions taken.
- Support a `--rollback <version>` flag to switch back to a cached version. If the version is unavailable, exit non-zero with guidance.
- Fail fast with clear messaging when the requested version cannot be activated.
