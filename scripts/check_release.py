"""Release guards, run against the BUILT distribution before upload.

Deliberately smaller than kirby-cost's and kirby-combat's: this package
carries no licensed game data, so the content guards those repos need do not
apply here. What remains is the pair that has actually bitten the family --
a tag that disagrees with the built version, and a distribution whose module
does not import from a clean environment.

Usage: python scripts/check_release.py dist/
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

FAILURES: list[str] = []


def ok(msg: str) -> None:
    print(f"ok    {msg}")


def bad(msg: str) -> None:
    print(f"FAIL  {msg}")
    FAILURES.append(msg)


def built_version(dist: Path) -> str | None:
    wheels = sorted(dist.glob("*.whl"))
    if not wheels:
        bad("no wheel in the distribution directory")
        return None
    m = re.match(r"kirby_dice-([^-]+)-", wheels[0].name)
    if not m:
        bad(f"cannot read a version out of {wheels[0].name}")
        return None
    return m.group(1)


def check_tag_matches(version: str) -> None:
    """A tag that does not match the built version publishes the wrong thing."""
    ref = os.environ.get("GITHUB_REF", "")
    if not ref.startswith("refs/tags/"):
        ok("not a tagged build; skipping the tag/version check")
        return
    tag = ref.removeprefix("refs/tags/").lstrip("v")
    if tag == version:
        ok(f"tag v{tag} agrees with the built version")
    else:
        bad(f"tag v{tag} does not match the built version {version}")


def check_imports_clean(dist: Path, version: str) -> None:
    """The wheel must import with nothing else installed. This package has no
    dependencies, and that claim should be enforced rather than asserted."""
    wheel = sorted(dist.glob("*.whl"))[0]
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(wheel) as z:
            z.extractall(tmp)
        probe = (
            "import kirby_dice;"
            "r = kirby_dice.RandomRoller(seed=1);"
            "assert r.roll_dice(3) and isinstance(r.seed, int);"
            "assert kirby_dice.RandomRoller().seed is not None"
        )
        res = subprocess.run(
            [sys.executable, "-c", probe],
            cwd=tmp,
            env={**os.environ, "PYTHONPATH": tmp},
            capture_output=True,
            text=True,
        )
    if res.returncode == 0:
        ok(f"kirby-dice {version}: imports and rolls with no dependencies installed")
    else:
        bad(f"the built wheel does not import cleanly: {res.stderr.strip()}")


def check_attribution(dist: Path) -> None:
    """The Bill Bame credit was missing for months. It ships or we do not."""
    wheel = sorted(dist.glob("*.whl"))[0]
    with zipfile.ZipFile(wheel) as z:
        init = z.read("kirby_dice/__init__.py").decode("utf8")
    if "Bill Bame" in init:
        ok("the Bill Bame attribution ships in the distribution")
    else:
        bad("the Bill Bame attribution is MISSING from kirby_dice/__init__.py")


def main() -> int:
    dist = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    if not dist.is_dir():
        print(f"no such directory: {dist}")
        return 1
    version = built_version(dist)
    if version is not None:
        check_tag_matches(version)
        check_imports_clean(dist, version)
        check_attribution(dist)
    print()
    if FAILURES:
        print(f"{len(FAILURES)} release guard(s) failed")
        return 1
    print("all release guards passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
