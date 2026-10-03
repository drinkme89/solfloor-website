# Debug Loop

```
Observe → Reproduce → Diagnose → Hypothesis → Fix → Test → Regression Check → Document
```

1. **Observe** — Fehlermeldung, Log, erwartetes vs. tatsächliches Verhalten, was hat sich zuletzt geändert?
2. **Reproduce** — minimaler, wiederholbarer Weg zum Fehler. Ohne Reproduktion kein Fix (außer offensichtlicher Tippfehler).
3. **Diagnose** — eingrenzen (Bisect, Logging, kleinste Eingabe).
4. **Hypothesis** — eine konkrete, prüfbare Ursache. Notieren.
5. **Fix** — an der Ursache, nicht am Symptom.
6. **Test** — Reproduktion schlägt jetzt nicht mehr fehl; idealerweise als automatischer Test.
7. **Regression Check** — bestehende Tests/Checks laufen.
8. **Document** — Ursache + Fix in `NOTES.md`; falls verallgemeinerbar in `BRAIN/LEARNINGS.md`.

**Max. 3 widerlegte Hypothesen**, dann Eskalation mit Hypothesen-Liste und Belegen.
Verboten: Tests deaktivieren, Fehler verschlucken (`except: pass`), "flaky" als Diagnose.
