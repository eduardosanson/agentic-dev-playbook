#!/usr/bin/env python3
"""
Cria um PR no GitHub com descrição automática.
"""

import subprocess
import json
import sys

def create_pr(branch, title, body):
    """
    Cria um PR usando GitHub CLI.
    """

    try:
        result = subprocess.run(
            [
                'gh',
                'pr',
                'create',
                '--base', 'main',
                '--head', branch,
                '--title', title,
                '--body', body
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            # Extrair URL do PR da saída
            output = result.stdout.strip()
            return True, output
        else:
            return False, result.stderr

    except Exception as e:
        return False, str(e)

def main():
    if len(sys.argv) < 4:
        print(json.dumps({
            'success': False,
            'error': 'Usage: create_pr.py <branch> <title> <body>'
        }))
        sys.exit(1)

    branch = sys.argv[1]
    title = sys.argv[2]
    body = sys.argv[3]

    success, output = create_pr(branch, title, body)

    if success:
        print(json.dumps({
            'success': True,
            'pr_url': output
        }))
    else:
        print(json.dumps({
            'success': False,
            'error': output
        }))
        sys.exit(1)

if __name__ == '__main__':
    main()
