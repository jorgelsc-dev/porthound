import unittest

from porthound.versioning import bump_version, classify_commit_bump, combine_bumps


class TestVersioningLogic(unittest.TestCase):
    def test_breaking_change_subject_forces_major(self):
        bump = classify_commit_bump(
            "feat(api)!: remove legacy agent mode",
            "",
            ("app.py", "frontend/src/views/ApiView.vue"),
        )
        self.assertEqual(bump, "major")

    def test_breaking_change_body_forces_major(self):
        bump = classify_commit_bump(
            "refactor: simplify scanner payloads",
            "BREAKING CHANGE: payload schema changed",
            ("scan_payloads.py",),
        )
        self.assertEqual(bump, "major")

    def test_feat_commit_bumps_minor(self):
        bump = classify_commit_bump(
            "feat: add runtime shutdown endpoint",
            "",
            ("app.py", "frontend/src/views/SecurityView.vue"),
        )
        self.assertEqual(bump, "minor")

    def test_fix_commit_bumps_patch(self):
        bump = classify_commit_bump(
            "fix: silence noisy websocket logs",
            "",
            ("ws_demo.py",),
        )
        self.assertEqual(bump, "patch")

    def test_docs_only_commit_stays_patch(self):
        bump = classify_commit_bump(
            "update docs",
            "",
            ("README.md", "docs/reference/api.md"),
        )
        self.assertEqual(bump, "patch")

    def test_runtime_fallback_without_conventional_subject_bumps_minor(self):
        bump = classify_commit_bump(
            "mixed improvements",
            "",
            ("app.py", "frontend/src/state/appStore.js"),
        )
        self.assertEqual(bump, "minor")

    def test_build_only_fallback_stays_patch(self):
        bump = classify_commit_bump(
            "pipeline maintenance",
            "",
            (".github/workflows/deb-package.yml", "packaging/deb/build.sh"),
        )
        self.assertEqual(bump, "patch")

    def test_combine_bumps_keeps_highest_weight(self):
        self.assertEqual(combine_bumps("patch", "minor"), "minor")
        self.assertEqual(combine_bumps("major", "patch"), "major")

    def test_bump_version_obeys_semver(self):
        self.assertEqual(bump_version("1.0.6", "patch"), "1.0.7")
        self.assertEqual(bump_version("1.0.6", "minor"), "1.1.0")
        self.assertEqual(bump_version("1.0.6", "major"), "2.0.0")
        self.assertEqual(bump_version("1.0.6", "none"), "1.0.6")
