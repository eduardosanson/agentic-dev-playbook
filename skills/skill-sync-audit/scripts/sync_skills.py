#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".DS_Store"}
TARGET_ROOTS = {
    "claude": Path.home() / ".claude" / "skills",
    "codex": Path.home() / ".codex" / "skills",
}


@dataclass
class SkillMeta:
    name: str
    path: Path
    description: str
    digest: str


def normalize_tokens(text: str) -> set:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def dir_digest(path: Path) -> str:
    hasher = hashlib.sha256()
    for entry in sorted(p for p in path.rglob("*") if p.is_file() and not any(part in IGNORE_DIRS for part in p.parts)):
        rel = entry.relative_to(path)
        hasher.update(str(rel).encode("utf-8"))
        hasher.update(entry.read_bytes())
    return hasher.hexdigest()


def parse_skill(path: Path) -> SkillMeta:
    content = path.read_text(encoding="utf-8")
    name_match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    desc_match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else path.parent.name
    description = desc_match.group(1).strip() if desc_match else ""
    return SkillMeta(name=name, path=path.parent, description=description, digest=dir_digest(path.parent))


def load_skills(root: Path) -> Dict[str, SkillMeta]:
    skills = {}
    if not root.exists():
        return skills
    for skill_md in sorted(root.glob("*/SKILL.md")):
        meta = parse_skill(skill_md)
        skills[meta.path.name] = meta
    return skills


def detect_agent() -> str | None:
    if (Path.home() / ".codex" / "skills").exists():
        return "codex"
    if (Path.home() / ".claude" / "skills").exists():
        return "claude"
    return None


def similarity(repo_skill: SkillMeta, installed: SkillMeta) -> float:
    a = normalize_tokens(repo_skill.name + " " + repo_skill.description + " " + repo_skill.path.name)
    b = normalize_tokens(installed.name + " " + installed.description + " " + installed.path.name)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def backup_dir(path: Path) -> None:
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup = path.with_name(f"{path.name}.bak.{stamp}")
    shutil.copytree(path, backup)


def replace_dir(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        backup_dir(target)
        shutil.rmtree(target)
    shutil.copytree(source, target)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--install-missing", action="store_true")
    parser.add_argument("--agent", choices=sorted(TARGET_ROOTS.keys()))
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    repo_skills = load_skills(repo_root / "skills")

    agent = args.agent or detect_agent()
    if agent is None:
        print("Could not detect current agent. Pass --agent codex|claude.", file=sys.stderr)
        return 1

    target_root = TARGET_ROOTS[agent]
    installed_skills = load_skills(target_root)
    report = {"agent": agent, "target_root": str(target_root), "present": [], "missing": [], "outdated": [], "updated": [], "installed": [], "similar": []}

    for skill_dir_name, repo_skill in repo_skills.items():
        installed = installed_skills.get(skill_dir_name)
        if installed is None:
            report["missing"].append(skill_dir_name)
            candidates: List[Tuple[float, str]] = []
            for other_name, other_skill in installed_skills.items():
                score = similarity(repo_skill, other_skill)
                if score >= 0.18:
                    candidates.append((score, other_name))
            if candidates:
                candidates.sort(reverse=True)
                pretty = ", ".join(f"{name} ({score:.2f})" for score, name in candidates[:3])
                report["similar"].append(f"{skill_dir_name}: {pretty}")
            elif args.apply and args.install_missing:
                replace_dir(repo_skill.path, target_root / skill_dir_name)
                report["installed"].append(skill_dir_name)
            continue

        report["present"].append(skill_dir_name)
        if installed.digest != repo_skill.digest:
            report["outdated"].append(skill_dir_name)
            if args.apply:
                replace_dir(repo_skill.path, target_root / skill_dir_name)
                report["updated"].append(skill_dir_name)

    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
