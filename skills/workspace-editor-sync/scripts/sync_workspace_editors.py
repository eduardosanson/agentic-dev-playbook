#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


CURSOR_RULE_SOURCE = Path("agent-rules/cursor/agentic-dev-playbook.mdc")
WINDSURF_RULE_SOURCE = Path("agent-rules/windsurf/agentic-dev-playbook.md")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def export_editor_rules(repo_root: Path, workspace_root: Path, apply: bool) -> dict:
    report = {
        "timestamp": now_iso(),
        "repo_root": str(repo_root),
        "workspace_root": str(workspace_root),
        "apply": apply,
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
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    workspace_root = Path(args.workspace_root).expanduser().resolve()
    payload = export_editor_rules(repo_root, workspace_root, args.apply)
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
