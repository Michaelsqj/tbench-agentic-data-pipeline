Ship `admin/apply_user_state.sh`, an executable Bash script that applies declarative user operations to the supplied `mock_root/` chroot and captures an audit report.

Functional requirements:
- Expect the desired state in `config/user_operations.yaml` (see example in the repo). Each entry can declare `state` (`present` or `absent`), `shell`, `full_name`, supplemental `groups`, and `remove_home`.
- Apply all changes against the staged chroot at `mock_root/` without affecting the real host. You may use standard tools (`useradd`, `usermod`, `userdel`, etc.) with `--root mock_root`, or manipulate the passwd/group files directly—choose the safest approach but ensure results match the desired state.
- When creating users, ensure home directories exist (e.g., `mock_root/home/<user>`). When removing users with `remove_home: true`, delete their home directory.
- Produce `reports/user_audit.json` containing the final list of users (username, uid, gid, shell, supplementary groups) and a list of actions performed during this run.
- Support `--plan-only`, which prints the actions that would be taken but does not modify any files. The audit file should still be generated with `applied` marked as false for each planned action.
- Make the script idempotent: rerunning with the same desired state should result in no further changes and note that the system already matches.
- Exit non-zero with a clear message if the YAML file is missing or malformed.
