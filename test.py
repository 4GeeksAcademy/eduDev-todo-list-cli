import contextlib
import io
import os
import tempfile
import unittest

import app


class TodoListTests(unittest.TestCase):
    def setUp(self):
        app.todos.clear()
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.original_todos_file = app.TODOS_FILE
        app.TODOS_FILE = os.path.join(
            self.temporary_directory.name, "todos.csv"
        )

    def tearDown(self):
        app.TODOS_FILE = self.original_todos_file
        app.todos.clear()
        self.temporary_directory.cleanup()

    def capture_list(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            app.print_list()
        return output.getvalue()

    def test_adds_one_and_multiple_tasks_in_order(self):
        app.add_one_task("Call supplier")
        app.add_one_task("Check inventory")
        app.add_one_task("Prepare report")

        self.assertEqual(
            app.todos,
            ["Call supplier", "Check inventory", "Prepare report"],
        )

    def test_prints_tasks_with_one_based_positions(self):
        app.todos.extend(["First task", "Second task"])

        self.assertEqual(
            self.capture_list(),
            "1. First task\n2. Second task\n",
        )

    def test_delete_removes_requested_task_and_positions_update(self):
        app.todos.extend(["First", "Second", "Third"])

        self.assertTrue(app.delete_task(2))
        self.assertEqual(app.todos, ["First", "Third"])
        self.assertEqual(self.capture_list(), "1. First\n2. Third\n")

    def test_invalid_deletions_leave_tasks_unchanged(self):
        app.todos.extend(["First", "Second"])

        for invalid_number in (0, 3, -1, "1"):
            self.assertFalse(app.delete_task(invalid_number))

        self.assertEqual(app.todos, ["First", "Second"])

    def test_csv_save_and_load_preserves_commas_and_quotes(self):
        expected = [
            "Call Smith, Jones & Co.",
            'Confirm the "priority" shipment',
        ]
        app.todos.extend(expected)

        app.save_todos()
        app.todos.clear()
        self.assertTrue(app.load_todos())

        self.assertEqual(app.todos, expected)

    def test_load_replaces_current_tasks_instead_of_duplicating(self):
        app.todos.extend(["Saved first", "Saved second"])
        app.save_todos()
        app.todos.append("Unsaved task")

        app.load_todos()
        app.load_todos()

        self.assertEqual(app.todos, ["Saved first", "Saved second"])

    def test_missing_file_produces_an_empty_usable_list(self):
        app.todos.append("Old task")

        self.assertFalse(app.load_todos())
        self.assertEqual(app.todos, [])

        app.add_one_task("New task")
        self.assertEqual(app.todos, ["New task"])


if __name__ == "__main__":
    unittest.main()
