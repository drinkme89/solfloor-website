#!/usr/bin/env python3
"""AI-CORE command line tool.

Standard library only, so it runs on Windows, macOS and Linux without installs.
Every command is read-only unless stated otherwise; nothing is ever deleted.

Usage:  python SCRIPTS/core.py <command> [args]   (run from the AI-CORE folder)
        python SCRIPTS/core.py --help
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("AI_CORE_ROOT", Path(__file__).resolve().parent.parent))

STALE_DAYS = 21
STATUSES = ("active", "paused", "blocked", "done")
REQUIRED_FILES = [
    "CLAUDE.md", "README.md", "SECURITY.md", ".gitignore",
    "BRAIN/PROFILE.md", "BRAIN/PREFERENCES.md", "BRAIN/GOALS.md", "BRAIN/PRINCIPLES.md",
    "BRAIN/RULES.md", "BRAIN/CONTEXT.md", "BRAIN/MEMORY.md", "BRAIN/DECISIONS.md",
    "BRAIN/LEARNINGS.md", "TEMPLATES/project/PROJECT.md",
]
PROJECT_FILES = ["PROJECT.md", "STATUS.md", "DECISIONS.md", "TASKS.md", "NEXT.md", "NOTES.md"]

SECRET_PATTERNS = [
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Anthropic key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}")),
    ("OpenAI-style key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9]{32,}")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|\bgithub_pat_[A-Za-z0-9_]{30,}")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("assigned secret", re.compile(
        r"(?i)\b(?:api[_-]?key|secret|token|passw(?:or)?d|pwd)\b\s*[:=]\s*['\"]?([^\s'\"<>]{12,})")),
]
# Values that are obviously placeholders, not secrets.
PLACEHOLDER = re.compile(r"(?i)^(?:\$\{?|%|your|example|changeme|xxx|placeholder|dummy|none|null|env\.|os\.environ)")
IGNORE_MARKER = "secret-scan: ignore"
SCAN_SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}
TEXT_SUFFIXES = {".md", ".txt", ".py", ".sh", ".ps1", ".json", ".yml", ".yaml", ".toml", ".ini",
                 ".cfg", ".env", ".js", ".ts", ".html", ".css", ".csv", ".log", ""}


# ---------------------------------------------------------------- helpers
def today() -> str:
    return dt.date.today().isoformat()


def slugify(name: str) -> str:
    table = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", "Ä": "ae", "Ö": "oe", "Ü": "ue"})
    slug = re.sub(r"[^a-z0-9]+", "-", name.translate(table).lower()).strip("-")
    return slug[:60]


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError):
        return ""


def section(text: str, heading: str) -> list[str]:
    """Return the non-empty lines below '## heading' up to the next '## '."""
    lines, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line[3:].strip().lower().startswith(heading.lower())
            continue
        if inside and line.strip() and not line.strip().startswith("<!--"):
            lines.append(line.rstrip())
    return lines


def field(text: str, name: str) -> str:
    m = re.search(rf"^{re.escape(name)}:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
    return m.group(1).strip() if m else ""


def is_none_line(line: str) -> bool:
    return line.strip("-* ").lower() in {"", "none", "keine", "-", "n/a"}


def projects_dir() -> Path:
    return ROOT / "PROJECTS"


def list_projects() -> list[Path]:
    d = projects_dir()
    if not d.is_dir():
        return []
    return sorted(p for p in d.iterdir() if p.is_dir() and not p.name.startswith((".", "_")))


def find_project(name: str) -> Path:
    slug = slugify(name)
    for p in list_projects():
        if p.name == slug or p.name == name:
            return p
    raise SystemExit(f"Projekt nicht gefunden: {name!r}. Vorhanden: {', '.join(p.name for p in list_projects()) or '-'}")


def project_info(p: Path) -> dict:
    status = read(p / "STATUS.md")
    tasks = read(p / "TASKS.md")
    nxt = read(p / "NEXT.md")
    proj = read(p / "PROJECT.md")
    goal = section(proj, "Ziel")
    updated = field(status, "Last updated")
    try:
        age = (dt.date.today() - dt.date.fromisoformat(updated)).days
    except ValueError:
        age = None
    return {
        "name": p.name,
        "title": (proj.splitlines() or [p.name])[0].lstrip("# ").strip(),
        "goal": goal[0] if goal else "",
        "status": (field(status, "Status").split() or ["?"])[0].lower(),
        "updated": updated or "?",
        "age": age,
        "blockers": [l for l in section(status, "Blocker") if not is_none_line(l)],
        "open": [l for l in tasks.splitlines() if re.match(r"\s*- \[ \]", l)],
        "done": [l for l in tasks.splitlines() if re.match(r"\s*- \[x\]", l, re.I)],
        "next": [l for l in nxt.splitlines() if re.match(r"\s*\d+\.\s+\S", l)],
    }


def decisions(limit: int = 5) -> list[tuple[str, str, str]]:
    """(date, title, source) from BRAIN/DECISIONS.md and every project's DECISIONS.md, newest first."""
    sources = [("BRAIN", ROOT / "BRAIN" / "DECISIONS.md")] + [(p.name, p / "DECISIONS.md") for p in list_projects()]
    found = []
    for src, path in sources:
        for m in re.finditer(r"^## (\d{4}-\d{2}-\d{2})\s*[—-]\s*(.+)$", read(path), re.MULTILINE):
            found.append((m.group(1), m.group(2).strip(), src))
    return sorted(found, reverse=True)[:limit]


