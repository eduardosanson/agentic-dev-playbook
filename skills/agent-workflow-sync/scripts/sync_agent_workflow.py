#!/usr/bin/env python3
import argparse
import hashlib
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


TARGETS = {
    "codex": Path.home() / ".codex" / "AGENTS.md",
    "claude": Path.home() / ".claude" / "CLAUDE.md",
    "home": Path.home() / "AGENTS.md",
}

SOURCE_PATHS = {
    "codex": Path("agent-rules/codex/AGENTS.md"),
    "claude": Path("agent-rules/claude/CLAUDE.md"),
    "home": Path("AGENTS.md"),
}

def detect_agent() -> str | None:
    if (Path.home() / ".codex" / "AGENTS.md").exists():
        return "codex"
    if (Path.home() / ".claude" / "CLAUDE.md").exists():
        return "claude"
    if (Path.home() / "AGENTS.md").exists():
        return "home"
    return None


def file_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def resolve_source_path(repo_root: Path, agent: str) -> Path:
    preferred = repo_root / SOURCE_PATHS[agent]
    if preferred.is_file():
        return preferred
    fallback = repo_root / "AGENTS.md"
    if fallback.is_file():
        return fallback
    raise FileNotFoundError(f"Missing source file for agent '{agent}'")


def load_local_source(repo_root: Path, agent: str) -> tuple[str, str]:
    source_path = resolve_source_path(repo_root, agent)
    if not source_path.is_file():
        raise FileNotFoundError(f"Missing source file: {source_path}")
    return source_path.read_text(encoding="utf-8"), str(source_path.relative_to(repo_root))


def load_remote_source(repo_root: Path, agent: str) -> tuple[str, str]:
    relative_source = str(SOURCE_PATHS[agent])
    fetch = subprocess.run(
        ["git", "-C", str(repo_root), "fetch", "origin", "main"],
        capture_output=True,
        text=True,
        check=False,
    )
    if fetch.returncode != 0:
        raise RuntimeError(fetch.stderr.strip() or "git fetch failed")
    show = subprocess.run(
        ["git", "-C", str(repo_root), "show", f"origin/main:{relative_source}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if show.returncode != 0:
        fallback_show = subprocess.run(
            ["git", "-C", str(repo_root), "show", "origin/main:AGENTS.md"],
            capture_output=True,
            text=True,
            check=False,
        )
        if fallback_show.returncode != 0:
            raise RuntimeError(show.stderr.strip() or "git show failed for agent-specific and fallback sources")
        return fallback_show.stdout, "AGENTS.md"
    return show.stdout, relative_source


def backup_and_write(path: Path, content: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup = path.with_name(f"{path.name}.bak.{stamp}")
        shutil.copy2(path, backup)
    path.write_text(content, encoding="utf-8")
    return "updated"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--fetch-remote", action="store_true")
    parser.add_argument("--agent", choices=sorted(TARGETS.keys()))
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    agent = args.agent or detect_agent()
    if agent is None:
        print("Could not detect current agent. Pass --agent codex|claude|home.", file=sys.stderr)
        return 1

    try:
        if args.fetch_remote:
            source_content, source_relpath = load_remote_source(repo_root, agent)
            source_kind = f"origin/main:{source_relpath}"
        else:
            source_content, source_relpath = load_local_source(repo_root, agent)
            source_kind = f"local {source_relpath}"
    except Exception as exc:
        if args.fetch_remote:
            source_content, source_relpath = load_local_source(repo_root, agent)
            source_kind = f"local {source_relpath} (remote fetch failed: {exc})"
        else:
            print(str(exc), file=sys.stderr)
            return 1

    path = TARGETS[agent]
    source_digest = file_hash(source_content)
    if not path.exists():
        if args.apply:
            backup_and_write(path, source_content)
            status = "created"
            detail = "target did not exist and was created"
        else:
            status = "missing"
            detail = "target file not found"
    else:
        current = path.read_text(encoding="utf-8")
        if file_hash(current) == source_digest:
            status = "up-to-date"
            detail = "content already aligned"
        elif args.apply:
            backup_and_write(path, source_content)
            status = "updated"
            detail = "content replaced from source"
        else:
            status = "outdated"
            detail = "content differs from source"

    print(f"Source used: {source_kind}")
    print("Workflow sync report:")
    print(f"- agent: {agent}")
    print(f"- target: {path}")
    print(f"- status: {status}")
    print(f"- detail: {detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
