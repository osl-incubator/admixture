"""
title: Tests for Julia environment helpers.
"""

from __future__ import annotations

import re
import sys

from pathlib import Path

import pytest

from admixture.exceptions import JuliaNotFoundError, OpenAdmixtureNotInstalledError
from admixture.julia_env import (
    _looks_like_path,
    _project_arg,
    bootstrap_julia_project,
    check_openadmixture_installed,
    find_julia,
    get_julia_version,
    get_openadmixture_version,
)
from admixture.setup import default_julia_project_dir

MISSING_JULIA_COMMAND = "definitely-not-julia-admixture-test"


def test_looks_like_path_detects_paths() -> None:
    """
    title: Path-like Julia arguments are detected.
    """
    assert _looks_like_path("/usr/bin/julia")
    assert _looks_like_path("bin/julia")
    assert _looks_like_path(r"C:\Julia\bin\julia.exe")
    assert not _looks_like_path("julia")


def test_find_julia_accepts_explicit_path(tmp_path: Path) -> None:
    """
    title: Explicit Julia executable paths are accepted.
    parameters:
      tmp_path:
        type: Path
    """
    executable = tmp_path / "julia"
    executable.write_text("#!/bin/sh\n")

    assert find_julia(executable) == executable


def test_find_julia_resolves_real_julia_from_path() -> None:
    """
    title: Julia command names are resolved from the real PATH.
    """
    executable = find_julia("julia")

    assert executable.is_file()
    assert executable.name.startswith("julia")


def test_find_julia_missing_command_raises() -> None:
    """
    title: Missing Julia commands raise a helpful error.
    """
    with pytest.raises(JuliaNotFoundError, match="Checked command on PATH"):
        find_julia(MISSING_JULIA_COMMAND)


def test_get_julia_version_from_real_runtime() -> None:
    """
    title: Julia version output is read from the real Julia runtime.
    """
    julia_version = get_julia_version("julia")

    assert julia_version.startswith("julia version ")


def test_get_julia_version_missing_executable_raises(tmp_path: Path) -> None:
    """
    title: OS errors while running Julia are wrapped.
    parameters:
      tmp_path:
        type: Path
    """
    with pytest.raises(JuliaNotFoundError, match="Could not execute"):
        get_julia_version(tmp_path / "missing-julia")


def test_project_arg() -> None:
    """
    title: Julia project arguments are built only when requested.
    """
    assert _project_arg(None) == []
    assert _project_arg("julia-env") == [f"--project={Path('julia-env')}"]


def test_check_openadmixture_installed_with_packaged_project() -> None:
    """
    title: OpenADMIXTURE imports from the packaged Julia project.
    """
    assert check_openadmixture_installed("julia", default_julia_project_dir())


def test_check_openadmixture_installed_returns_false_for_non_julia_runtime() -> None:
    """
    title: OpenADMIXTURE import checks fail for a non-Julia executable.
    """
    assert not check_openadmixture_installed(sys.executable)


def test_get_openadmixture_version_from_packaged_project() -> None:
    """
    title: OpenADMIXTURE version discovery uses the packaged Julia project.
    """
    openadmixture_version = get_openadmixture_version(
        "julia",
        default_julia_project_dir(),
    )

    assert openadmixture_version is not None
    assert re.match(r"^\d+(\.\d+)+", openadmixture_version)


def test_get_openadmixture_version_returns_none_for_non_julia_runtime() -> None:
    """
    title: OpenADMIXTURE version discovery returns None when Julia code fails.
    """
    assert get_openadmixture_version(sys.executable) is None


def test_bootstrap_julia_project_failure_with_non_julia_runtime(tmp_path: Path) -> None:
    """
    title: Julia bootstrap failures are reported without network installation.
    parameters:
      tmp_path:
        type: Path
    """
    with pytest.raises(OpenAdmixtureNotInstalledError, match="bootstrap failed"):
        bootstrap_julia_project(tmp_path / "julia-env", julia=sys.executable)
