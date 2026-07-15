from __future__ import annotations

import shutil
import sys
import unittest
import uuid
import zipfile
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import build_codex_plugin as package  # noqa: E402
import build_release_archive as release  # noqa: E402


class ReleaseArchiveTests(unittest.TestCase):
    def setUp(self) -> None:
        self.output = ROOT / "dist" / "release-tests" / uuid.uuid4().hex

    def tearDown(self) -> None:
        if self.output.exists():
            shutil.rmtree(self.output)

    def test_release_metadata_matches_both_manifests_and_notes(self) -> None:
        result = release.validate_release_metadata(release.expected_tag())
        self.assertEqual(result["version"], package.PLUGIN_VERSION)
        self.assertEqual(result["tag"], f"v{package.PLUGIN_VERSION}")

    def test_two_release_archives_are_byte_deterministic(self) -> None:
        first = release.build_release_archive(self.output / "first")
        second = release.build_release_archive(self.output / "second")
        self.assertEqual(first["archive_sha256"], second["archive_sha256"])
        self.assertEqual(
            Path(first["archive_path"]).read_bytes(),
            Path(second["archive_path"]).read_bytes(),
        )
        self.assertEqual(first["package_files"], 41)

    def test_wrong_release_tag_is_rejected_before_build(self) -> None:
        with self.assertRaises(release.ReleaseArchiveError):
            release.build_release_archive(self.output, tag="v9.9.9")
        self.assertFalse(self.output.exists())

    def test_archive_content_mutation_is_rejected(self) -> None:
        result = release.build_release_archive(self.output)
        archive_path = Path(result["archive_path"])
        with zipfile.ZipFile(archive_path, "a", compression=zipfile.ZIP_STORED) as archive:
            archive.writestr("cotend/unexpected.txt", "unexpected\n")
        with self.assertRaises(release.ReleaseArchiveError):
            release.verify_release_archive(archive_path)

    def test_output_must_stay_under_dist(self) -> None:
        with self.assertRaises(release.ReleaseArchiveError):
            release.guarded_output_directory(ROOT / "outside-release")

    def test_output_rejects_simulated_linked_dist_root(self) -> None:
        original = package._is_linklike

        def classify(path: Path) -> bool:
            return path == release.DIST_ROOT or original(path)

        with mock.patch.object(package, "_is_linklike", side_effect=classify):
            with self.assertRaises(release.ReleaseArchiveError):
                release.guarded_output_directory(release.DIST_ROOT / "candidate")


if __name__ == "__main__":
    unittest.main()
