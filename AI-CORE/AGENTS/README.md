# Agents

Agenten sind **Rollen mit klaren Grenzen**, keine separaten Programme. Jede Datei ist zugleich Doku
und Arbeitsanweisung. In Claude Code sind sie zusätzlich als Subagents in `.claude/agents/` registriert
(dünne Verweise auf diese Dateien, damit es nur eine Quelle gibt).

| Agent | Wann | Darf schreiben? |
|---|---|---|
| [RESEARCHER](RESEARCHER.md) | Fragen, die Recherche brauchen | nur `RESEARCH/`, `KNOWLEDGE/` |
| [PLANNER](PLANNER.md) | Ziel → Aufgaben, Reihenfolge, DoD | `TASKS.md`, `NEXT.md`, `PROJECT.md` |
| [BUILDER](BUILDER.md) | Umsetzung: Code, Dateien, Config | Projektdateien laut Plan |
| [REVIEWER](REVIEWER.md) | Ergebnis gegen Anforderungen prüfen | nein (nur Bericht) |
| [DEBUGGER](DEBUGGER.md) | Fehler mit unklarer Ursache | Fix + Test |
| [SECURITY](SECURITY.md) | Secrets, Rechte, externe Integrationen | nein (nur Bericht) |
| [DOCUMENTATION](DOCUMENTATION.md) | Nach Änderungen: Doku nachziehen | Doku-Dateien |

**Faustregel:** Kleine Aufgaben erledigt Claude direkt. Agenten lohnen sich, wenn eine **unabhängige
Perspektive** hilft (Review, Security) oder viel Material gesichtet werden muss (Research).
Wer baut, reviewt nicht selbst abschließend.

Gemeinsame Regeln für alle Agenten: [../CLAUDE.md](../CLAUDE.md), [../SECURITY.md](../SECURITY.md).
