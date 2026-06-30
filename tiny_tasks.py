#!/usr/bin/env python3
"""A tiny JSON-backed command-line task tracker."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


DEFAULT_DATA_FILE = Path(".tiny_tasks.json")


@dataclass
class Task:
    id: int
    text: str
    completed: bool
    created_at: str
    completed_at: str | None = None


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_tasks(path: Path) -> list[Task]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as handle:
        raw_tasks = json.load(handle)

    return [Task(**item) for item in raw_tasks]


def save_tasks(path: Path, tasks: Iterable[Task]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(task) for task in tasks]
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def add_task(tasks: list[Task], text: str) -> Task:
    clean_text = text.strip()
    if not clean_text:
        raise ValueError("Task text cannot be empty.")

    next_id = max((task.id for task in tasks), default=0) + 1
    task = Task(
        id=next_id,
        text=clean_text,
        completed=False,
        created_at=now_iso(),
    )
    tasks.append(task)
    return task


def complete_task(tasks: list[Task], task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            if task.completed:
                raise ValueError(f"Task {task_id} is already completed.")
            task.completed = True
            task.completed_at = now_iso()
            return task

    raise ValueError(f"Task {task_id} was not found.")


def format_task(task: Task) -> str:
    marker = "x" if task.completed else " "
    return f"{task.id:>3}. [{marker}] {task.text}"


def task_summary(tasks: list[Task]) -> dict[str, int]:
    completed = sum(1 for task in tasks if task.completed)
    total = len(tasks)
    return {
        "total": total,
        "open": total - completed,
        "completed": completed,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A tiny JSON-backed task tracker.")
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_FILE,
        help="Path to the task data JSON file.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a task.")
    add_parser.add_argument("text", help="Task text.")

    list_parser = subparsers.add_parser("list", help="List tasks.")
    list_parser.add_argument(
        "--all",
        action="store_true",
        help="Include completed tasks.",
    )

    done_parser = subparsers.add_parser("done", help="Complete a task.")
    done_parser.add_argument("id", type=int, help="Task ID.")

    subparsers.add_parser("summary", help="Show task counts.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    tasks = load_tasks(args.data)

    try:
        if args.command == "add":
            task = add_task(tasks, args.text)
            save_tasks(args.data, tasks)
            print(f"Added task {task.id}: {task.text}")
            return 0

        if args.command == "list":
            visible_tasks = tasks if args.all else [task for task in tasks if not task.completed]
            if not visible_tasks:
                print("No tasks.")
                return 0
            for task in visible_tasks:
                print(format_task(task))
            return 0

        if args.command == "done":
            task = complete_task(tasks, args.id)
            save_tasks(args.data, tasks)
            print(f"Completed task {task.id}: {task.text}")
            return 0

        if args.command == "summary":
            summary = task_summary(tasks)
            print(
                f"Total: {summary['total']} | "
                f"Open: {summary['open']} | "
                f"Completed: {summary['completed']}"
            )
            return 0

    except ValueError as error:
        parser.exit(status=2, message=f"error: {error}\n")

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
