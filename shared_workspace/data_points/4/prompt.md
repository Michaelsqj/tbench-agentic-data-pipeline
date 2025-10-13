Create an executable Bash script `deploy/install_internal_tool.sh` to install the `.deb` artifact at `artifacts/internal-tool_1.4.2.deb` and record its status.

Implementation requirements:
- Use `dpkg -i` to install the artifact. If the install fails because of missing dependencies, run `apt-get install -f` (or `apt --fix-broken install`) once and retry `dpkg -i`. If the second attempt still fails, exit non-zero.
- After a successful install, query the system for the installed version using `dpkg-query -W -f '${Version}' internal-tool`.
- Write a JSON status file at `reports/internal_tool_status.json` with keys `package`, `version`, and `source` (`local-artifact`).
- When the requested version is already installed, skip reinstallation and exit 0 while still refreshing the status JSON.
- Log each major step to stdout so CI logs show what happened.
- Exit non-zero with a helpful message if the artifact is missing.
