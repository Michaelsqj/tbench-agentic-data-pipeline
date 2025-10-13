Write an executable Bash script `maintenance/remove_vendor_ppa.sh` that decommissions the PPA listed in `config/vendor_ppa.txt`, purges its packages, and produces an audit report.

Functional requirements:
- Read the PPA identifier from `config/vendor_ppa.txt`.
- Support an optional `PPA_ROOT` environment variable (default `/`) to allow operating in a staging tree. When set, treat `$PPA_ROOT/etc/apt/sources.list.d` as the sources directory and `$PPA_ROOT/var/log` for logs.
- Use `add-apt-repository --remove` to drop the PPA list file, installing `software-properties-common` if the command is missing.
- Ensure `ppa-purge` is installed; run it against the PPA and capture any packages downgraded or removed.
- Run `apt-get update` after the purge and list remaining packages that still reference the PPA (use `apt-cache policy`).
- Create `reports/ppa_retirement_report.md` summarising the PPA removed, commands executed, downgraded packages, and any remaining packages that require manual action. The report should clearly state when there was nothing to do (idempotent rerun).
- Exit non-zero with a helpful error message when the PPA identifier file is missing or empty.
