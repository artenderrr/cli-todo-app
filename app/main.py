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
                loaded_items = json.load(f)
                valid_items = self.get_valid_items(loaded_items)
                return valid_items
        except (FileNotFoundError, JSONDecodeError):
            return []
    
    @staticmethod
    def get_valid_items(items):
        """ Filters loaded items to get only valid ones """
        # loaded items should be represented as a list
        if not isinstance(items, list):
            return []
        return [*filter(Tasks.validate_item, items)]

    @staticmethod
    def validate_item(item):
        """ Validates single given item from loaded ones """
        # item should be dictionary
        if not isinstance(item, dict):
            return False
        # item should contain only two key-value pairs
        if not len(item.items()) == 2:
            return False
        # item should contain "name" and "done" keys
        if "name" not in item or "done" not in item:
            return False
        # value of "name" should be string
        if not isinstance(item["name"], str):
            return False
        # value of "done" should be boolean
        if not isinstance(item["done"], bool):
            return False
        return True

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