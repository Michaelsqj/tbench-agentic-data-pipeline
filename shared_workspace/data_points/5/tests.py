import os
import subprocess
from pathlib import Path

SCRIPT = Path("tools/run_and_capture.sh")


def _write_commands(lines):
    commands_path = Path("commands/sequence.txt")
    commands_path.parent.mkdir(parents=True, exist_ok=True)
    commands_path.write_text("
".join(lines) + "
")


def test_harness_exists():
    assert SCRIPT.exists(), "tools/run_and_capture.sh is missing"
    assert SCRIPT.stat().st_mode & 0o111, "Script must be executable"


def test_runs_commands_and_writes_logs(tmp_path):
    _write_commands([
        "# Run simple commands",
        "echo FIRST",
        "bash -c 'echo SECOND && echo ERR >&2'"
    ])

    env = os.environ.copy()
    env.pop("ALLOW_FAILURES", None)

    result = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True, env=env)
    assert result.returncode == 0, result.stderr or result.stdout

    logs_dir = Path("logs")
    assert logs_dir.exists(), "logs directory missing"
    logs = sorted(logs_dir.glob("*.log"))
    assert len(logs) == 2, "Expected two transcript logs"
    first_log = logs[0].read_text()
    assert "FIRST" in first_log
    second_log = logs[1].read_text()
    assert "SECOND" in second_log and "ERR" in second_log

    summary_path = logs_dir / "summary.md"
    assert summary_path.exists(), "summary.md missing"
    summary = summary_path.read_text()
    assert "echo FIRST" in summary
    assert "exit_code: 0" in summary

    # Rerun with ALLOW_FAILURES to ensure new logs are generated
    env["ALLOW_FAILURES"] = "true"
    _write_commands([
        "echo AGAIN",
        "bash -c 'echo FAIL >&2; exit 2'",
        "echo AFTER"
    ])
    result2 = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True, env=env)
    assert result2.returncode == 0, result2.stderr or result2.stdout
    logs_after = sorted(logs_dir.glob("*.log"))
    assert len(logs_after) >= 3, "Expected additional log files after rerun"
    summary2 = summary_path.read_text()
    assert "exit_code: 2" in summary2
    assert "ALLOW_FAILURES" not in summary2.upper()


def test_failure_handling_without_allow():
    _write_commands([
        "echo OK",
        "bash -c 'exit 7'",
        "echo SHOULD_NOT_RUN"
    ])

    env = os.environ.copy()
    env.pop("ALLOW_FAILURES", None)

    result = subprocess.run([
        "bash",
        str(SCRIPT)
    ], capture_output=True, text=True, env=env)
    assert result.returncode != 0, "Harness should exit non-zero on first failure"
    outputs = (result.stderr or result.stdout).lower()
    assert "command failed" in outputs

    logs = sorted(Path("logs").glob("*.log"))
    if logs:
        combined = "
".join(log.read_text() for log in logs)
        assert "SHOULD_NOT_RUN" not in combined, "Execution should stop after failure"
