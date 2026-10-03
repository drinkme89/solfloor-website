# Automations

Register aller Automationen. Regel: **Erst manuell testen, dann planen.** Jede Automation muss das Gate
"Automation" in [WORKFLOWS/QUALITY_GATES.md](../WORKFLOWS/QUALITY_GATES.md) bestehen.

| Name | Was | Auslöser | Status | Stoppen |
|---|---|---|---|---|
| secret-scan | Blockiert Commits mit möglichen Secrets | Git pre-commit (`core.py install-hook`) | verfügbar, manuell zu installieren | `.git/hooks/pre-commit` löschen |
| dashboard | DASHBOARD.md erzeugen | manuell `core.py dashboard --write` | manuell | — |
| weekly | Weekly-Review-Entwurf | manuell `core.py weekly` | manuell | — |

Geplante Ausführung (Cron / Windows-Aufgabenplanung) erst, wenn der manuelle Ablauf mehrfach funktioniert hat — Beispiele in SETUP.md.
n8n erst, wenn mehrere externe Dienste verknüpft werden müssen (siehe ARCHITECTURE.md).
