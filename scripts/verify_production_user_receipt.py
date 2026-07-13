from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.verify_user_skill_delivery import (  # noqa: E402
    protected_boundaries,
    stat_only_snapshot,
)


def main() -> int:
    boundaries = protected_boundaries()
    before = {label: stat_only_snapshot(path) for label, path in boundaries.items()}

    suite = unittest.defaultTestLoader.loadTestsFromName(
        "tests.test_production_user_receipt"
    )
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        return 1

    after = {label: stat_only_snapshot(path) for label, path in boundaries.items()}
    changed = sorted(label for label in boundaries if before[label] != after[label])
    if changed:
        print(f"PRODUCTION_USER_RECEIPT_BOUNDARY_CHANGED labels={','.join(changed)}")
        return 2

    print(
        "PRODUCTION_USER_RECEIPT_OK "
        f"tests={result.testsRun} skipped={len(result.skipped)} "
        f"protected_boundaries={len(boundaries)} unchanged=true "
        "production_apply=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
