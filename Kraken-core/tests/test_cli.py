"""Unit tests for KRAKEN's new Sprint 2 CLI commands.

These tests exercise the Typer application directly via `CliRunner`.
Subprocess-backed commands (`test`, `format`, `lint`) have their underlying
`kraken.devtools` calls monkeypatched so the suite never spawns pytest,
black, or ruff as a subprocess of itself.
"""

import pytest
from typer.testing import CliRunner

from kraken import cli

runner = CliRunner()


def test_version_command_still_works(clean_env: None) -> None:
    """Sprint 1's `version` command must keep working unchanged."""
    result = runner.invoke(cli.app, ["version"])

    assert result.exit_code == 0
    assert "KRAKEN v" in result.stdout


def test_doctor_command_reports_success(clean_env: None) -> None:
    """`kraken doctor` should exit 0 when every check passes."""
    result = runner.invoke(cli.app, ["doctor"])

    assert result.exit_code == 0
    assert "KRAKEN Doctor" in result.stdout


def test_doctor_command_fails_when_a_check_fails(
    clean_env: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`kraken doctor` should exit non-zero if any diagnostic check fails."""
    from kraken.diagnostics import CheckResult

    monkeypatch.setattr(
        cli,
        "run_all_checks",
        lambda settings: [CheckResult(name="Broken check", passed=False, detail="nope")],
    )

    result = runner.invoke(cli.app, ["doctor"])

    assert result.exit_code == 1


def test_info_command_prints_snapshot(clean_env: None) -> None:
    """`kraken info` should exit 0 and print the KRAKEN application name."""
    result = runner.invoke(cli.app, ["info"])

    assert result.exit_code == 0
    assert "Info" in result.stdout


def test_test_command_invokes_run_tests(
    clean_env: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`kraken test` should delegate to `devtools.run_tests`."""
    monkeypatch.setattr(cli, "run_tests", lambda: 0)

    result = runner.invoke(cli.app, ["test"])

    assert result.exit_code == 0


def test_test_command_propagates_failure(
    clean_env: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`kraken test` should exit with pytest's exit code on failure."""
    monkeypatch.setattr(cli, "run_tests", lambda: 1)

    result = runner.invoke(cli.app, ["test"])

    assert result.exit_code == 1


def test_format_command_invokes_run_format_with_check_flag(
    clean_env: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`kraken format --check` should call `run_format(check=True)`."""
    captured: dict[str, bool] = {}

    def _fake_run_format(check: bool = False) -> int:
        captured["check"] = check
        return 0

    monkeypatch.setattr(cli, "run_format", _fake_run_format)

    result = runner.invoke(cli.app, ["format", "--check"])

    assert result.exit_code == 0
    assert captured["check"] is True


def test_lint_command_invokes_run_lint_with_fix_flag(
    clean_env: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`kraken lint --fix` should call `run_lint(fix=True)`."""
    captured: dict[str, bool] = {}

    def _fake_run_lint(fix: bool = False) -> int:
        captured["fix"] = fix
        return 0

    monkeypatch.setattr(cli, "run_lint", _fake_run_lint)

    result = runner.invoke(cli.app, ["lint", "--fix"])

    assert result.exit_code == 0
    assert captured["fix"] is True