def inbox_items() -> list[Path]:
    d = ROOT / "INBOX"
    return sorted(p for p in d.glob("*.md") if p.name.lower() != "readme.md") if d.is_dir() else []


# ---------------------------------------------------------------- checks
def iter_text_files(base: Path):
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in SCAN_SKIP_DIRS]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix.lower() in TEXT_SUFFIXES and p.stat().st_size < 2_000_000:
                yield p


def git_visible_files(base: Path):
    """Files git would track (tracked + untracked, minus .gitignore'd); None if not a git repo."""
    try:
        res = subprocess.run(["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                             cwd=base, capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    files = [base / f for f in res.stdout.decode("utf-8", "replace").split("\0") if f]
    return [p for p in files if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES and p.stat().st_size < 2_000_000]


def scan_secrets(base: Path | None = None) -> list[str]:
    """Scan files that could end up in git. Gitignored files (e.g. .env) are skipped on purpose:
    that is exactly where secrets belong."""
    base = base or ROOT
    files = git_visible_files(base)
    if files is None:
        files = [p for p in iter_text_files(base) if not p.name.startswith(".env")]
    hits = []
    for p in sorted(files):
        if p.name == ".env.example":
            continue
        for n, line in enumerate(read(p).splitlines(), 1):
            if IGNORE_MARKER in line:
                continue
            for label, rx in SECRET_PATTERNS:
                m = rx.search(line)
                if not m:
                    continue
                value = m.group(m.lastindex) if m.lastindex else m.group(0)
                if label == "assigned secret" and PLACEHOLDER.match(value):
                    continue
                hits.append(f"{p.relative_to(base)}:{n}: möglicher Secret ({label})")
                break
    return hits


def check_links(base: Path | None = None) -> list[str]:
    base = base or ROOT
    bad = []
    for p in base.rglob("*.md"):
        if any(part in SCAN_SKIP_DIRS for part in p.parts):
            continue
        text = re.sub(r"```.*?```", "", read(p), flags=re.S)  # ignore code blocks
        for target in re.findall(r"\]\(([^)\s]+)\)", text):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            t = target.split("#")[0]
            if t and not (p.parent / t).exists():
                bad.append(f"{p.relative_to(base)}: toter Link -> {target}")
    return bad


def check_context_expiry() -> list[str]:
    out = []
    for n, line in enumerate(read(ROOT / "BRAIN" / "CONTEXT.md").splitlines(), 1):
        m = re.search(r"expires:\s*(\d{4}-\d{2}-\d{2})", line)
        if m and m.group(1) < today():
            out.append(f"BRAIN/CONTEXT.md:{n}: abgelaufen ({m.group(1)}) -> archivieren oder verlängern")
    return out


def check_memory_size() -> list[str]:
    out = []
    for p in sorted((ROOT / "BRAIN").glob("*.md")):
        lines = len(read(p).splitlines())
        if lines > 200:
            out.append(f"BRAIN/{p.name}: {lines} Zeilen (>200) -> konsolidieren")
    return out


def check_projects() -> list[str]:
    out = []
    for p in list_projects():
        missing = [f for f in PROJECT_FILES if not (p / f).exists()]
        if missing:
            out.append(f"PROJECTS/{p.name}: fehlende Dateien {missing}")
        info = project_info(p)
        if info["status"] not in STATUSES:
            out.append(f"PROJECTS/{p.name}: unbekannter Status {info['status']!r} (erlaubt: {', '.join(STATUSES)})")
        if info["status"] in ("active", "blocked") and info["age"] is not None and info["age"] > STALE_DAYS:
            out.append(f"PROJECTS/{p.name}: seit {info['age']} Tagen nicht aktualisiert (stale)")
        if info["status"] == "active" and not info["next"]:
            out.append(f"PROJECTS/{p.name}: aktiv, aber NEXT.md ist leer")
    return out


def run_checks() -> dict[str, list[str]]:
    return {
        "Struktur": [f"fehlt: {f}" for f in REQUIRED_FILES if not (ROOT / f).exists()],
        "Secrets": scan_secrets(),
        "Links": check_links(),
        "Memory": check_context_expiry() + check_memory_size(),
        "Projekte": check_projects(),
    }


# ---------------------------------------------------------------- commands
def cmd_new_project(args) -> int:
    slug = slugify(args.name)
    if not slug:
        raise SystemExit("Ungültiger Projektname.")
    target = projects_dir() / slug
    if target.exists():
        raise SystemExit(f"Existiert bereits: PROJECTS/{slug} (nichts verändert)")
    tpl = ROOT / "TEMPLATES" / "project"
    shutil.copytree(tpl, target)
    for f in target.rglob("*.md"):
        f.write_text(read(f).replace("{{PROJECT_NAME}}", args.name).replace("{{DATE}}", today()), encoding="utf-8")
    print(f"Erstellt: PROJECTS/{slug}/")
    for f in sorted(target.rglob("*")):
        print("  ", f.relative_to(target))
    print("Nächster Schritt: PROJECT.md (Ziel, Scope, Definition of Done) ausfüllen.")
    return 0


def cmd_list(args) -> int:
    ps = [project_info(p) for p in list_projects()]
    if not ps:
        print("Keine Projekte. Anlegen mit: core.py new-project \"Name\"")
    for i in ps:
        print(f"{i['name']:<30} {i['status']:<8} offen:{len(i['open']):<3} aktualisiert:{i['updated']}")
    return 0


def cmd_status(args) -> int:
    p = find_project(args.name)
    i = project_info(p)
    print(f"# {i['title']}  [{i['status']}]  (aktualisiert {i['updated']})")
    print(f"Ziel: {i['goal'] or '- (PROJECT.md ausfüllen)'}")
    print("\nAktueller Stand:")
    for l in section(read(p / "STATUS.md"), "Aktueller Stand") or ["-"]:
        print(" ", l)
    print("\nBlocker:", *(i["blockers"] or ["keine"]), sep="\n  ")
    print(f"\nTasks: {len(i['open'])} offen, {len(i['done'])} erledigt")
    print("\nNext:", *(i["next"][:5] or ["- (NEXT.md leer)"]), sep="\n  ")
    print("\nLetzte Entscheidungen:")
    for d, t, _ in [x for x in decisions(50) if x[2] == p.name][:3] or [("-", "", "")]:
        print(f"  {d} {t}")
    return 0


def render_dashboard() -> str:
    ps = [project_info(p) for p in list_projects()]
    active = [i for i in ps if i["status"] in ("active", "blocked")]
    checks = run_checks()
    out = ["# AI CORE — Dashboard", "", f"_Generiert: {dt.datetime.now():%Y-%m-%d %H:%M} mit `python SCRIPTS/core.py dashboard --write`. Nicht von Hand bearbeiten._", ""]
    out += ["## Aktive Projekte", ""]
    out += [f"- **{i['name']}** ({i['status']}, {len(i['open'])} offene Tasks, aktualisiert {i['updated']})" for i in active] or ["- keine"]
    out += ["", "## Next Actions", ""]
    nxt = [f"{l.split('.', 1)[1].strip()} — _{i['name']}_" for i in active for l in i["next"][:2]]
    out += [f"{n}. {t}" for n, t in enumerate(nxt[:7], 1)] or ["- keine"]
    out += ["", "## Inbox", "", f"{len(inbox_items())} unverarbeitete Einträge", ""]
    out += ["## Blocker", ""]
    out += [f"- {i['name']}: {b.strip('-* ')}" for i in ps for b in i["blockers"]] or ["- keine"]
    out += ["", "## Letzte Entscheidungen", ""]
    out += [f"- {d} — {t} _({s})_" for d, t, s in decisions(5)] or ["- keine"]
    out += ["", "## System", ""]
    for name, issues in checks.items():
        out.append(f"- {name}: {'OK' if not issues else f'{len(issues)} Hinweis(e)'}")
    out += ["", f"Pausiert/fertig: {', '.join(i['name'] for i in ps if i['status'] in ('paused', 'done')) or '-'}", ""]
    return "\n".join(out)


def cmd_dashboard(args) -> int:
    text = render_dashboard()
    if args.write:
        (ROOT / "DASHBOARD.md").write_text(text, encoding="utf-8")
        print("DASHBOARD.md aktualisiert.")
    else:
        print(text)
    return 0


def cmd_check(args) -> int:
    results = {"Secrets": scan_secrets()} if args.secrets_only else run_checks()
    total = 0
    for name, issues in results.items():
        print(f"[{'OK ' if not issues else '!! '}] {name}")
        for i in issues:
            print("      ", i)
        total += len(issues)
    if args.secrets_only:
        return 1 if total else 0
    # Only structural problems and secrets fail the run; the rest are maintenance hints.
    return 1 if (results["Secrets"] or results["Struktur"]) else 0


def cmd_inbox(args) -> int:
    d = ROOT / "INBOX"
    d.mkdir(exist_ok=True)
    if args.action == "add":
        text = " ".join(args.text).strip()
        if not text:
            raise SystemExit("Leerer Inbox-Eintrag.")
        stamp = dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        path = d / f"{stamp}-{slugify(text)[:40] or 'note'}.md"
        path.write_text(f"# Inbox {stamp}\n\nSource: {args.source}\nStatus: new\n\n{text}\n", encoding="utf-8")
        print(f"Gespeichert: INBOX/{path.name}")
    else:
        items = inbox_items()
        print(f"{len(items)} Einträge")
        for p in items:
            body = [l for l in read(p).splitlines()[4:] if l.strip()]
            print(f"  {p.name}: {(body or [''])[0][:80]}")
    return 0


def cmd_weekly(args) -> int:
    year, week, _ = dt.date.today().isocalendar()
    lines = [f"# Weekly Review {year}-W{week:02d}", "", f"_Generiert {today()}. Entwurf — bitte prüfen, dann Entscheidungen in Projekte übernehmen._", ""]
    for i in (project_info(p) for p in list_projects()):
        stale = i["age"] is not None and i["age"] > STALE_DAYS and i["status"] != "done"
        lines += [f"## {i['name']} ({i['status']}){' — STALE' if stale else ''}", "",
                  f"- Offene Tasks: {len(i['open'])}, erledigt: {len(i['done'])}",
                  f"- Blocker: {'; '.join(b.strip('-* ') for b in i['blockers']) or 'keine'}",
                  f"- Next: {i['next'][0].split('.', 1)[1].strip() if i['next'] else '(leer)'}", ""]
    lines += ["## Inbox", "", f"{len(inbox_items())} unverarbeitete Einträge", "", "## System-Hinweise", ""]
    lines += [f"- {k}: {x}" for k, v in run_checks().items() for x in v] or ["- keine"]
    out = ROOT / "OUTPUT" / f"weekly-review-{year}-W{week:02d}.md"
    out.parent.mkdir(exist_ok=True)
    if out.exists() and not args.force:
        raise SystemExit(f"Existiert bereits: {out.relative_to(ROOT)} (--force zum Überschreiben)")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Geschrieben: {out.relative_to(ROOT)}")
    return 0


def cmd_archive(args) -> int:
    p = find_project(args.name)
    if project_info(p)["status"] != "done":
        raise SystemExit("Erst 'Status: done' in STATUS.md setzen (Abschluss bewusst bestätigen), dann archivieren.")
    dest = ROOT / "ARCHIVE" / "projects" / f"{today()}-{p.name}"
    if dest.exists():
        raise SystemExit(f"Ziel existiert bereits: {dest.relative_to(ROOT)}")
    if not args.yes:
        if input(f"PROJECTS/{p.name} nach {dest.relative_to(ROOT)} verschieben? [j/N] ").strip().lower() not in ("j", "y", "ja", "yes"):
            print("Abgebrochen.")
            return 1
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(p), str(dest))
    print(f"Archiviert (verschoben, nicht gelöscht): {dest.relative_to(ROOT)}")
    return 0


def cmd_install_hook(args) -> int:
    top = ROOT
    while not (top / ".git").exists():
        if top.parent == top:
            raise SystemExit("Kein Git-Repository gefunden.")
        top = top.parent
    hook = top / ".git" / "hooks" / "pre-commit"
    if hook.exists():
        raise SystemExit(f"{hook} existiert bereits — nicht überschrieben. Bitte manuell zusammenführen.")
    rel = os.path.relpath(Path(__file__).resolve(), top).replace(os.sep, "/")
    hook.write_text("#!/bin/sh\n# AI-CORE: block commits that contain likely secrets\n"
                    "if command -v python3 >/dev/null 2>&1; then PY=python3; else PY=python; fi\n"
                    f"exec \"$PY\" \"{rel}\" check --secrets-only\n", encoding="utf-8")
    hook.chmod(0o755)
    print(f"Installiert: {hook}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="core.py", description="AI-CORE Werkzeug (nur Standardbibliothek).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("new-project", help="Projektstruktur aus TEMPLATES/project anlegen")
    s.add_argument("name"); s.set_defaults(fn=cmd_new_project)
    sub.add_parser("list", help="Alle Projekte mit Status").set_defaults(fn=cmd_list)
    s = sub.add_parser("status", help="Projektstand zusammenfassen"); s.add_argument("name"); s.set_defaults(fn=cmd_status)
    s = sub.add_parser("dashboard", help="Dashboard anzeigen (--write: DASHBOARD.md schreiben)")
    s.add_argument("--write", action="store_true"); s.set_defaults(fn=cmd_dashboard)
    s = sub.add_parser("check", help="Struktur, Secrets, Links, Memory, Projekte prüfen")
    s.add_argument("--secrets-only", action="store_true"); s.set_defaults(fn=cmd_check)
    s = sub.add_parser("inbox", help="Inbox: add <text> | list")
    s.add_argument("action", choices=["add", "list"]); s.add_argument("text", nargs="*")
    s.add_argument("--source", default="manual"); s.set_defaults(fn=cmd_inbox)
    s = sub.add_parser("weekly", help="Weekly-Review-Entwurf nach OUTPUT/ schreiben")
    s.add_argument("--force", action="store_true"); s.set_defaults(fn=cmd_weekly)
    s = sub.add_parser("archive", help="Abgeschlossenes Projekt nach ARCHIVE/ verschieben")
    s.add_argument("name"); s.add_argument("--yes", action="store_true"); s.set_defaults(fn=cmd_archive)
    sub.add_parser("install-hook", help="Git pre-commit Secret-Scan installieren").set_defaults(fn=cmd_install_hook)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        sys.exit(main())
    except BrokenPipeError:  # output piped into e.g. `head`
        sys.exit(0)
