"""
title: Tests for packaged Julia setup helpers.
"""

from __future__ import annotations

import importlib
import sys

import pytest

from admixture.exceptions import OpenAdmixtureNotInstalledError

admixture_setup_module = importlib.import_module("admixture.setup")


def test_default_julia_project_dir_points_to_packaged_project() -> None:
    """
    title: The default Julia project lives inside the Python package.
    """
    project_dir = admixture_setup_module.default_julia_project_dir()

    assert project_dir.name == "julia-env"
    assert project_dir.parent.name == "admixture"
    assert (project_dir / "Project.toml").is_file()
    assert (project_dir / "Manifest.toml").is_file()


def test_instantiate_julia_project_failure_with_non_julia_runtime() -> None:
    """
    title: Packaged project instantiation failures are reported.
    """
    with pytest.raises(OpenAdmixtureNotInstalledError, match="instantiation failed"):
        admixture_setup_module.instantiate_julia_project(julia=sys.executable)
