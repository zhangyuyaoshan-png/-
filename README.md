# Tiny Tasks

Tiny Tasks is a small command-line task tracker written with the Python standard
library. It is intentionally simple: add tasks, list tasks, complete tasks, and
see a short summary.

## Quick Start

```bash
python3 tiny_tasks.py add "Write project notes"
python3 tiny_tasks.py list
python3 tiny_tasks.py done 1
python3 tiny_tasks.py summary
```

By default, tasks are stored in `.tiny_tasks.json` in the current directory.
Use `--data PATH` to choose another file:

```bash
python3 tiny_tasks.py --data /tmp/tasks.json add "Try Codex"
```

## Commands

- `add TEXT`: add a new task
- `list`: show open tasks by default
- `list --all`: show open and completed tasks
- `done ID`: mark a task as completed
- `summary`: show total, open, and completed task counts

## Tests

```bash
python3 -m unittest discover -s tests
```
