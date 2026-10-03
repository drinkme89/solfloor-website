# Quality Gates

Ein Ergebnis gilt erst als fertig, wenn das passende Gate bestanden ist. Antworte pro Punkt mit **ja / nein / n.a. + Beleg**.

## Software
- [ ] Code läuft (Befehl + Ausgabe vorhanden)
- [ ] Tests laufen und sind grün; neue Logik hat einen Test
- [ ] Edge Cases geprüft (leer, ungültig, doppelt, sehr groß — soweit relevant)
- [ ] Keine offensichtlichen Fehler (Review gelesen, nicht nur ausgeführt)
- [ ] Keine Secrets (`python SCRIPTS/core.py check --secrets-only`)
- [ ] Bestehende Funktionalität nicht beschädigt (Regression)
- [ ] Doku aktuell

## Research
- [ ] Aussagen belegt (jede Faktenaussage hat Quelle)
- [ ] Primärquellen bevorzugt
- [ ] Fakten und Interpretation getrennt
- [ ] Unsicherheiten und Widersprüche sichtbar
- [ ] Quellendatum bei zeitkritischen Themen

## Automation
- [ ] Manuell ausgelöst und erfolgreich getestet, bevor sie geplant läuft
- [ ] Trigger funktioniert
- [ ] Happy Path funktioniert
- [ ] Fehlerbehandlung: Fehler werden sichtbar (Log/Exit-Code), nicht verschluckt
- [ ] Idempotent: doppelte Ausführung erzeugt keinen Schaden/keine Duplikate
- [ ] Sensible Daten korrekt behandelt; keine Secrets in Logs
- [ ] Abschaltbar (wie stoppe ich sie?) und in `AUTOMATIONS/README.md` dokumentiert

## Dokumentation
- [ ] Beschreibt Ist-Zustand
- [ ] Anleitungen ausführbar wie geschrieben
- [ ] `core.py check`: keine toten Links

## Memory-Änderung
- [ ] Zukünftig nützlich, geprüft, nicht doppelt, nicht sensibel (siehe [BRAIN/MEMORY.md](../BRAIN/MEMORY.md))
