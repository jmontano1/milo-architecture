#!/usr/bin/env python3
"""Self-check for the public reference implementation.

Runs without network, without secrets, and without importing the private
MILO mono-repo. Safe for CI and for third-party verification.

    python3 examples/test_reference.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEMO = ROOT / "persist_before_deliver.py"


def test_demo_runs_and_gates() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        # Demo writes audit.jsonl next to itself; run from a temp copy of the
        # script dir would be heavy — instead run in place and clean if needed.
        # The repo .gitignore already excludes examples/audit.jsonl.
        r = subprocess.run(
            [sys.executable, str(DEMO)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
        )
        assert r.returncode == 0, r.stderr or r.stdout
        out = r.stdout
        assert "blocked" in out, "over-threshold force should be blocked"
        assert "recommended_alternative" in out, "near-threshold force should recommend"
        assert "applied_n" in out, "routine force should apply"
        audit = ROOT / "audit.jsonl"
        assert audit.is_file(), "audit.jsonl must be written before/after dispatch"
        lines = [ln for ln in audit.read_text().splitlines() if ln.strip()]
        assert len(lines) >= 5, f"expected multiple audit events, got {len(lines)}"
        for ln in lines:
            rec = json.loads(ln)
            assert "ts" in rec and "id" in rec and "kind" in rec


def test_override_demo() -> None:
    override = ROOT / "supervisory_primacy_override.py"
    assert override.is_file()
    r = subprocess.run(
        [sys.executable, str(override)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert r.returncode == 0, r.stderr or r.stdout
    assert "override_logged" in r.stdout
    assert "held" in r.stdout or "hold" in r.stdout.lower()


def main() -> int:
    tests = [test_demo_runs_and_gates, test_override_demo]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"ok  {t.__name__}")
        except Exception as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e}", file=sys.stderr)
    if failed:
        print(f"{failed} test(s) failed", file=sys.stderr)
        return 1
    print(f"all {len(tests)} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
