from task_cli.database import Database
import time


class TodoList:

    def __init__(self, db_name="todo.db") -> None:
        self.db = Database(db_name)

    def add_todo(self, title):
        return self.db.add_todo(title=title.title())

    def remove_todo(self, id):
        todo = self.db.get_todo(id)
        if todo is None:
            return None
        else:
            self.db.remove_todo(int(id))
            return True

    def get_todo(self, id):
        todo = self.db.get_todo(int(id))
        return todo

    def update_todo(self, id, title, is_completed=False):
        todo = self.db.get_todo(id)
        if todo is None:
            return None
        else:
            self.db.update_todo(id=id, title=title, is_completed=is_completed)
            return todo

    def list_todos(self):
        todos = self.db.get_all_tasks()
        return todos

    def mark_complete(self, id):
        todo = self.db.get_todo(int(id))
        if todo is None:
            return None
        else:
            self.db.mark_complete(int(id))
            updated_todo = self.db.get_todo(int(id))
            return updated_todo


class TodoItem:
    todo_counter = int(time.time() * 1000)

    def __init__(self, title, is_completed=False) -> None:
        self.id = TodoItem.todo_counter
        self.title = title
        self.is_completed = is_completed

    def mark_complete(self):
        self.is_completed = True

    def mark_incomplete(self):
        self.is_completed = True

    def __str__(self) -> str:
        status = "Completed" if self.is_completed else "Pending"
        return f"{self.title} --- {status}"
