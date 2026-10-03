# Weekly Review

1. `python SCRIPTS/core.py weekly` → Entwurf in `OUTPUT/weekly-review-YYYY-Www.md` (offene Tasks, Blocker, Stale-Projekte, System-Hinweise).
2. Claude liest den Entwurf plus `NEXT.md` aller aktiven Projekte und ergänzt:
   - Was ist diese Woche passiert? Was steht an?
   - Welche Projekte sind stale → pausieren, abschließen oder wiederbeleben?
   - Top 3 Prioritäten für die nächste Woche (abgeglichen mit `BRAIN/GOALS.md`).
3. Inbox verarbeiten ([INBOX_PROCESSING](INBOX_PROCESSING.md)).
4. Nutzer bestätigt → `NEXT.md`/`STATUS.md` der Projekte aktualisieren, `dashboard --write`.
