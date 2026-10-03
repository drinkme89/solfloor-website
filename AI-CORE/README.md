# AI CORE

Persönliches AI-System: ein **Gedächtnis** über mich, **Projekte**, die ihren Stand selbst festhalten, klar definierte
**Agenten-Rollen**, wiederholbare **Workflows** mit Qualitätsprüfungen — als einfache Markdown-Dateien in Git.
Funktioniert mit Claude Code (voll), mit jeder Chat-Oberfläche (über [PROMPTS](PROMPTS/)) und mit Obsidian als Editor.

## In 60 Sekunden
```bash
cd AI-CORE
claude                                  # Claude Code starten; liest CLAUDE.md automatisch
python SCRIPTS/core.py dashboard        # Überblick
python SCRIPTS/core.py new-project "Mein Projekt"
python SCRIPTS/core.py check            # Struktur, Secrets, Links, Memory, Projekte prüfen
```
In Claude Code dann natürlich sprechen: `Project status: mein-projekt`, `Research: …`, `Remember: …` — oder `/status mein-projekt`.

## Befehle
| Befehl | Wirkung |
|---|---|
| `Start project: X` | Projektstruktur anlegen, Ziel & DoD erfragen, Plan erstellen |
| `Project status: X` | Stand zusammenfassen |
| `Next: X` | Nächste sinnvolle Schritte bestimmen |
| `Remember: X` | Speicherort prüfen, Eintrag vorschlagen, nach OK speichern |
| `Research: X` | Research-Loop mit Quellen |
| `Build: X` | Build-Loop inkl. Test und Review |
| `Review: X` | Qualitätsprüfung |
| `Weekly review` | Überblick über alle Projekte |
| `Process inbox` | Inbox sortieren (mit Freigabe) |

Details und CLI-Referenz: [COMMANDS.md](COMMANDS.md).

## Aufbau
| Ordner | Zweck |
|---|---|
| [BRAIN/](BRAIN/MEMORY.md) | Gedächtnis über mich: Profil, Ziele, Präferenzen, Regeln, Entscheidungen, Learnings, temporärer Kontext |
| [PROJECTS/](PROJECTS/README.md) | Ein Ordner pro Projekt mit eigenem Gedächtnis |
| [AGENTS/](AGENTS/README.md) | Rollen: Researcher, Planner, Builder, Reviewer, Debugger, Security, Documentation |
| [WORKFLOWS/](WORKFLOWS/README.md) | Build-, Research-, Debug-, Review-Loops, Quality Gates, Routinen |
| [PROMPTS/](PROMPTS/README.md) | Prompts für Oberflächen ohne Dateizugriff |
| [KNOWLEDGE/](KNOWLEDGE/README.md) | Dauerhaftes Wissen |
| [INBOX/](INBOX/README.md) | Eingang für Unsortiertes |
| [AUTOMATIONS/](AUTOMATIONS/README.md) | Register der Automationen |
| `TEMPLATES/` | Vorlagen (Projekt) |
| `SCRIPTS/` | `core.py` (CLI) + Tests |
| `OUTPUT/`, `ARCHIVE/`, `LOGS/`, `CONFIG/` | Ergebnisse, Abgelegtes, Logs (nicht versioniert), Konfiguration |

Mehr: [ARCHITECTURE.md](ARCHITECTURE.md) · [SETUP.md](SETUP.md) · [SECURITY.md](SECURITY.md) · [CHANGELOG.md](CHANGELOG.md)
