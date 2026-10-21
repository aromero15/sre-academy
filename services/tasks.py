class TaskService:
    def __init__(self):
        self._tasks = {}

    def create(self, title):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title required")
        task_id = len(self._tasks) + 1
        task = {"id": task_id, "title": title.strip()}
        self._tasks[task_id] = task
        return task

    def get(self, task_id):
        return self._tasks.get(task_id)
