Build a Python CLI at `tools/kept_back_report.py` that inspects an apt upgrade log and produces `reports/kept_back_plan.md` describing how to resolve held packages.

Required behaviour:
- By default read `logs/apt-upgrade.log`. Support a `--log-path` argument to override.
- Detect the `The following packages have been kept back:` section and capture the package names in the order they appear.
- For each kept-back package include a bullet in the report with the package name and a recommended `sudo apt-get --with-new-pkgs upgrade <pkg>` command.
- Summarise why apt normally keeps packages back (new dependencies) and when it is appropriate to escalate to `sudo apt-get dist-upgrade`.
- If no packages are held back, create the report with a short confirmation that nothing needs action.
- Exit non-zero with a clear error message if the log cannot be read.
