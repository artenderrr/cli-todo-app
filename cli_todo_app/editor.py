import click
from click.exceptions import UsageError
from functools import wraps
from cli_todo_app.tasks import Tasks

def validate_names_presence(func):
    @wraps(func)
    def wrapper(names):
        if not names:
            raise UsageError("Missing argument 'NAMES'.")
        func(names)
    return wrapper

@click.command()
@click.argument("names", nargs=-1)
@validate_names_presence
def add(names):
    """ Add new tasks to the list """
    response = Tasks().add_items(names)
    response.show()

@click.command()
@click.argument("names", nargs=-1)
@validate_names_presence
def remove(names):
    """ Removes existing tasks from the list """
    response = Tasks().remove_items(names)
    response.show()

@click.command()
@click.argument("names", nargs=-1)
@validate_names_presence
def done(names):
    """ Sets task's status as complete """
    for name in names:
        status = Tasks().mark_item_done(name)
        if status == "marked as done":
            click.echo(f"Done task with name \"{name}\"")
        elif status == "already marked as done":
            click.echo(f"Task with name \"{name}\" is already done")
        elif status == "task doesn't exist":
            click.echo(f"Task with name \"{name}\" doesn't exist")

@click.command()
@click.argument("names", nargs=-1)
@validate_names_presence
def undone(names):
    """ Sets task's status as not complete """
    for name in names:
        status = Tasks().mark_item_not_done(name)
        if status == "marked as not done":
            click.echo(f"Undone task with name \"{name}\"")
        elif status == "already marked as not done":
            click.echo(f"Task with name \"{name}\" is not done yet")
        elif status == "task doesn't exist":
            click.echo(f"Task with name \"{name}\" doesn't exist")