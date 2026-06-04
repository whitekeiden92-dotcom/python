"""Simple Task Management CLI.

Usage: run `python main.py` and follow the menu prompts.
"""

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


def main():
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
            print("Task added.")

        elif choice == 2:
            if not tasks:
                print("No tasks to mark.")
                continue
            print("All tasks:")
            for i, t in enumerate(tasks):
                status = "✓" if t.get("completed") else " "
                print(f"{i}. [{status}] {t['title']} - {t['description']}")
            idx = input("Enter task index to mark complete: ")
            if not validation.validate_index(idx, tasks):
                print("Invalid index.")
                continue
            idx = int(idx)
            task_utils.mark_complete(tasks, idx)
            print("Task marked complete.")

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
                print("No tasks yet.")
            else:
                print("All tasks:")
                for i, t in enumerate(all_tasks):
                    status = "Completed" if t.get("completed") else "Pending"
                    print(f"{i}. {t['title']} - {t['description']} ({status})")

        elif choice == 5:
            pct = task_utils.progress_percent(tasks)
            print(f"Progress: {pct}%")


if __name__ == "__main__":
    main()
