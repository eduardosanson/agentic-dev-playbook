#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


SUPERPOWERS_REPO_URL = "https://github.com/obra/superpowers.git"
SUPERPOWERS_CLONE_DIR = Path.home() / ".codex" / "superpowers"
SUPERPOWERS_LINK = Path.home() / ".agents" / "skills" / "superpowers"
CODEX_SKILLS_DIR = Path.home() / ".codex" / "skills"
RULES_DIR = Path.home() / ".codex" / "rules"
STATE_FILE = RULES_DIR / "agentic-dev-playbook-superpowers-state.json"
LOG_FILE = RULES_DIR / "agentic-dev-playbook-superpowers-log.jsonl"
PROJECT_SKILLS_DIRNAME = "skills"
CURSOR_RULE_SOURCE = Path("agent-rules/cursor/agentic-dev-playbook.mdc")
WINDSURF_RULE_SOURCE = Path("agent-rules/windsurf/agentic-dev-playbook.md")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_replacements(repo_root: Path) -> dict[str, str]:
    path = repo_root / PROJECT_SKILLS_DIRNAME / "superpowers-sync" / "config" / "replacements.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {"managed_project_skills": [], "superseded_project_skills": {}, "superpowers_repo": str(SUPERPOWERS_CLONE_DIR)}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    RULES_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def append_log(payload: dict) -> None:
    RULES_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=True) + "\n")


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True, check=check)


def ensure_superpowers(apply: bool) -> list[str]:
    actions = []
    if not SUPERPOWERS_CLONE_DIR.exists():
        if apply:
            SUPERPOWERS_CLONE_DIR.parent.mkdir(parents=True, exist_ok=True)
            run(["git", "clone", SUPERPOWERS_REPO_URL, str(SUPERPOWERS_CLONE_DIR)])
            actions.append(f"cloned:{SUPERPOWERS_CLONE_DIR}")
        else:
            actions.append(f"missing-clone:{SUPERPOWERS_CLONE_DIR}")
    else:
        if apply:
            run(["git", "-C", str(SUPERPOWERS_CLONE_DIR), "pull", "--ff-only"])
            actions.append(f"updated-clone:{SUPERPOWERS_CLONE_DIR}")
        else:
            actions.append(f"clone-present:{SUPERPOWERS_CLONE_DIR}")

    target = SUPERPOWERS_CLONE_DIR / "skills"
    if SUPERPOWERS_LINK.is_symlink() or SUPERPOWERS_LINK.exists():
        if SUPERPOWERS_LINK.is_symlink() and os.readlink(SUPERPOWERS_LINK) == str(target):
            actions.append(f"link-ok:{SUPERPOWERS_LINK}")
        elif apply:
            backup = SUPERPOWERS_LINK.with_name(f"{SUPERPOWERS_LINK.name}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}")
            shutil.move(str(SUPERPOWERS_LINK), str(backup))
            SUPERPOWERS_LINK.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(str(target), str(SUPERPOWERS_LINK))
            actions.append(f"relinked:{SUPERPOWERS_LINK}")
        else:
            actions.append(f"link-needs-fix:{SUPERPOWERS_LINK}")
    else:
        if apply:
            SUPERPOWERS_LINK.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(str(target), str(SUPERPOWERS_LINK))
            actions.append(f"linked:{SUPERPOWERS_LINK}")
        else:
            actions.append(f"missing-link:{SUPERPOWERS_LINK}")
    return actions


def backup_path(path: Path) -> Path:
    return path.with_name(f"{path.name}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}")


def backup_and_remove(path: Path) -> str:
    backup = backup_path(path)
    shutil.move(str(path), str(backup))
    return str(backup)


def copy_skill(source: Path, target: Path) -> None:
    if target.exists():
        backup = backup_path(target)
        shutil.move(str(target), str(backup))
    shutil.copytree(source, target)


