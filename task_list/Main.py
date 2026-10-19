import ToDoTask

def run_program():
    task_list = ToDoTask.TaskList()
    print("Commands: (q)uit; (d)isplay; (n)ext; (a)dd; (c)omplete; (u)ndo; (t)otals")

    while True:
        user_input = input()
        if user_input == "q":
            break

        if user_input == "":
            print("Commands: (q)uit; (d)isplay; (n)ext; (a)dd; (c)omplete; (u)ndo; (t)otals")
            continue

        if user_input == "d":
            print(task_list)
            continue

        if user_input == "n":
            try:
                next = task_list.next()
                print(f"Next: ({next[0]}) {next[1]}")
            except:
                print("No pending tasks")
            continue

        parts = user_input.strip().split(maxsplit=2)
        if not parts:
            return
        command = parts[0]

        if command == "a":
            if len(parts) < 3:
                print("Error: Missing priority or name")
                continue

            try:
                priority = int(parts[1])
                name = parts[2]

                task_list.add(priority, name)
                print(f"Added ({priority}) {name}")
            except ValueError as e:
                print(f"Error: {e}")
            continue

        parts = user_input.strip().split(maxsplit=1)
        if not parts:
            continue
        command = parts[0]

        if command == "c":
            try:
                completed = task_list.complete(parts[1])
                print(f"Completed ({completed[0]}) {completed[1]}")
            except IndexError as e:
                completed = task_list.complete()
                print(f"Completed ({completed[0]}) {completed[1]}")
            except ValueError as e:
                print(f"Error: {e}")
            continue

        if command == "u":
            try:
                undid = task_list.undo()
                print(f"Restored ({undid[0]}) {undid[1]})")

            except ValueError as e:
                print(f"Error: {e}")
            continue

        if user_input == "t":
            print(f"{task_list.remaining()} pending; {task_list.completed()} completed")
            continue