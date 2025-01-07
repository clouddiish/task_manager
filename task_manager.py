import json


def validate_input(input):
    """
    Validates whether the input is a non-empty string.

    Args:
        input (any): The input to validate.

    Returns:
        bool: True if the input is a non-empty string, False otherwise.
    """
    if type(input) == str and bool(input.strip()):
        return True
    else:
        return False


def load_tasks(file_path):
    """
    Loads tasks from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing tasks.

    Returns:
        dict: A dictionary with task names as keys and their completion status as values.
    """
    with open(file_path, "r") as f:
        tasks = json.load(f)

    tasks = {task.lower(): tasks[task] for task in tasks}

    return tasks


def dump_tasks(file_path, tasks):
    """
    Writes tasks to a JSON file.

    Args:
        file_path (str): The path to the JSON file.
        tasks (dict): A dictionary with task names as keys and their completion status as values.
    """
    with open(file_path, "w") as f:
        json.dump(tasks, f, indent=2)


def list_tasks(tasks):
    """
    Prints all tasks with their completion status.

    Args:
        tasks (dict): A dictionary with task names as keys and their completion status as values.
    """
    if len(tasks) == 0:
        print("No tasks added.")
        return

    for task in tasks:
        if tasks[task]:
            print("-", task, "✅")
        else:
            print("-", task, "❌")


def add_task(file_path, tasks, name):
    """
    Adds a new task to the tasks list.

    Args:
        file_path (str): The path to the JSON file.
        tasks (dict): A dictionary with task names as keys and their completion status as values.
        name (str): The name of the new task.

    Raises:
        ValueError: If the task already exists or if the input is invalid.
    """
    name = name.lower()

    if validate_input(name) and (name.lower() not in tasks):
        tasks.update({name: False})
    else:
        print("Task already exists.")
        return

    dump_tasks(file_path, tasks)

    print("Task was added.")


def remove_task(file_path, tasks, name):
    """
    Removes a task from the tasks list.

    Args:
        file_path (str): The path to the JSON file.
        tasks (dict): A dictionary with task names as keys and their completion status as values.
        name (str): The name of the task to remove.

    Raises:
        TypeError: If the input is invalid.
        ValueError: If the task does not exist.
    """
    if not validate_input(name):
        raise TypeError

    prev_length = len(tasks)
    name = name.lower()

    if name in tasks:
        del tasks[name]

    new_length = len(tasks)

    if prev_length == new_length:
        raise ValueError

    dump_tasks(file_path, tasks)

    print("Task removed.")


def change_complete(file_path, tasks, name):
    """
    Toggles the completion status of a task.

    Args:
        file_path (str): The path to the JSON file.
        tasks (dict): A dictionary with task names as keys and their completion status as values.
        name (str): The name of the task to toggle.

    Raises:
        TypeError: If the input is invalid.
        ValueError: If the task does not exist.
    """
    if not validate_input(name):
        raise TypeError

    found = False
    completed = False
    name = name.lower()

    if name in tasks:
        found = True
        tasks[name] = not tasks[name]
        if tasks[name]:
            completed = True

    if not found:
        raise ValueError

    dump_tasks(file_path, tasks)

    if completed:
        print("Task changed to completed.")
    else:
        print("Task changed to uncompleted.")


def run(file_path):
    """
    Runs the main task management loop.

    Args:
        file_path (str): The path to the JSON file.
    """
    try:
        while True:
            tasks = load_tasks(file_path)

            action = input(
                """
                What do you want to do?
                    l - list tasks
                    c - change status of a task
                    a - add task
                    r - remove task
                    e - end program
                """
            ).lower()

            match action:
                case "l":
                    print("CURRENT TASKS:")
                    list_tasks(tasks)
                case "c":
                    task_name = input("Name of the task to change the status of: ")
                    change_complete(file_path, tasks, task_name)
                case "a":
                    task_name = input("Name of a new task: ")
                    add_task(file_path, tasks, task_name)
                case "r":
                    task_name = input("Name of the task to remove: ")
                    sure = input("Are you sure? (y/n) ")
                    if sure.lower() == "y":
                        remove_task(file_path, tasks, task_name)
                    else:
                        continue
                case "e":
                    end = input("Are you sure? (y/n) ")
                    if end.lower() == "y":
                        break
                    else:
                        continue
                case _:
                    print("Wrong letter provided.")

    except FileNotFoundError:
        dump_tasks(file_path, {})
        print("New tasks file was created. Try again.")
        run(file_path)

    except json.JSONDecodeError:
        dump_tasks(file_path, {})
        print(
            "There was something wrong with the tasks file. Tasks were reset. Try again."
        )
        run(file_path)

    except TypeError:
        print("Task name must be a unique, non-empty string.")
        run(file_path)

    except ValueError:
        print("Task not in tasks list.")
        run(file_path)

    except Exception as e:
        print("Something went wrong. Try again.")
        print("Error code:", str(e))
        run(file_path)


run("tasks.json")
