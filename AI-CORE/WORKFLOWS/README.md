# Workflows

| Workflow | Auslöser | Agenten |
|---|---|---|
| [BUILD_LOOP](BUILD_LOOP.md) | `Build: X` | PLANNER → BUILDER → REVIEWER → DOCUMENTATION |
| [RESEARCH_LOOP](RESEARCH_LOOP.md) | `Research: X` | RESEARCHER → REVIEWER |
| [DEBUG_LOOP](DEBUG_LOOP.md) | Fehler mit unklarer Ursache | DEBUGGER |
| [REVIEW_LOOP](REVIEW_LOOP.md) | `Review: X` | REVIEWER, SECURITY |
| [PROJECT_UPDATE](PROJECT_UPDATE.md) | Ende jeder Arbeitssitzung an einem Projekt | — |
| [INBOX_PROCESSING](INBOX_PROCESSING.md) | `Process inbox` | — |
| [WEEKLY_REVIEW](WEEKLY_REVIEW.md) | `Weekly review` | — |
| [MEMORY_CONSOLIDATION](MEMORY_CONSOLIDATION.md) | monatlich / `check` meldet Memory | — |
| [QUALITY_GATES](QUALITY_GATES.md) | in jedem Loop vor "Done" | REVIEWER |

## Schleifen-Begrenzung (gilt für alle Loops)
- **Max. 3 Iterationen** desselben Fix-/Review-Zyklus für dasselbe Problem.
- Danach **Eskalation an den Nutzer** mit: was versucht wurde, was beobachtet wurde, konkrete Frage oder Optionen.
- Jede Iteration muss etwas **Neues** versuchen. Gleicher Ansatz zweimal = sofort eskalieren.
- Eskalation ist kein Scheitern, sondern die vorgesehene Ausfahrt.
