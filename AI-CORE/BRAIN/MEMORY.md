# Memory — Regeln & Index

Diese Datei ist das **Inhaltsverzeichnis und Regelwerk** des Gedächtnisses, kein Speicherort für Fakten.

## Wo gehört was hin?

| Memory-Typ | Datei | Inhalt | Lebensdauer |
|---|---|---|---|
| Profile | [PROFILE.md](PROFILE.md) | Wer ich bin, Rolle, Fähigkeiten, Tools | stabil |
| Goals | [GOALS.md](GOALS.md) | Ziele (langfristig / dieses Jahr / Quartal) | stabil, quartalsweise prüfen |
| Preference | [PREFERENCES.md](PREFERENCES.md) | Kommunikation, Antwortstil, Arbeitsweise | stabil |
| Principles / Rules | [PRINCIPLES.md](PRINCIPLES.md), [RULES.md](RULES.md) | Werte; harte Regeln für die KI | stabil |
| Decision | [DECISIONS.md](DECISIONS.md) | Projektübergreifende Entscheidungen + Begründung | dauerhaft |
| Learning | [LEARNINGS.md](LEARNINGS.md) | Erkenntnisse aus abgeschlossener Arbeit | dauerhaft, konsolidieren |
| Project | `PROJECTS/<name>/` | Alles Projektspezifische | bis Projektende, dann ARCHIVE |
| Temporary | [CONTEXT.md](CONTEXT.md) | Kurzfristiges, **immer mit `expires:`** | Tage bis Wochen |

Projektspezifisches gehört **nie** in BRAIN, sondern in das Projekt.

## Format eines Eintrags

```
- [2026-10-03] Aussage in einem Satz. (Quelle: user | abgeleitet)
```

Temporärer Kontext zusätzlich mit Ablaufdatum:

```
- [2026-10-03] Bin bis Freitag im Urlaub. (expires: 2026-10-10)
```

## Speicherregeln (vor jedem Speichern prüfen)

Speichern **nur wenn alle** zutreffen:
1. **Zukünftig nützlich** — wird wahrscheinlich in einer späteren Sitzung gebraucht.
2. **Geprüft** — vom Nutzer gesagt oder bestätigt. Abgeleitetes wird als `(Quelle: abgeleitet)` markiert und beim nächsten Kontakt bestätigt.
3. **Nicht doppelt** — vorher die Zieldatei lesen; bestehenden Eintrag aktualisieren statt neu anlegen.
4. **Nicht sensibel** — siehe Ausschlussliste unten und `RULES.md`.
5. **Kein Protokoll** — Ergebnisse speichern, nicht Gesprächsverläufe.

**"Remember: X"** → Claude schlägt Zieldatei + exakten Eintrag vor und speichert erst nach Bestätigung.
Ausnahme: der Nutzer sagt ausdrücklich "speichere direkt".

## Niemals speichern
- Passwörter, API-Keys, Tokens, private Schlüssel, PINs
- Gesundheits-, Finanz-, Ausweis- und Kontodaten (außer ausdrücklich gewünscht und nicht in öffentlichen Repos)
- Persönliche Daten Dritter ohne Notwendigkeit
- Alles, was in [RULES.md](RULES.md) unter "Nicht speichern" steht

## Konsolidierung
Ablauf: [WORKFLOWS/MEMORY_CONSOLIDATION.md](../WORKFLOWS/MEMORY_CONSOLIDATION.md). Rhythmus: monatlich oder wenn
`python SCRIPTS/core.py check` Memory-Hinweise meldet (abgelaufener Kontext, Datei > 200 Zeilen).
