import click

class Response:
    def __init__(self, data):
        self.blocks = [ResponseBlock(group, tasks) for group, tasks in data.items()]

    def show(self):
        for block in self.blocks:
            block.show()

class ResponseBlock:
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks
    
    def show(self):
        if self.tasks:
            click.echo(f"{self.header}:")
            self.show_tasks()

    def show_tasks(self):
        for task in sorted(self.tasks):
            click.secho(" " * 4 + task, fg=self.color)

    @property
    def header(self):
        if self.name == "added":
            header = "Added these tasks" if len(self.tasks) > 1 else "Added this task"
        elif self.name == "already_exist":
            header = "These tasks already exist" if len(self.tasks) > 1 else "This task already exists"
        elif self.name == "removed":
            header = "Removed these tasks" if len(self.tasks) > 1 else "Removed this task"
        elif self.name == "don't exist":
            header = "These tasks don't exist" if len(self.tasks) > 1 else "This task doesn't exist"
        return header
    
    @property
    def color(self):
        if self.name in ("added", "removed"):
            color = "green"
        elif self.name in ("already_exist", "don't exist"):
            color = "red"
        return color