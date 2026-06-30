import tempfile
import unittest
from pathlib import Path

from tiny_tasks import add_task, complete_task, load_tasks, save_tasks, task_summary


class TinyTasksTest(unittest.TestCase):
    def test_add_task_assigns_incrementing_ids(self):
        tasks = []

        first = add_task(tasks, "Write notes")
        second = add_task(tasks, "Review changes")

        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)
        self.assertEqual([task.text for task in tasks], ["Write notes", "Review changes"])

    def test_add_task_rejects_empty_text(self):
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            add_task([], "   ")

    def test_complete_task_marks_matching_task(self):
        tasks = []
        task = add_task(tasks, "Ship the first version")

        completed = complete_task(tasks, task.id)

        self.assertTrue(completed.completed)
        self.assertIsNotNone(completed.completed_at)

    def test_complete_task_rejects_missing_id(self):
        with self.assertRaisesRegex(ValueError, "was not found"):
            complete_task([], 99)

    def test_complete_task_rejects_already_completed_task(self):
        tasks = []
        task = add_task(tasks, "One-and-done")
        complete_task(tasks, task.id)

        with self.assertRaisesRegex(ValueError, "already completed"):
            complete_task(tasks, task.id)

    def test_save_and_load_tasks_round_trip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "tasks.json"
            tasks = []
            add_task(tasks, "Persist me")

            save_tasks(path, tasks)
            loaded_tasks = load_tasks(path)

        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0].text, "Persist me")

    def test_task_summary_counts_open_and_completed_tasks(self):
        tasks = []
        first = add_task(tasks, "Open task")
        add_task(tasks, "Completed task")
        complete_task(tasks, first.id)

        self.assertEqual(task_summary(tasks), {"total": 2, "open": 1, "completed": 1})


if __name__ == "__main__":
    unittest.main()
