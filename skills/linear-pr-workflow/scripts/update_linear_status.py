#!/usr/bin/env python3
"""
Atualiza status de uma tarefa no Linear.
"""

import subprocess
import json
import sys

def update_issue_status(issue_id, new_status):
    """
    Atualiza status de uma issue no Linear.
    Statuses válidos: Backlog, Todo, In Progress, In Review, Done
    """

    try:
        # Usar Linear CLI
        result = subprocess.run(
            [
                'linear',
                'issue',
                'update',
                issue_id,
                '--status',
                new_status
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return True
        else:
            print(f"Error: {result.stderr}", file=sys.stderr)
            return False

    except Exception as e:
        print(f"Exception: {str(e)}", file=sys.stderr)
        return False

def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            'success': False,
            'error': 'Usage: update_linear_status.py <issue_id> <new_status>'
        }))
        sys.exit(1)

    issue_id = sys.argv[1]
    new_status = sys.argv[2]

    # Validar status
    valid_statuses = ['Backlog', 'Todo', 'In Progress', 'In Review', 'Done']
    if new_status not in valid_statuses:
        print(json.dumps({
            'success': False,
            'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
        }))
        sys.exit(1)

    # Atualizar
    if update_issue_status(issue_id, new_status):
        print(json.dumps({
            'success': True,
            'issue_id': issue_id,
            'status': new_status
        }))
    else:
        print(json.dumps({
            'success': False,
            'error': f'Could not update {issue_id} to {new_status}'
        }))
        sys.exit(1)

if __name__ == '__main__':
    main()
