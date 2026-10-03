# Config

Nicht-geheime Konfiguration. Secrets gehören in `../.env` (gitignored; Vorlage: `.env.example`) oder in den Secret Store
des Betriebssystems (Windows Credential Manager, macOS Keychain, Linux Secret Service) — **nie** in diesen Ordner,
außer in `CONFIG/secrets/` (gitignored).
