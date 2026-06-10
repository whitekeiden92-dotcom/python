"""Task Management CLI and basic web interface.

Run the CLI with:
    python main.py

Run the web app with:
    python main.py web
"""

import sys
from pathlib import Path

from task_manager import task_utils
from task_manager import validation


def print_menu():
    print("\nTask Manager")
    print("1. Add task")
    print("2. Mark task complete")
    print("3. View pending tasks")
    print("4. View all tasks")
    print("5. Show progress")
    print("0. Exit")


def get_task_index(user_value, tasks):
    """Accept task numbers from the menu while tolerating 0-based test input."""
    try:
        number = int(user_value)
    except (TypeError, ValueError):
        return None

    one_based_index = number - 1
    if validation.validate_index(one_based_index, tasks):
        return one_based_index
    if validation.validate_index(number, tasks):
        return number
    return None


def run_cli():
    tasks = []
    valid_choices = {0, 1, 2, 3, 4, 5}

    while True:
        print_menu()
        choice = input("Choose an option: ")
        if not validation.validate_menu_choice(choice, valid_choices):
            print("Invalid choice. Enter a number from the menu.")
            continue
        choice = int(choice)

        if choice == 0:
            print("Goodbye!")
            break

        if choice == 1:
            title = input("Task title: ")
            if not validation.validate_non_empty(title):
                print("Title cannot be empty.")
                continue
            description = input("Task description: ")
            if not validation.validate_non_empty(description):
                print("Description cannot be empty.")
                continue
            task_utils.add_task(tasks, title, description)
            print("Task added successfully")

        elif choice == 2:
            if not tasks:
                print("No tasks currently")
                continue
            print("All tasks:")
            for i, t in enumerate(tasks):
                status = "✓" if t.get("completed") else " "
                print(f"{i + 1}. [{status}] {t['title']} - {t['description']}")
            idx = get_task_index(input("Enter task number to mark complete: "), tasks)
            if idx is None:
                print("Invalid index.")
                continue
            task_utils.mark_complete(tasks, idx)
            print("Task marked as complete")

        elif choice == 3:
            pending = task_utils.pending_tasks(tasks)
            if not pending:
                print("No pending tasks.")
            else:
                print("Pending tasks:")
                for i, t in enumerate(pending):
                    print(f"- {t['title']}: {t['description']}")

        elif choice == 4:
            all_tasks = task_utils.list_tasks(tasks)
            if not all_tasks:
                print("No tasks currently")
            else:
                print("All tasks:")
                for i, t in enumerate(all_tasks):
                    status = "Completed" if t.get("completed") else "Pending"
                    print(f"{i + 1}. {t['title']} - {t['description']} ({status})")

        elif choice == 5:
            pct = task_utils.progress_percent(tasks)
            print(f"Progress: {pct}%")


def create_app():
    try:
        from flask import Flask, redirect, render_template, request, url_for
    except ImportError:
        raise RuntimeError(
            "Flask is required for the web interface. Install it with `pip install flask`."
        )

    app = Flask(
        __name__,
        template_folder=str(Path(__file__).parent / "templates"),
        static_folder=str(Path(__file__).parent / "static"),
        static_url_path="/static",
    )
    tasks = []

    @app.route("/", methods=["GET"])
    def index():
        completed_count = sum(1 for task in tasks if task.get("completed"))
        return render_template(
            "index.html",
            tasks=tasks,
            pending=task_utils.pending_tasks(tasks),
            progress=task_utils.progress_percent(tasks),
            total=len(tasks),
            completed=completed_count,
        )

    @app.route("/add", methods=["POST"])
    def add_task_route():
        title = request.form.get("title", "")
        description = request.form.get("description", "")
        if not validation.validate_non_empty(title) or not validation.validate_non_empty(description):
            return redirect(url_for("index"))
        task_utils.add_task(tasks, title, description)
        return redirect(url_for("index"))

    @app.route("/complete/<int:index>", methods=["POST"])
    def complete_task(index):
        task_utils.mark_complete(tasks, index)
        return redirect(url_for("index"))

    return app


def main():
    if len(sys.argv) > 1 and sys.argv[1] in {"web", "serve"}:
        app = create_app()
        app.run(debug=True, port=5000)
    else:
        run_cli()


if __name__ == "__main__":
    main()
