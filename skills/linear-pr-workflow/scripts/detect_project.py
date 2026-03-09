#!/usr/bin/env python3
"""
Detecta o projeto Linear baseado no repositório Git atual.
Retorna workspace e projectId do Linear.
"""

import subprocess
import json
import sys
from pathlib import Path

def get_git_remote():
    """Obtém URL do origin do Git."""
    try:
        result = subprocess.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def extract_repo_info(git_url):
    """Extrai owner/repo da URL do Git."""
    if not git_url:
        return None, None

    # Suporta https://github.com/user/repo.git e git@github.com:user/repo.git
    if 'github.com' in git_url:
        parts = git_url.replace('git@github.com:', '').replace('https://github.com/', '').split('/')
        if len(parts) >= 2:
            owner = parts[0]
            repo = parts[1].replace('.git', '')
            return owner, repo

    return None, None

def map_repo_to_linear():
    """
    Mapeia repositório Git para workspace/projeto Linear.

    Mapping padrão:
    - athlete-android → SofIA BR / Android App
    - athlete-web → SofIA BR / Frontend Web
    - athlete-backend → SofIA BR / Backend
    """

    git_url = get_git_remote()
    owner, repo = extract_repo_info(git_url)

    if not owner or not repo:
        return None

    # Mapping de repositórios conhecidos
    mapping = {
        'athlete-android': {
            'workspace': 'SofIA BR',
            'project': 'Android App',
            'workspace_id': 'fc98d85c-90f4-4fbe-89d3-1253128fc431'
        },
        'athlete-web': {
            'workspace': 'SofIA BR',
            'project': 'Frontend Web',
            'workspace_id': 'fc98d85c-90f4-4fbe-89d3-1253128fc431'
        },
        'athlete-backend': {
            'workspace': 'SofIA BR',
            'project': 'Backend',
            'workspace_id': 'fc98d85c-90f4-4fbe-89d3-1253128fc431'
        }
    }

    if repo in mapping:
        return mapping[repo]

    return None

def main():
    result = map_repo_to_linear()

    if not result:
        print(json.dumps({
            'success': False,
            'error': 'Could not auto-detect Linear project. Please specify manually.'
        }))
        sys.exit(1)

    print(json.dumps({
        'success': True,
        'workspace': result['workspace'],
        'project': result['project'],
        'workspace_id': result['workspace_id']
    }))

if __name__ == '__main__':
    main()
