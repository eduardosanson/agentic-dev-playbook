#!/usr/bin/env python3
"""
Dependency analyzer for Linear tasks.
Processes dependency data and generates analysis.
"""

import json
import sys
from typing import Dict, List, Set, Tuple
from collections import defaultdict, deque


class DependencyGraph:
    def __init__(self):
        self.tasks = {}  # task_id -> task_data
        self.blocks = defaultdict(set)  # task_id -> set of task_ids it blocks
        self.blocked_by = defaultdict(set)  # task_id -> set of task_ids blocking it

    def add_task(self, task_id: str, task_data: dict):
        """Add a task to the graph."""
        self.tasks[task_id] = task_data

    def add_relationship(self, task_id: str, blocks_task_id: str):
        """Add a 'blocks' relationship: task_id blocks blocks_task_id."""
        self.blocks[task_id].add(blocks_task_id)
        self.blocked_by[blocks_task_id].add(task_id)

    def get_blocked_tasks(self) -> List[Tuple[str, Set[str]]]:
        """Return list of (task_id, blocking_tasks) for tasks that are blocked."""
        return [(tid, self.blocked_by[tid]) for tid in self.tasks if self.blocked_by[tid]]

    def get_critical_tasks(self) -> List[Tuple[str, int]]:
        """Return list of (task_id, count) for tasks blocking many others, sorted by count."""
        return sorted(
            [(tid, len(blocked)) for tid, blocked in self.blocks.items() if blocked],
            key=lambda x: x[1],
            reverse=True
        )

    def find_cycles(self) -> List[List[str]]:
        """Find all cycles in the dependency graph using DFS."""
        visited = set()
        rec_stack = set()
        cycles = []

        def dfs(node, path):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.blocks[node]:
                if neighbor not in visited:
                    dfs(neighbor, path + [neighbor])
                elif neighbor in rec_stack:
                    # Found a cycle
                    cycle_start = path.index(neighbor) if neighbor in path else 0
                    cycles.append(path[cycle_start:] + [neighbor])

            rec_stack.discard(node)

        for task_id in self.tasks:
            if task_id not in visited:
                dfs(task_id, [task_id])

        return cycles

    def find_critical_path(self) -> List[str]:
        """Find the longest path in the dependency graph (critical path)."""
        # Use topological sort + dynamic programming
        in_degree = {tid: len(self.blocked_by[tid]) for tid in self.tasks}
        queue = deque([tid for tid in self.tasks if in_degree[tid] == 0])
        path_length = {tid: 1 for tid in self.tasks}
        parent = {tid: None for tid in self.tasks}

        while queue:
            node = queue.popleft()
            for dependent in self.blocks[node]:
                if path_length[dependent] < path_length[node] + 1:
                    path_length[dependent] = path_length[node] + 1
                    parent[dependent] = node
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # Reconstruct longest path
        longest = max(self.tasks.keys(), key=lambda x: path_length[x])
        path = []
        current = longest
        while current:
            path.insert(0, current)
            current = parent[current]

        return path

    def get_ready_tasks(self) -> List[str]:
        """Return tasks with no blocking dependencies (ready to start)."""
        return [tid for tid in self.tasks if not self.blocked_by[tid]]

    def get_impact_of_task(self, task_id: str) -> Set[str]:
        """Return all tasks that would be unblocked if this task is completed."""
        impacted = set()
        visited = set()

        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for dependent in self.blocks[node]:
                # Check if dependent would be fully unblocked
                blocking_count = len(self.blocked_by[dependent]) - (1 if node in self.blocked_by[dependent] else 0)
                if blocking_count == 0:
                    impacted.add(dependent)
                dfs(dependent)

        dfs(task_id)
        return impacted


def analyze_tasks(tasks_data: List[dict], relationships_data: List[dict]) -> dict:
    """
    Analyze task dependencies.

    Args:
        tasks_data: List of task objects with id, title, status
        relationships_data: List of relationship objects with task_id, blocks_task_id

    Returns:
        Analysis results dictionary
    """
    graph = DependencyGraph()

    # Add tasks
    for task in tasks_data:
        graph.add_task(task['id'], task)

    # Add relationships
    for rel in relationships_data:
        if rel['task_id'] in graph.tasks and rel['blocks_task_id'] in graph.tasks:
            graph.add_relationship(rel['task_id'], rel['blocks_task_id'])

    # Run analyses
    blocked_tasks = graph.get_blocked_tasks()
    critical_tasks = graph.get_critical_tasks()
    cycles = graph.find_cycles()
    critical_path = graph.find_critical_path()
    ready_tasks = graph.get_ready_tasks()

    return {
        'total_tasks': len(graph.tasks),
        'blocked_count': len(blocked_tasks),
        'critical_count': len(critical_tasks),
        'blocked_tasks': [
            {'task_id': tid, 'title': graph.tasks[tid].get('title', 'Unknown'),
             'status': graph.tasks[tid].get('status', 'Unknown'),
             'blocking': list(blocked)}
            for tid, blocked in blocked_tasks
        ],
        'critical_tasks': [
            {'task_id': tid, 'title': graph.tasks[tid].get('title', 'Unknown'),
             'blocks_count': count}
            for tid, count in critical_tasks
        ],
        'critical_path': [
            {'task_id': tid, 'title': graph.tasks[tid].get('title', 'Unknown')}
            for tid in critical_path
        ],
        'ready_tasks': [
            {'task_id': tid, 'title': graph.tasks[tid].get('title', 'Unknown')}
            for tid in ready_tasks
        ],
        'cycles': cycles,
        'graph': {
            'tasks': {tid: {'title': t.get('title', 'Unknown'), 'status': t.get('status', 'Unknown')}
                     for tid, t in graph.tasks.items()},
            'relationships': [
                {'from': tid, 'to': blocked, 'type': 'blocks'}
                for tid, blocked_set in graph.blocks.items()
                for blocked in blocked_set
            ]
        }
    }


if __name__ == '__main__':
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Analyze
    results = analyze_tasks(
        input_data.get('tasks', []),
        input_data.get('relationships', [])
    )

    # Output results
    print(json.dumps(results, indent=2))
