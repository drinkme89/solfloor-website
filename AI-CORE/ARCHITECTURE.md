# Architecture

## Grundidee
**Dateien sind die Datenbank, Git ist das Backup, Claude ist die Laufzeit.** Alles ist lesbares Markdown; kein Server,
keine Datenbank, kein Vendor-Lock-in. Jede KI mit Dateizugriff kann das System nutzen; ohne Dateizugriff helfen die PROMPTS.

```
            ┌──────────── Oberflächen ────────────┐
            │ Claude Code · Obsidian · (Open WebUI)│ · (Voice)
            └───────────────┬──────────────────────┘
                            │ liest progressiv (CLAUDE.md-Tabelle)
   BRAIN/  ←── Memory-Regeln ──→  PROJECTS/<p>/   KNOWLEDGE/   INBOX/
      │                              │
   AGENTS/ (Rollen)  ──  WORKFLOWS/ (Loops + Quality Gates)
                            │
                SCRIPTS/core.py (deterministische Teile: anlegen, prüfen, Dashboard)
                            │
                 Git (privates Remote) = Versionierung + Backup
```

## Abweichungen von der ursprünglichen Zielstruktur (und warum)
| Abweichung | Grund |
|---|---|
| `BRAIN/DECISIONS.md`, `BRAIN/LEARNINGS.md` ergänzt | Decision- und Learning-Memory brauchen eigene Orte, sonst wird `MEMORY.md` zur Müllhalde. `MEMORY.md` ist jetzt Index + Regeln. |
| `TEMPLATES/project/` | Eine Vorlage statt im Skript hartkodiert → anpassbar ohne Code. |
| `WORKFLOWS/DEBUG_LOOP`, `QUALITY_GATES`, `INBOX_PROCESSING`, `WEEKLY_REVIEW`, `MEMORY_CONSOLIDATION` | Im Konzept gefordert, in der Baumstruktur nicht enthalten. |
| `.claude/agents`, `.claude/commands`, `.claude/settings.json` | Macht Agenten und Befehle in Claude Code direkt nutzbar; Permission-Sperren erzwingen Sicherheitsregeln technisch. Agenten-Inhalt bleibt nur in `AGENTS/` (keine Duplikate). |
| `DASHBOARD.md` wird generiert | Manuell gepflegte Dashboards veralten; die Daten stehen ohnehin in den Projektdateien. |
| Eine CLI statt vieler Skripte | Python-Standardbibliothek → läuft auf Windows/macOS/Linux ohne Installation; testbar. |

## Datenkonventionen (von `core.py` gelesen)
- `STATUS.md`: `Status: active|paused|blocked|done`, `Last updated: YYYY-MM-DD`, Abschnitte `## Aktueller Stand`, `## Blocker`
- `TASKS.md`: `- [ ]` offen, `- [x]` erledigt
- `NEXT.md`: nummerierte Liste `1. …`
- `DECISIONS.md`: Überschriften `## YYYY-MM-DD — Titel`
- `BRAIN/CONTEXT.md`: Einträge mit `expires: YYYY-MM-DD`
- Stale-Grenze: 21 Tage ohne Update bei aktiven Projekten.

## Optionale Komponenten — Bewertung
Nicht installiert. Entscheidung jeweils durch den Nutzer; Ausbau nur bei konkretem Bedarf.

| Komponente | Nutzen | Wann sinnvoll | Kosten / Aufwand |
|---|---|---|---|
| **Obsidian** | Komfortabler Editor + Graph für genau diese Markdown-Dateien | Sofort, wenn der Nutzer gern in Notizen arbeitet | kostenlos (privat); kein Server |
| **Ollama** | Lokale Modelle für Klassifikation, Zusammenfassung, Extraktion, datenschutzkritische Texte | Wenn sensible Daten nicht in die Cloud sollen oder viele Kleinaufgaben anfallen | kostenlos; braucht RAM/GPU (≥ 16 GB RAM für 7–8B-Modelle) |
| **Open WebUI** | Chat-Oberfläche für lokale + Cloud-Modelle, Knowledge/RAG, Voice | Wenn eine Web-/Mobile-Oberfläche neben Claude Code gewünscht ist | kostenlos; Docker, lokaler Netzwerkdienst (nur an 127.0.0.1 binden) |
| **Voice (Whisper)** | Sprachnotizen → Text → INBOX | Wenn unterwegs viel diktiert wird | lokal kostenlos (`faster-whisper`/`whisper.cpp`); Cloud-STT kostet pro Minute |
| **n8n** | Visuelle Workflows über mehrere externe Dienste | Erst bei ≥ 2–3 verknüpften Diensten (Mail → Inbox → Kalender) | Self-hosted kostenlos (Docker); Cloud kostenpflichtig |
| **RAG / Vektor-DB** | Semantische Suche | > ~500 Dokumente oder viele PDFs; sonst reicht Grep | Aufwand > Nutzen bei kleinem Bestand |
| **MCP-Connectors** | Kalender, Mail, GitHub etc. | Nur pro konkretem Anwendungsfall, read-only zuerst | je nach Dienst; Datenschutz prüfen |

### Voice-Workflow (Entwurf)
```
Sprache → Whisper (lokal) → Text → core.py inbox add --source voice → Process inbox / Frage an Claude → Antwort → optional TTS
```
Voice schreibt nur in die INBOX. Aktionen entstehen erst über Process inbox mit Freigabe.

### Lokal vs. Cloud (Ollama-Entscheidungsregel)
Lokal: Klassifikation, kurze Zusammenfassungen, Extraktion, alles mit sensiblen Daten.
Cloud (Claude): Planung, Code, Recherche, komplexes Reasoning, Review.