def sync_project_skills(repo_root: Path, apply: bool) -> dict:
    project_skills_dir = repo_root / PROJECT_SKILLS_DIRNAME
    replacements = load_replacements(repo_root)
    state = load_state()

    current_project_skills = sorted(
        p.name for p in project_skills_dir.iterdir()
        if p.is_dir() and (p / "SKILL.md").exists()
    )

    managed_before = set(state.get("managed_project_skills", []))
    superseded_before = set(state.get("superseded_project_skills", {}).keys())

    report = {
        "managed_present": [],
        "managed_updated": [],
        "managed_installed": [],
        "managed_removed": [],
        "superseded_removed": [],
        "superseded_skipped": [],
        "replacement_map": replacements,
    }

    CODEX_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    for skill_name in current_project_skills:
        if skill_name == "superpowers-sync":
            continue
        source = project_skills_dir / skill_name
        target = CODEX_SKILLS_DIR / skill_name
        if skill_name in replacements:
            report["superseded_skipped"].append(skill_name)
            if target.exists() and apply:
                backup_and_remove(target)
                report["superseded_removed"].append(skill_name)
            continue

        if target.exists():
            report["managed_present"].append(skill_name)
            if apply:
                copy_skill(source, target)
                report["managed_updated"].append(skill_name)
        else:
            if apply:
                shutil.copytree(source, target)
                report["managed_installed"].append(skill_name)

    still_existing = set(current_project_skills)
    for old_skill in sorted(managed_before):
        if old_skill not in still_existing and old_skill not in replacements:
            target = CODEX_SKILLS_DIR / old_skill
            if target.exists() and apply:
                backup_and_remove(target)
                report["managed_removed"].append(old_skill)

    for old_skill in sorted(superseded_before):
        if old_skill not in still_existing:
            target = CODEX_SKILLS_DIR / old_skill
            if target.exists() and apply:
                backup_and_remove(target)
                report["managed_removed"].append(old_skill)

    new_state = {
        "managed_project_skills": sorted(
            skill for skill in current_project_skills
            if skill not in replacements and skill != "superpowers-sync"
        ),
        "superseded_project_skills": replacements,
        "superpowers_repo": str(SUPERPOWERS_CLONE_DIR),
        "last_sync": now_iso(),
    }
    if apply:
        save_state(new_state)
    return report


def export_editor_rules(repo_root: Path, workspace_root: Path, apply: bool) -> dict:
    report = {
        "cursor": {"target": str(workspace_root / ".cursor" / "rules" / "agentic-dev-playbook.mdc"), "status": "skipped"},
        "windsurf": {"target": str(workspace_root / ".windsurf" / "rules" / "agentic-dev-playbook.md"), "status": "skipped"},
        "notes": [
            "Cursor official Superpowers install uses marketplace command: /add-plugin superpowers",
            "Windsurf compatibility in this project is provided through workspace rule files; no official upstream Superpowers install path for Windsurf was detected in the inspected repository"
        ],
    }

    cursor_source = repo_root / CURSOR_RULE_SOURCE
    windsurf_source = repo_root / WINDSURF_RULE_SOURCE

    if apply:
        cursor_target = workspace_root / ".cursor" / "rules" / "agentic-dev-playbook.mdc"
        cursor_target.parent.mkdir(parents=True, exist_ok=True)
        cursor_target.write_text(cursor_source.read_text(encoding="utf-8"), encoding="utf-8")
        report["cursor"]["status"] = "written"

        windsurf_target = workspace_root / ".windsurf" / "rules" / "agentic-dev-playbook.md"
        windsurf_target.parent.mkdir(parents=True, exist_ok=True)
        windsurf_target.write_text(windsurf_source.read_text(encoding="utf-8"), encoding="utf-8")
        report["windsurf"]["status"] = "written"
    else:
        report["cursor"]["status"] = "available"
        report["windsurf"]["status"] = "available"

    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--workspace-root")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    workspace_root = Path(args.workspace_root).expanduser().resolve() if args.workspace_root else None

    superpowers_actions = ensure_superpowers(args.apply)
    skills_report = sync_project_skills(repo_root, args.apply)
    editor_report = export_editor_rules(repo_root, workspace_root, args.apply) if workspace_root else {
        "cursor": {"status": "not-requested"},
        "windsurf": {"status": "not-requested"},
        "notes": ["Pass --workspace-root to materialize Cursor and Windsurf workspace rule files"],
    }

    payload = {
        "timestamp": now_iso(),
        "repo_root": str(repo_root),
        "workspace_root": str(workspace_root) if workspace_root else None,
        "apply": args.apply,
        "superpowers": superpowers_actions,
        "editors": editor_report,
        "skills": skills_report,
    }
    if args.apply:
        append_log(payload)

    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
