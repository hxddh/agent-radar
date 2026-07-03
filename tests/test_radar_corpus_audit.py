from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "radar_corpus_audit.py"


spec = importlib.util.spec_from_file_location("radar_corpus_audit", MODULE_PATH)
assert spec is not None
radar_corpus_audit = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(radar_corpus_audit)


class RadarCorpusAuditTest(unittest.TestCase):
    def test_detects_multiple_candidate_inbox(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "research-log.md").write_text(
                "# Log\n\n## Candidate inbox\n\n- one\n\n## Candidate inbox\n\n- two\n",
                encoding="utf-8",
            )
            report = radar_corpus_audit.audit_corpus(root)
            codes = [item["code"] for item in report["issues"]]
            self.assertIn("multiple-candidate-inbox", codes)

    def test_detects_legacy_pass_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "research-log.md").write_text(
                "# Log\n\n### Pass: Daily update (2026-07-03)\n\n- item\n",
                encoding="utf-8",
            )
            report = radar_corpus_audit.audit_corpus(root)
            self.assertTrue(any(item["code"] == "legacy-pass-sections" for item in report["issues"]))

    def test_apply_fix_archives_pass_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "research-log.md").write_text(
                "# Log\n\n## Candidate inbox\n\n- item\n\n### Pass: old pass\n\n- archived\n",
                encoding="utf-8",
            )
            import datetime as dt

            report = radar_corpus_audit.apply_corpus_fixes(root, dt.date(2026, 7, 3), dry_run=False)
            self.assertTrue(report.get("applied"))
            cleaned = (root / "research-log.md").read_text(encoding="utf-8")
            self.assertNotIn("### Pass:", cleaned)
            archive = (root / "research-log-archive" / "2026-07.md").read_text(encoding="utf-8")
            self.assertIn("archived", archive.lower())


if __name__ == "__main__":
    unittest.main()
