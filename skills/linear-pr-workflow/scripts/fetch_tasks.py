#!/usr/bin/env python3
"""
Busca tasks em TODO no Linear ordenadas por prioridade.
"""

import subprocess
import json
import sys

def fetch_linear_tasks(workspace_id, team_name='SofIA BR'):
    """
    Busca tasks em TODO usando Linear CLI.
    Retorna JQL para tasks em Todo status ordenadas por prioridade.
    """

    try:
        # Usar Linear CLI para buscar tasks
        result = subprocess.run(
            [
                'gh',
                'api',
                f'graphql',
                '-f',
                f'query=query {{ team(key: "SofIA") {{ issues(filter: {{ status: {{ name: "Todo" }} }}) {{ edges {{ node {{ id identifier title priority {{ value }} }} }} }} }} }}'
            ],
            capture_output=True,
            text=True,
            cwd='/tmp'  # Rodar longe do repo
        )

        if result.returncode != 0:
            # Fallback: usar jq para buscar tasks diretamente
            return fetch_tasks_fallback()

        return json.loads(result.stdout)

    except Exception as e:
        return fetch_tasks_fallback()

def fetch_tasks_fallback():
    """
    Fallback: tenta buscar usando linear command diretamente.
    """
    try:
        result = subprocess.run(
            [
                'linear',
                'issue',
                'list',
                '--filter',
                'status:Todo',
                '--output',
                'json'
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            raise Exception(f"Linear command failed: {result.stderr}")

    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': f'Could not fetch tasks from Linear: {str(e)}'
        }), file=sys.stderr)
        return None

def sort_by_priority(tasks):
    """
    Ordena tasks por prioridade (decrescente: urgent → low).
    Linear usa: 1=Urgent, 2=High, 3=Medium, 4=Low, 0=None
    """
    if not tasks:
        return []

    def priority_key(task):
        priority = task.get('priority', {}).get('value', 0)
        # Inverte: 1 (Urgent) vem primeiro
        return (-priority, task.get('identifier', ''))

    return sorted(tasks, key=priority_key)

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False,
            'error': 'Usage: fetch_tasks.py <workspace_id>'
        }), file=sys.stderr)
        sys.exit(1)

    workspace_id = sys.argv[1]

    # Buscar tasks
    tasks = fetch_linear_tasks(workspace_id)

    if not tasks:
        print(json.dumps({
            'success': False,
            'error': 'Could not fetch tasks'
        }))
        sys.exit(1)

    # Extrair issues e ordenar
    issues = []
    if isinstance(tasks, dict) and 'data' in tasks:
        issues = tasks['data']
    elif isinstance(tasks, dict) and 'issues' in tasks:
        issues = tasks['issues']
    elif isinstance(tasks, list):
        issues = tasks

    sorted_issues = sort_by_priority(issues)

    print(json.dumps({
        'success': True,
        'tasks': sorted_issues,
        'count': len(sorted_issues)
    }))

if __name__ == '__main__':
    main()
