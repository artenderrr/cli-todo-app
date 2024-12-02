import json
from json.decoder import JSONDecodeError
import click

class Tasks:
    def __init__(self):
        self.file_path = "data/todos.json"
        self.items = self.load_items()

    def load_items(self):
        """ Loads tasks from file and returns them as a list of dictionaries """
        try:
            with open(self.file_path, encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, JSONDecodeError):
            return []

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """ Entry point of application """
    if not ctx.invoked_subcommand:
        tasks = sorted(Tasks().items, key=lambda task: task["done"])
        if tasks:
            for task in tasks:
                click.echo(f"[{"x" if task["done"] else " "}] {task["name"]}")
        else:
            click.echo("You have no todos yet.")