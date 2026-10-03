# Commands

## Natürliche Befehle (in Claude Code oder jeder Sitzung mit Dateizugriff)

| Befehl | Slash-Command | Ablauf |
|---|---|---|
| `Start project: X` | `/start-project X` | `core.py new-project` → Ziel/Scope/DoD erfragen → PLANNER erstellt TASKS + NEXT |
| `Project status: X` | `/status X` | `core.py status` + STATUS/DECISIONS/NEXT lesen → Zusammenfassung ≤ 15 Zeilen |
| `Next: X` | `/next X` | Projektdateien lesen → 3–5 nächste Schritte → NEXT.md nach Bestätigung |
| `Remember: X` | `/remember X` | Regeln aus BRAIN/MEMORY.md → Zieldatei + Eintrag vorschlagen → nach OK speichern |
| `Research: X` | `/research X` | [RESEARCH_LOOP](WORKFLOWS/RESEARCH_LOOP.md) |
| `Build: X` | `/build X` | [BUILD_LOOP](WORKFLOWS/BUILD_LOOP.md) |
| `Review: X` | `/review X` | [REVIEW_LOOP](WORKFLOWS/REVIEW_LOOP.md) |
| `Weekly review` | `/weekly-review` | [WEEKLY_REVIEW](WORKFLOWS/WEEKLY_REVIEW.md) |
| `Process inbox` | `/process-inbox` | [INBOX_PROCESSING](WORKFLOWS/INBOX_PROCESSING.md) |

## CLI: `python SCRIPTS/core.py <befehl>`
(Windows: `py SCRIPTS\core.py …`). Nur Python-Standardbibliothek. Löscht nie etwas.

| Befehl | Wirkung | Schreibt? |
|---|---|---|
| `new-project "Name"` | Projekt aus Vorlage anlegen (bricht ab, wenn vorhanden) | ja, neuer Ordner |
| `list` | Projekte mit Status, offenen Tasks, Datum | nein |
| `status <name>` | Ziel, Stand, Blocker, Tasks, Next, Entscheidungen | nein |
| `dashboard [--write]` | Dashboard anzeigen / nach DASHBOARD.md schreiben | nur mit `--write` |
| `check [--secrets-only]` | Struktur, Secrets, tote Links, Memory, Projekte. Exit 1 bei Secrets/Strukturfehlern | nein |
| `inbox add "Text" [--source voice]` / `inbox list` | Inbox-Eintrag anlegen / auflisten | `add`: ja |
| `weekly [--force]` | Weekly-Review-Entwurf in OUTPUT/ | ja |
| `archive <name> [--yes]` | Projekt mit `Status: done` nach ARCHIVE/projects/ **verschieben** | ja (verschiebt) |
| `install-hook` | Git pre-commit Secret-Scan (überschreibt keinen vorhandenen Hook) | ja |

Tests: `python -m unittest discover -s SCRIPTS -v`
