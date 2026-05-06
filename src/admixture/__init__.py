"""
title: Python wrapper around OpenADMIXTURE.jl.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from admixture.exceptions import (
    JuliaNotFoundError,
    OpenAdmixtureError,
    OpenAdmixtureNotInstalledError,
    OpenAdmixtureRunError,
    OutputParseError,
    PlinkInputError,
)
from admixture.result import OpenAdmixtureResult
from admixture.runner import OpenAdmixtureRunner, run_openadmixture
from admixture.setup import default_julia_project_dir, setup


def get_version() -> str:
    """
    title: Get the version of the admixture package.
    returns:
      type: str
    """
    try:
        return version("admixture")
    except PackageNotFoundError:  # pragma: no cover - only used from source trees.
        return "0.0.3"  # semantic-release


__version__ = get_version()


__all__ = [
    "JuliaNotFoundError",
    "OpenAdmixtureError",
    "OpenAdmixtureNotInstalledError",
    "OpenAdmixtureResult",
    "OpenAdmixtureRunError",
    "OpenAdmixtureRunner",
    "OutputParseError",
    "PlinkInputError",
    "__version__",
    "default_julia_project_dir",
    "run_openadmixture",
    "setup",
]
