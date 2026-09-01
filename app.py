import csv


todos = []
TODOS_FILE = "todos.csv"


def add_one_task(title):
    todos.append(title)


def print_list():
    if not todos:
        print("No pending tasks.")
        return

    for position, title in enumerate(todos, start=1):
        print(f"{position}. {title}")


def delete_task(number_to_delete):
    if not isinstance(number_to_delete, int):
        return False
    if number_to_delete < 1 or number_to_delete > len(todos):
        return False

    todos.pop(number_to_delete - 1)
    return True


def save_todos():
    with open(TODOS_FILE, "w", newline="", encoding="utf-8") as todo_file:
        writer = csv.writer(todo_file)
        for title in todos:
            writer.writerow([title])


def load_todos():
    try:
        with open(TODOS_FILE, "r", newline="", encoding="utf-8") as todo_file:
            loaded_todos = [row[0] for row in csv.reader(todo_file) if row]
    except FileNotFoundError:
        todos.clear()
        return False

    todos[:] = loaded_todos
    return True


def show_menu():
    print("\nTodo List")
    print("1. Add task")
    print("2. List tasks")
    print("3. Delete task")
    print("4. Save tasks")
    print("5. Load tasks")
    print("6. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Task title: ").strip()
            if title:
                add_one_task(title)
                print("Task added.")
            else:
                print("Task title cannot be empty.")
        elif choice == "2":
            print_list()
        elif choice == "3":
            print_list()
            if not todos:
                continue
            try:
                number = int(input("Task number to delete: ").strip())
            except ValueError:
                print("Enter a valid task number.")
                continue
            if delete_task(number):
                print("Task deleted.")
            else:
                print("Task number does not exist.")
        elif choice == "4":
            save_todos()
            print("Tasks saved.")
        elif choice == "5":
            if load_todos():
                print("Tasks loaded.")
            else:
                print("No saved task file was found. Starting with an empty list.")
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Choose a valid menu option.")


if __name__ == "__main__":
    main()
