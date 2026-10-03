# Setup

## Voraussetzungen
- **Git** und **Python ≥ 3.9** (nur Standardbibliothek)
- **Claude Code** (empfohlen) — oder jede KI-Oberfläche mit Dateizugriff
- Optional: Obsidian als Editor

## Installation
1. **Privates** Repository verwenden (BRAIN enthält persönliche Daten), z. B. auf GitHub "Private" anlegen und klonen.
   Wichtig: nicht in ein öffentliches Repo pushen.
2. In den Ordner wechseln und prüfen:
   ```bash
   python SCRIPTS/core.py check        # Windows: py SCRIPTS\core.py check
   python -m unittest discover -s SCRIPTS
   ```
3. Secret-Scan als Git-Hook aktivieren: `python SCRIPTS/core.py install-hook`
4. Optional: `.env.example` → `.env` kopieren und nur benötigte Werte eintragen.
5. Claude Code im Ordner starten: `claude`. Erster Befehl: Onboarding (BRAIN befüllen) oder `/start-project …`.

## Obsidian (optional)
"Open folder as vault" → AI-CORE-Ordner. `.obsidian/workspace*.json` ist gitignored.

## Geplante Ausführung (erst nach erfolgreichem manuellem Test)
Linux/macOS (crontab -e), Montag 8:00 Weekly-Entwurf:
```
0 8 * * 1  cd /pfad/zu/AI-CORE && python3 SCRIPTS/core.py weekly >> LOGS/weekly.log 2>&1
```
Windows (Aufgabenplanung, PowerShell):
```
schtasks /Create /SC WEEKLY /D MON /ST 08:00 /TN "AI-CORE weekly" /TR "py C:\pfad\AI-CORE\SCRIPTS\core.py weekly"
```

## Backup
- Nach jedem Meilenstein: `git add -A && git commit -m "…" && git push` (privates Remote).
- Zusätzlich: Ordner in bestehendes Backup (z. B. Time Machine, Dateiversionsverlauf) aufnehmen.

## Wiederherstellung
```bash
git clone <privates-repo> AI-CORE && cd AI-CORE
python SCRIPTS/core.py check
```
Einzelne Datei zurückholen: `git log -- BRAIN/PROFILE.md` → `git checkout <commit> -- BRAIN/PROFILE.md`.
Secrets (`.env`) sind nicht im Repo — aus dem Passwortmanager neu anlegen.
