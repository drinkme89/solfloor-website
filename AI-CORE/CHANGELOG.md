# Changelog

## 2026-10-03 — Foundation
- Ordnerstruktur, `.gitignore`, `CLAUDE.md`, `README.md`, `SECURITY.md`, `ARCHITECTURE.md`, `SETUP.md`, `COMMANDS.md`.
- BRAIN mit Memory-Typen (Profile, Goals, Preferences, Principles, Rules, Decisions, Learnings, Temporary Context) — noch ohne persönliche Inhalte.
- Projektvorlage, 7 Agenten, 9 Workflows inkl. Quality Gates, 6 Prompts.
- Claude-Code-Integration: Slash-Commands, Subagents, Permission-Sperren.
- `SCRIPTS/core.py` (new-project, list, status, dashboard, check, inbox, weekly, archive, install-hook) mit Tests.
- Gefunden und behoben beim Smoke-Test: (1) Secret-Scan prüfte auch gitignorierte Dateien → eine korrekt ignorierte `.env`
  blockierte jeden Commit; jetzt werden nur Dateien gescannt, die Git sehen würde (+ Regressionstest).
  (2) Pre-commit-Hook lief bei Fund doppelt. (3) BrokenPipe bei `| head`.
