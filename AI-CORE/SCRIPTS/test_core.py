"""Tests for core.py. Run from AI-CORE:  python -m unittest discover -s SCRIPTS -v

Every test works on a temporary copy of AI-CORE, so the real files are never touched.
"""
import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import core  # noqa: E402

REAL_ROOT = Path(__file__).resolve().parent.parent


class CoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "AI-CORE"
        shutil.copytree(REAL_ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        # Start every test with no projects and an empty inbox, but keep the folder READMEs.
        for p in (self.root / "PROJECTS").iterdir():
            if p.is_dir():
                shutil.rmtree(p)
        for p in (self.root / "INBOX").glob("*.md"):
            if p.name.lower() != "readme.md":
                p.unlink()
        self._old_root, core.ROOT = core.ROOT, self.root

    def tearDown(self):
        core.ROOT = self._old_root
        shutil.rmtree(self.tmp)

    def run_cmd(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = core.main(list(argv))
        return code, out.getvalue()

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    # -- projects
    def test_slugify(self):
        self.assertEqual(core.slugify("Größe & Übung 2026!"), "groesse-uebung-2026")
        self.assertEqual(core.slugify("  "), "")

    def test_new_project_creates_full_structure_and_fills_placeholders(self):
        code, _ = self.run_cmd("new-project", "Test Projekt")
        self.assertEqual(code, 0)
        p = self.root / "PROJECTS" / "test-projekt"
        for f in core.PROJECT_FILES + ["RESEARCH", "OUTPUT", "ARCHIVE"]:
            self.assertTrue((p / f).exists(), f)
        text = (p / "STATUS.md").read_text(encoding="utf-8")
        self.assertNotIn("{{", text)
        self.assertIn(core.today(), text)

    def test_new_project_refuses_to_overwrite(self):
        self.run_cmd("new-project", "X")
        marker = self.root / "PROJECTS" / "x" / "NOTES.md"
        marker.write_text("wichtig", encoding="utf-8")
        with self.assertRaises(SystemExit):
            self.run_cmd("new-project", "X")
        self.assertEqual(marker.read_text(encoding="utf-8"), "wichtig")

    def test_project_info_parses_template_conventions(self):
        self.run_cmd("new-project", "Info")
        p = self.root / "PROJECTS" / "info"
        self.write("PROJECTS/info/STATUS.md", "Status: blocked\nLast updated: 2000-01-01\n## Blocker\n- Warte auf Angebot\n")
        self.write("PROJECTS/info/TASKS.md", "## Offen\n- [ ] a\n- [ ] b\n## Erledigt\n- [x] c\n")
        i = core.project_info(p)
        self.assertEqual(i["status"], "blocked")
        self.assertEqual(i["blockers"], ["- Warte auf Angebot"])
        self.assertEqual((len(i["open"]), len(i["done"])), (2, 1))
        self.assertEqual(len(i["next"]), 2)
        self.assertTrue(any("stale" in x for x in core.check_projects()))

    def test_template_blocker_none_is_not_a_blocker(self):
        self.run_cmd("new-project", "Clean")
        self.assertEqual(core.project_info(self.root / "PROJECTS" / "clean")["blockers"], [])
        self.assertEqual(core.check_projects(), [])

    def test_status_and_list_run(self):
        self.run_cmd("new-project", "S")
        self.assertEqual(self.run_cmd("status", "s")[0], 0)
        self.assertIn("s ", self.run_cmd("list")[1])
        with self.assertRaises(SystemExit):
            self.run_cmd("status", "gibt-es-nicht")

    def test_decisions_are_collected_newest_first(self):
        self.run_cmd("new-project", "D")
        self.write("PROJECTS/d/DECISIONS.md", "# x\n## 2026-01-02 — Neu\n## 2025-05-05 — Alt\n")
        self.write("BRAIN/DECISIONS.md", "## 2026-03-01 — Global\n")
        self.assertEqual([t for _, t, _ in core.decisions()], ["Global", "Neu", "Alt"])

    def test_archive_requires_done_and_moves_without_deleting(self):
        self.run_cmd("new-project", "A")
        with self.assertRaises(SystemExit):
            self.run_cmd("archive", "a", "--yes")
        status = self.root / "PROJECTS" / "a" / "STATUS.md"
        status.write_text(status.read_text(encoding="utf-8").replace("Status: active", "Status: done"), encoding="utf-8")
        self.assertEqual(self.run_cmd("archive", "a", "--yes")[0], 0)
        self.assertFalse((self.root / "PROJECTS" / "a").exists())
        self.assertTrue((self.root / "ARCHIVE" / "projects" / f"{core.today()}-a" / "PROJECT.md").exists())

    # -- checks
    def test_secret_scan_finds_real_looking_secrets(self):
        self.write("KNOWLEDGE/leak.md", "api_key = 'abcd1234efgh5678ijkl'\n")  # secret-scan: ignore
        self.write("OUTPUT/k.txt", "ghp_" + "a" * 36 + "\n")
        self.write("CONFIG/id.txt", "-----BEGIN OPENSSH PRIVATE KEY-----\n")  # secret-scan: ignore
        hits = core.scan_secrets()
        self.assertEqual(len(hits), 3, hits)

    def test_secret_scan_ignores_placeholders_and_marker(self):
        self.write("KNOWLEDGE/ok.md", "API_KEY=${ANTHROPIC_API_KEY}\npassword: your-password-here\n"
                   "token = 'abcdefghijklmnopqrst'  # secret-scan: ignore\n")
        self.assertEqual(core.scan_secrets(), [])

    @unittest.skipUnless(shutil.which("git"), "git not installed")
    def test_secret_scan_skips_gitignored_env_but_finds_tracked(self):
        # Regression: a correctly ignored .env used to block every commit via the pre-commit hook.
        import subprocess
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        self.write(".env", "ANTHROPIC_API_KEY=sk-ant-" + "r" * 30 + "\n")
        self.assertEqual(core.scan_secrets(), [])
        self.write("PROJECTS/n.md", "sk-ant-" + "r" * 30 + "\n")
        self.assertEqual(len(core.scan_secrets()), 1)

    def test_check_fails_on_secret(self):
        self.assertEqual(self.run_cmd("check")[0], 0)
        self.write("BRAIN/PROFILE.md", "sk-ant-" + "x" * 30)
        self.assertEqual(self.run_cmd("check")[0], 1)
        self.assertEqual(self.run_cmd("check", "--secrets-only")[0], 1)

    def test_broken_links_are_reported_but_code_blocks_ignored(self):
        self.write("KNOWLEDGE/l.md", "[ok](README.md) [weg](nope.md) [web](https://x.y)\n```\n[code](fake.md)\n```\n")
        bad = core.check_links()
        self.assertEqual(len(bad), 1)
        self.assertIn("nope.md", bad[0])

    def test_expired_context_is_reported(self):
        self.write("BRAIN/CONTEXT.md", "- [2020-01-01] alt (expires: 2020-01-02)\n- [2020-01-01] neu (expires: 2999-01-01)\n")
        self.assertEqual(len(core.check_context_expiry()), 1)

    # -- outputs
    def test_dashboard_contains_sections_and_project(self):
        self.run_cmd("new-project", "Dash")
        self.run_cmd("inbox", "add", "Idee", "eins")
        text = core.render_dashboard()
        for h in ("Aktive Projekte", "Next Actions", "Inbox", "Blocker", "Letzte Entscheidungen", "System"):
            self.assertIn(h, text)
        self.assertIn("**dash**", text)
        self.assertIn("1 unverarbeitete", text)

    def test_inbox_add_and_reject_empty(self):
        code, out = self.run_cmd("inbox", "add", "Milch kaufen", "--source", "voice")
        self.assertEqual(code, 0)
        item = core.inbox_items()[0]
        self.assertIn("Source: voice", item.read_text(encoding="utf-8"))
        with self.assertRaises(SystemExit):
            self.run_cmd("inbox", "add")

    def test_weekly_does_not_overwrite_without_force(self):
        self.run_cmd("new-project", "W")
        self.assertEqual(self.run_cmd("weekly")[0], 0)
        with self.assertRaises(SystemExit):
            self.run_cmd("weekly")
        self.assertEqual(self.run_cmd("weekly", "--force")[0], 0)


if __name__ == "__main__":
    unittest.main()
