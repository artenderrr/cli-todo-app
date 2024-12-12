import click

class Response:
    def __init__(self, data, context=None):
        self.blocks = {group: ResponseBlock(group, tasks) for group, tasks in data.items() if tasks}
        self.context = context

    def is_empty(self):
        return len(self.blocks) == 0

    @staticmethod
    def handle_edge_cases(func):
        def wrapper(self):
            if self.context in ("remove_all_tasks", "done_all_tasks") and self.is_empty():
                click.echo("You don't have any tasks yet.")
            elif self.context == "remove_done_tasks" and self.is_empty():
                click.echo("You haven't done any tasks yet.")
            elif (self.context == "done_all_tasks"
                and
                not self.blocks.get("done", None) and self.blocks.get("already done", None)
                ):
                click.echo("All tasks are already done.")
            else:
                func(self)
        return wrapper
    
    @handle_edge_cases
    def show(self):
        for block in self.blocks.values():
            block.show()

class ResponseBlock:
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks
        self.HEADERS = {
            "added": ("Added this task", "Added these tasks"),
            "removed": ("Removed this task", "Removed these tasks"),
            "done": ("Done this task", "Done these tasks"),
            "undone": ("Undone this task", "Undone these tasks"),
            "already exist": ("This task already exists", "These tasks already exist"),
            "don't exist": ("This task doesn't exist", "These tasks don't exist"),
            "already done": ("This task is already done", "These tasks are already done"),
            "already undone": ("This task is not done yet", "These tasks are not done yet")
        }
        self.COLORS = {
            "green": ("added", "removed", "done", "undone"),
            "yellow": ("already done", "already undone"),
            "red": ("already exist", "don't exist")
        }
    
    def show(self):
        if self.tasks:
            click.echo(f"{self.header}:")
            self.show_tasks()

    def show_tasks(self):
        for task in sorted(self.tasks):
            click.secho(" " * 4 + task, fg=self.color)

    @property
    def header(self):
        return self.HEADERS[self.name][len(self.tasks) > 1]
    
    @property
    def color(self):
        for color, group in self.COLORS.items():
            if self.name in group:
                return color