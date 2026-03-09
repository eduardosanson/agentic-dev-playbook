#!/usr/bin/env python3
"""
Detect test frameworks in the current project.

This script automatically identifies which test frameworks are available
in the project and returns their configuration.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List

def detect_jest() -> bool:
    """Check if Jest is configured."""
    return (
        Path("package.json").exists() and
        Path("jest.config.js").exists() or
        Path("jest.config.json").exists()
    )

def detect_pytest() -> bool:
    """Check if pytest is configured."""
    return (
        Path("pytest.ini").exists() or
        Path("pyproject.toml").exists() or
        Path("setup.cfg").exists()
    )

def detect_gradle() -> bool:
    """Check if Gradle is configured."""
    return Path("build.gradle").exists() or Path("build.gradle.kts").exists()

def detect_go_tests() -> bool:
    """Check if Go tests exist."""
    return any(Path(".").glob("*_test.go"))

def detect_rspec() -> bool:
    """Check if RSpec is configured."""
    return Path("spec").exists() and Path(".rspec").exists()

def detect_frameworks() -> Dict[str, str]:
    """
    Detect all available test frameworks.

    Returns a dict with framework names and their run commands.
    """
    frameworks = {}

    if detect_jest():
        frameworks["jest"] = "npm test -- --coverage"

    if detect_pytest():
        frameworks["pytest"] = "pytest --verbose --cov --cov-report=html"

    if detect_gradle():
        frameworks["gradle"] = "gradle test connectedAndroidTest --info"

    if detect_go_tests():
        frameworks["go"] = "go test ./... -v -cover"

    if detect_rspec():
        frameworks["rspec"] = "rspec --format documentation"

    return frameworks

def main():
    """Main entry point."""
    frameworks = detect_frameworks()

    if not frameworks:
        print(json.dumps({
            "status": "error",
            "message": "No test frameworks detected",
            "frameworks": []
        }))
        return 1

    print(json.dumps({
        "status": "success",
        "frameworks": frameworks,
        "count": len(frameworks)
    }, indent=2))
    return 0

if __name__ == "__main__":
    exit(main())
