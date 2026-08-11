from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import build_local_codex_artifact as local_artifact  # noqa: E402


class LocalCodexArtifactTests(unittest.TestCase):
    def test_archive_bytes_are_reproducible_and_locked(self) -> None:
        first_artifact, first = local_artifact.archive_bytes(ROOT)
        second_artifact, second = local_artifact.archive_bytes(ROOT)

        self.assertEqual(first_artifact, second_artifact)
        self.assertEqual(first, second)
        self.assertEqual(first_artifact.artifact_id, "cotend-codex-r000016")
        self.assertEqual(first_artifact.revision, 16)
        self.assertEqual(len(first_artifact.skills), 10)
        self.assertEqual(len(first_artifact.files), 71)

        with zipfile.ZipFile(local_artifact.io.BytesIO(first)) as archive:
            self.assertEqual(len(archive.infolist()), 73)
            self.assertTrue(
                all(
                    info.filename.startswith("cotend-codex-r000016/")
                    for info in archive.infolist()
                )
            )

    def test_build_refuses_different_existing_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output_root = Path(temporary)
            result = local_artifact.build_local_artifact(ROOT, output_root)
            destination = Path(result["output"])
            self.assertEqual(
                hashlib.sha256(destination.read_bytes()).hexdigest(),
                result["archive_sha256"],
            )
            destination.write_bytes(b"not-the-owned-artifact")
            with self.assertRaises(local_artifact.LocalArtifactBuildError):
                local_artifact.build_local_artifact(ROOT, output_root)


if __name__ == "__main__":
    unittest.main()
