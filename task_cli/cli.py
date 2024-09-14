from typing import Optional
import typer
from task_cli import __app_name__, __version__
from task_cli.todo import TodoList
from rich.console import Console
from rich.table import Table

app = typer.Typer()
todo = TodoList()
console = Console()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


def create_task_table(task, title: str):
    """Generate a Rich Table for a given task."""
    table = Table(title=title)
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Status", justify="center")
    table.add_column("Created At", justify="center")
    table.add_column("Updated At", justify="center")

    id, title, is_completed, created_at, updated_at = task
    status = "Completed" if is_completed else "Pending"
    table.add_row(str(id), title.title(), status, str(created_at), str(updated_at))

    return table


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
def add(title: str):
    """Add a new task to the todo list."""
    task = todo.add_todo(title)
    if task is not None:
        task = todo.get_todo(task)
        table = create_task_table(task, "Task Created Successfully")
        console.print(table)
    else:
        console.print("Task Not Found!", style="bold red")


@app.command()
def list():
    """List all tasks."""
    todos = todo.list_todos()
    table = Table(title="Task List")

    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Status", justify="center")
    table.add_column("Created At", justify="center")
    table.add_column("Updated At", justify="center")

    for task in todos:
        id, title, is_completed, created_at, updated_at = task
        status = "Completed" if is_completed else "Pending"
        table.add_row(str(id), title.title(), status, str(created_at), str(updated_at))

    console.print(table)


@app.command()
def remove(id: int):
    """Remove a task from the task list by ID."""
    task = todo.remove_todo(id)
    if task is not None:
        console.print("Task Removed Successfully!", style="bold yellow")
    else:
        console.print("Task Not Found!", style="bold red")


@app.command()
def get(id: int):
    """Get details of a task by ID."""
    task = todo.get_todo(id)
    if task is not None:
        table = create_task_table(task, "Task Fetched Successfully")
        console.print(table)
    else:
        console.print("Task Not Found!", style="bold red")


@app.command()
def complete(id: int):
    """Mark a task as completed."""
    task = todo.mark_complete(id)
    if task is not None:
        table = create_task_table(task, "Task Marked As Completed")
        console.print(table)
    else:
        console.print("Task Not Found!", style="bold red")


@app.command()
def update(id: int, title: str, is_completed: bool = False):
    """Update a task's title and completion status."""
    task = todo.update_todo(id, title, is_completed)
    task = todo.mark_complete(id)
    if task is not None:
        table = create_task_table(task, "Task Marked As Completed")
        console.print(table)
    else:
        console.print("Task Not Found!", style="bold red")
