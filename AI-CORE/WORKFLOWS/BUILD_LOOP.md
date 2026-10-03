# Build Loop

```
Understand → Plan → Build → Test → Review → Fix → Retest → Document → Done
```

| Schritt | Was | Ergebnis |
|---|---|---|
| Understand | Ziel, Kontext, bestehenden Code lesen. Unklarheiten klären. | Ein Satz: "Fertig ist es, wenn …" |
| Plan | PLANNER: Aufgaben + DoD. Bei trivialen Aufgaben: 3-Zeilen-Plan im Kopf genügt. | `TASKS.md`, DoD |
| Build | BUILDER: kleinste Änderung, die die Aufgabe löst. | Änderung |
| Test | Ausführen. Tests laufen lassen. Happy Path + 1–2 Edge Cases. | Befehl + Ausgabe |
| Review | REVIEWER gegen DoD + [Quality Gate](QUALITY_GATES.md). Bei Secrets/Integrationen auch SECURITY. | Verdict |
| Fix | Nur blockierende Funde. | Änderung |
| Retest | Gleiche Tests + Regression. | Ausgabe |
| Document | DOCUMENTATION; `STATUS.md`, `TASKS.md`, `NEXT.md`, `CHANGELOG.md`. | aktualisierte Doku |
| Done | Nur wenn Gate bestanden **und** Doku aktuell. | Meldung mit Belegen |

**Nicht fertig**, nur weil Code geschrieben wurde. Review → Fix → Retest maximal **3×**, dann eskalieren.
