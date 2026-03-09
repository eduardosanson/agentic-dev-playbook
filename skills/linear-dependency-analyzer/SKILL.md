---
name: linear-dependency-analyzer
description: |
  Analyzes task dependencies in Linear projects to identify blockers, critical paths, and impact analysis. Use this skill whenever you need to: understand how tasks are blocking each other in a Linear project; identify which tasks are critical (blocking many others); see the full dependency graph of a project; determine what tasks are blocked and why; analyze the impact of completing a specific task; find the optimal execution order; or detect circular dependencies. This skill fetches data directly from Linear API, generates visual dependency maps in Markdown, and suggests status updates without modifying tasks. Perfect for sprint planning, roadmap analysis, and unblocking teams. Always use this skill when the user asks about dependencies, blockers, critical paths, task relationships, or impact analysis in Linear.
compatibility: Requires Linear API access via claude's Linear tools
---

# Linear Dependency Analyzer

## Resumo

Analisa dependências entre tarefas no Linear para identificar bloqueios, caminho crítico, impacto de conclusão e ordem de execução recomendada.

This skill analyzes task dependencies in Linear projects to help you understand blockers, identify critical paths, and evaluate impact of task completions.

## How It Works

1. **Discover Project Context**
   - Try to infer the project/team from conversation context (e.g., previous Linear mentions)
   - If unclear, ask the user which project/team to analyze
   - Only analyze tasks with status NOT in: Backlog, Refined

2. **Fetch Dependency Data**
   - Use Linear API (via claude's Linear tools) to get:
     - All tasks in the project
     - Relationship data (which tasks block which)
   - Filter out Backlog and Refined status tasks
   - Build a dependency graph

3. **Analyze & Visualize**
   - Identify blocked tasks (tasks waiting on others)
   - Identify critical tasks (those blocking many others)
   - Detect circular dependencies (warn if found)
   - Generate Markdown visualization with:
     - Dependency graph (ASCII or table format)
     - Blocked tasks list with reasons
     - Critical path analysis
     - Suggestions for execution order

4. **Suggest Updates** (Never Modify)
   - Suggest status updates for unblocked tasks
   - Recommend priority shifts based on critical path
   - Show impact of completing specific tasks
   - Present as recommendations, not automatic changes

## Output Format

Always generate a structured Markdown report with these sections:

### 📊 Dependency Overview
Brief summary: total tasks, blocked count, critical tasks count, any circular dependencies detected.

### 🔗 Dependency Graph
Visual representation using:
- Table format: Task ID → Dependencies → Blocked By → Status
- Or ASCII tree if hierarchical
- Color coding in description: 🔴 Blocked, 🟡 Critical, 🟢 Ready

### 🚧 Blocked Tasks
List of tasks that cannot proceed:
- Task ID and title
- Blocking tasks (what they're waiting for)
- Estimated unblock time if possible

### ⭐ Critical Tasks
Tasks that block many others (high impact):
- Task ID and title
- Number of tasks depending on this one
- Recommendation to prioritize

### 🛣️ Critical Path
Longest chain of dependencies:
- Sequence of tasks that must be completed in order
- Estimated timeline impact

### 💡 Suggestions
Actionable recommendations:
- Tasks ready to start (dependencies met)
- Priority suggestions based on critical path
- If a specific task was analyzed: "Impact of completing TASK-123: would unblock X tasks"
- Order recommendation: optimal sequence to minimize blocked time

### ⚠️ Alerts
- Circular dependencies if found
- High-risk bottlenecks (single task blocking many)
- Status inconsistencies

## When to Use

- **Analyze project structure**: "analise as dependências do projeto SOF"
- **Find blockers**: "quais tarefas estão bloqueadas?"
- **Impact analysis**: "qual é o impacto de concluir SOF-123?"
- **Unblock teams**: "o que devemos fazer para desbloquear o time?"
- **Sprint planning**: "qual é o caminho crítico para o MVP?"
- **Suggest updates**: "sugira atualizações de status baseado nas dependências"

## Important Notes

- This skill **never modifies** tasks directly — always suggest changes
- Excludes Backlog and Refined status tasks from analysis
- Uses Linear's standard relationship types (blocks / is blocked by)
- Generated visualizations are in Markdown for easy sharing
- Focus is on **understanding relationships**, not task content
