import sqlite3


class Database:

    def __init__(self, db_name="todo.db") -> None:
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                is_completed BOOLEAN NOT NULL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        self.cursor.execute(create_table_sql)
        self.connection.commit()

    def add_todo(self, title, is_completed=False):
        add_todo_sql = """
            INSERT INTO tasks (title, is_completed) VALUES (?, ?)
        """
        self.cursor.execute(add_todo_sql, (title, is_completed))
        self.connection.commit()
        return self.cursor.lastrowid

    def update_todo(self, id, title, is_completed):
        update_todo_sql = """
            UPDATE tasks SET title = ?, is_completed = ? WHERE id = ?
        """
        self.cursor.execute(update_todo_sql, (title, is_completed, id))
        self.connection.commit()

    def mark_complete(self, id):
        update_todo_sql = """
            UPDATE tasks SET  is_completed = ? WHERE id = ?
        """
        self.cursor.execute(update_todo_sql, (True, id))
        self.connection.commit()

    def remove_todo(self, id):
        delete_task_sql = "DELETE FROM tasks WHERE id = ?;"
        self.cursor.execute(delete_task_sql, (id,))
        self.connection.commit()

    def get_todo(self, id):
        get_todo_sql = """
            SELECT id, title, is_completed, created_at, updated_at
            FROM tasks 
            WHERE id = ?
        """
        self.cursor.execute(
            get_todo_sql,
            (id,),
        )
        return self.cursor.fetchone()

    def get_all_tasks(self, status):
        if status is None:
            select_all_tasks_sql = "SELECT * FROM tasks ORDER BY updated_at DESC;"
        elif status.lower() == "completed":
            select_all_tasks_sql = (
                "SELECT * FROM tasks WHERE is_completed = 1 ORDER BY updated_at DESC;"
            )
        elif status.lower() == "pending":
            select_all_tasks_sql = (
                "SELECT * FROM tasks WHERE is_completed = 0 ORDER BY updated_at DESC;"
            )
        self.cursor.execute(select_all_tasks_sql)
        return self.cursor.fetchall()

    def __del__(self):
        self.connection.close()
