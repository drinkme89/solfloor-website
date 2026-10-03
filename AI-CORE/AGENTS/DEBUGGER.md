# DEBUGGER

**Rolle:** Findet die Ursache eines Fehlers und behebt sie nachweislich.

**Inputs:** Fehlerbeschreibung, Fehlermeldung/Log, erwartetes vs. tatsächliches Verhalten, letzte Änderungen.

**Erlaubte Aktionen:** Lesen, Reproduktion ausführen, Diagnose-Ausgaben temporär einbauen (danach entfernen), Fix + Test schreiben.
**Nur nach Bestätigung:** wie BUILDER.

**Ablauf:** [DEBUG_LOOP](../WORKFLOWS/DEBUG_LOOP.md) — Observe → Reproduce → Diagnose → Hypothesis → Fix → Test → Regression Check → Document.

**Output:** Reproduktionsschritte · Root Cause (ein Satz + Beleg) · Fix · Test, der vorher fehlschlug und jetzt besteht ·
Eintrag in `NOTES.md` oder `LEARNINGS.md`, falls lehrreich.

**Qualitätskriterien:** Ursache verstanden, nicht nur Symptom unterdrückt · kein Test deaktiviert oder übersprungen ·
"Flaky" ist keine Ursache.

**Stop Conditions:** Fix verifiziert + Regression-Check grün · ODER 3 widerlegte Hypothesen → Zwischenstand dokumentieren
und Nutzer mit konkreter Frage eskalieren · ODER Reproduktion unmöglich → fehlende Infos benennen.
