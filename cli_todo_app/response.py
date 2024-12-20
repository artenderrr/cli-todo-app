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
            if self.context in ("remove_all_tasks", "done_all_tasks", "undone_all_tasks") and self.is_empty():
                click.echo("You don't have any tasks yet.")
            elif self.context == "remove_done_tasks" and self.is_empty():
                click.echo("You haven't done any tasks yet.")
            elif self.context == "done_all_tasks" and not self.blocks.get("done", None):
                click.echo("All tasks are already done.")
            elif self.context == "undone_all_tasks" and not self.blocks.get("undone", None):
                click.echo("You haven't done any tasks yet.")
            else:
                func(self)
        return wrapper
    
    def should_skip_block(self, block):
        return (
            block.name == "already done" and self.context == "done_all_tasks"
            or
            block.name == "already undone" and self.context == "undone_all_tasks"
        )
    
    @handle_edge_cases
    def show(self):
        for block in self.blocks.values():
            if self.should_skip_block(block):
                continue
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
            "already undone": ("This task is not done yet", "These tasks are not done yet"),
            "nonexistent ids": ("Task with this ID doesn't exist", "Tasks with these IDs don't exist"),
            "invalid names": ("This task name is not valid", "These task names are not valid")
        }
        self.COLORS = {
            "green": ("added", "removed", "done", "undone"),
            "yellow": ("already done", "already undone"),
            "red": ("already exist", "don't exist", "nonexistent ids", "invalid names")
        }
    
    def show(self):
        if self.tasks:
            click.echo(f"{self.header}:")
            self.show_tasks()

    def show_tasks(self):
        for task in sorted(self.tasks):
            click.secho(f"↪ {task}", fg=self.color)

    @property
    def header(self):
        return self.HEADERS[self.name][len(self.tasks) > 1]
    
    @property
    def color(self):
        for color, group in self.COLORS.items():
            if self.name in group:
                return color