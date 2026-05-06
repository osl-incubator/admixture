"""
title: Tests for command line entry points.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from admixture import cli


def test_main_without_subcommand_prints_help(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    title: The top-level command prints help when no subcommand is provided.
    parameters:
      capsys:
        type: pytest.CaptureFixture[str]
    """
    returncode = cli.main([])

    captured = capsys.readouterr()
    assert returncode == 2
    assert "usage: admixture" in captured.out
    assert captured.err == ""


def test_main_setup_help(capsys: pytest.CaptureFixture[str]) -> None:
    """
    title: The setup subcommand exposes command-line help.
    parameters:
      capsys:
        type: pytest.CaptureFixture[str]
    """
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["setup", "--help"])

    captured = capsys.readouterr()
    assert exc_info.value.code == 0
    assert "usage: admixture setup" in captured.out
    assert "--julia" in captured.out


def test_main_setup_missing_julia_reports_error(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    title: The setup command reports missing Julia without a traceback.
    parameters:
      tmp_path:
        type: Path
      capsys:
        type: pytest.CaptureFixture[str]
    """
    returncode = cli.main(["setup", "--julia", str(tmp_path / "missing-julia")])

    captured = capsys.readouterr()
    assert returncode == 1
    assert captured.out == ""
    assert "Install Julia" in captured.err
