class TaskList:
    """"Builds a task list, each task has priority and name.
    Tasks are stored in their priority order, the most important first"""
    def __init__(self) -> None:
        self._pending = []
        self._completed = []

    def __str__(self) -> str:
        to_return = "TaskList:"

        if len(self._pending) == 0:
            return to_return + " empty"
        items = []
        for pending_task in self._pending[:4]:
            items.append(f"({pending_task[0]}) {pending_task[1]}")

        to_return = to_return + " " + ", ".join(items)

        if  len(items) >= 4:
            to_return += ", ..."

        return to_return

    def __repr__(self) -> str:
        return f"TaskList({self._pending}, {self._completed})"

    def add(self, priority: int, name: str) -> None:
        #Adds a task to the pending list
        if priority < 1:
            raise ValueError("Priority must be greater than 0")
        if not name:
            raise ValueError("Task name cannot be empty")
        if ";" in name or "|" in name:
            raise ValueError("Task name cannot contain ';' or '|'")

        all_tasks = self._pending + self._completed
        if any(existing_name == name for _, existing_name in all_tasks):
            raise ValueError("Task with this name already exists")

        new_task = (priority, name)

        self._pending.append(new_task)
        self._pending.sort()

    def complete(self, name: str = None) -> tuple:
        #Moves a task from pending to completed list
        if not self._pending:
            raise ValueError("No tasks pending")

        if name is None:
            task = self._pending.pop(0)
        else:
            task = None
            for pending_task in self._pending:
                if pending_task[1].lower() == name.lower():
                    task = pending_task
                    break

            if task is None:
                raise ValueError(f"No pending task with name '{name}'")

            self._pending.remove(task)

        self._completed.append(task)
        return task


    def pending(self) -> list:
        #Returns a list of pending tasks
        lst = []
        for priority, name in self._pending:
            lst.append(name)
        return lst

    def undo(self) -> tuple:
        #Cancels the lastly done task
       if not self._completed:
           raise ValueError("No completed tasks")

       task = self._completed.pop()
       self._pending.append(task)
       self._pending.sort()

       return task

    def next(self) -> tuple:
        #Returns the next most important task
        try:
            return self._pending[0]
        except:
            raise ValueError("No pending tasks")

    def remaining(self) -> int:
        #Returns remaining tasks in pending list
        return len(self._pending)

    def completed(self) -> int:
        #Returns completed tasks in completed list
        return len(self._completed)

    def save(self, path):
        try :
            with open(path, "w") as f:
                lst = []
                for pending_task in self._pending:
                    lst.append(f"{pending_task[0]};{pending_task[1]}")
                pending = "|".join(lst)

                lst = []
                for completed_task in self._completed:
                    lst.append(f"{completed_task[0]};{completed_task[1]}")
                completed = "|".join(lst)

                f.write(pending + "\n" + completed + "\n")
        except:
            raise ValueError()

    def load(self, path):
        lines = []
        try:
            with open(path, "r") as f:
                for line in f:
                    lines.append(line.strip())

            if len(lines) > 3:
                raise ValueError("File malformed")

            pen_list = lines[0].split("|")
            _pending = []
            for pending_task in pen_list:
                if not pending_task:
                    break
                pending_task = pending_task.strip().split(";")
                _pending.append((int(pending_task[0]), pending_task[1]))

            com = lines[1].strip()
            com_list = com.split("|")
            _completed = []
            for completed_task in com_list:
                if not completed_task:
                    break
                completed_task = completed_task.strip().split(";")
                _completed.append((int(completed_task[0]), completed_task[1]))

            self._pending = _pending
            self._completed = _completed
        except:
            raise ValueError()