"""
title: Tests for Julia/OpenADMIXTURE environment metadata.
"""

from __future__ import annotations

import re

from admixture import OpenAdmixtureRunner


def test_version_info() -> None:
    """
    title: Version metadata includes Python, Julia and backend fields.
    """
    info = OpenAdmixtureRunner().version_info()

    assert info["admixture_python_version"]
    assert info["python_version"]
    assert info["platform"]
    assert str(info["julia_executable"]).endswith("julia")
    assert str(info["julia_version"]).startswith("julia version ")
    assert info["openadmixture_installed"] is True
    assert isinstance(info["openadmixture_version"], str)
    assert re.match(r"^\d+(\.\d+)+", info["openadmixture_version"])
