"""
title: Tests for runner edge cases.
"""

from __future__ import annotations

import shutil
import sys

from pathlib import Path

import pytest

from admixture import OpenAdmixtureRunner, run_openadmixture
from admixture.exceptions import (
    OpenAdmixtureNotInstalledError,
    OpenAdmixtureRunError,
    PlinkInputError,
)

DATA_DIR = Path(__file__).parent / "data" / "tiny-plink"


def _copy_tiny_plink(tmp_path: Path) -> Path:
    """
    title: Copy the tiny PLINK fixture into a writable temporary directory.
    parameters:
      tmp_path:
        type: Path
    returns:
      type: Path
    """
    prefix = tmp_path / "tiny-plink" / "tiny"
    prefix.parent.mkdir(parents=True, exist_ok=True)
    for suffix in ("bed", "bim", "fam"):
        shutil.copyfile(DATA_DIR / f"tiny.{suffix}", Path(f"{prefix}.{suffix}"))
    return prefix


def test_build_command_rejects_invalid_extra_arg(tmp_path: Path) -> None:
    """
    title: Extra argument names must be safe CLI flag names.
    parameters:
      tmp_path:
        type: Path
    """
    runner = OpenAdmixtureRunner()

    with pytest.raises(ValueError, match="Invalid extra"):
        runner._build_command(
            bfile=tmp_path / "example",
            k=2,
            out_prefix=tmp_path / "out",
            seed=None,
            threads=None,
            extra_args={"bad flag": 1},
        )


def test_ensure_openadmixture_available_with_packaged_project() -> None:
    """
    title: The packaged Julia project provides OpenADMIXTURE.jl.
    """
    OpenAdmixtureRunner()._ensure_openadmixture_available()


def test_runner_missing_openadmixture_raises_before_execution(tmp_path: Path) -> None:
    """
    title: Missing OpenADMIXTURE.jl raises install guidance before execution.
    parameters:
      tmp_path:
        type: Path
    """
    plink_prefix = _copy_tiny_plink(tmp_path)

    with pytest.raises(OpenAdmixtureNotInstalledError, match=r"Pkg\.add"):
        OpenAdmixtureRunner(julia=sys.executable).run(
            bfile=plink_prefix,
            k=2,
            out_prefix=tmp_path / "out" / "tiny_k2",
        )


def test_runner_reports_real_bridge_failure_for_unknown_argument(
    tmp_path: Path,
) -> None:
    """
    title: Real Julia bridge failures are surfaced as runner errors.
    parameters:
      tmp_path:
        type: Path
    """
    plink_prefix = _copy_tiny_plink(tmp_path)

    with pytest.raises(OpenAdmixtureRunError, match="Unknown argument"):
        OpenAdmixtureRunner(timeout=120).run(
            bfile=plink_prefix,
            k=2,
            out_prefix=tmp_path / "out" / "tiny_k2",
            extra_args={"definitely_unknown_arg": 1},
        )


def test_run_openadmixture_uses_temporary_runner_validation(tmp_path: Path) -> None:
    """
    title: Convenience function delegates to runner input validation.
    parameters:
      tmp_path:
        type: Path
    """
    with pytest.raises(PlinkInputError, match=r"missing\.bed"):
        run_openadmixture(
            bfile=tmp_path / "missing",
            k=2,
            out_prefix=tmp_path / "out",
        )
