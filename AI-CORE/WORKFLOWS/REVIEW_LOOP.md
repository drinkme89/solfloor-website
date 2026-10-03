# Review Loop

```
Scope festlegen → Anforderungen sammeln → Prüfen → Bericht → (Fix durch BUILDER) → Re-Review
```

1. **Scope** — Was wird geprüft (Datei, Diff, Projekt, Recherche)? Gegen welche Anforderung?
2. **Anforderungen** — DoD aus `PROJECT.md`, Aufgabe aus `TASKS.md`, passendes [Quality Gate](QUALITY_GATES.md).
3. **Prüfen** — REVIEWER (fachlich), SECURITY (wenn Secrets, Rechte, externe Dienste, Datenflüsse betroffen).
   Automatisch: `python SCRIPTS/core.py check`.
4. **Bericht** — Format aus [REVIEWER](../AGENTS/REVIEWER.md). Blockierend vs. optional trennen.
5. **Fix** — durch BUILDER, nicht durch REVIEWER.
6. **Re-Review** — nur die Funde erneut prüfen. Max. **3 Runden**, dann Nutzer entscheidet.
