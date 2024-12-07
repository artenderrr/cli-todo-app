import click
from click.exceptions import UsageError
from cli_todo_app.tasks import Tasks

@click.command()
@click.argument("names", nargs=-1)
def add(names):
    """ Add new tasks to the list """
    if not names:
        raise UsageError("Missing argument 'NAMES'.")
    for name in names:
        success = Tasks().add_item(name)
        if success:
            click.echo(f"Added new task with name \"{name}\"")
        else:
            click.echo(f"Task with name \"{name}\" already exists")

@click.command()
@click.argument("names", nargs=-1)
def remove(names):
    """ Removes existing tasks from the list """
    if not names:
        raise UsageError("Missing argument 'NAMES'.")
    for name in names:
        success = Tasks().remove_item(name)
        if success:
            click.echo(f"Removed task with name \"{name}\"")
        else:
            click.echo(f"Task with name \"{name}\" doesn't exist")

@click.command()
@click.argument("names", nargs=-1)
def done(names):
    """ Sets task's status as complete """
    if not names:
        raise UsageError("Missing argument 'NAMES'.")
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
def undone(names):
    """ Sets task's status as not complete """
    if not names:
        raise UsageError("Missing argument 'NAMES'.")
    for name in names:
        status = Tasks().mark_item_not_done(name)
        if status == "marked as not done":
            click.echo(f"Undone task with name \"{name}\"")
        elif status == "already marked as not done":
            click.echo(f"Task with name \"{name}\" is not done yet")
        elif status == "task doesn't exist":
            click.echo(f"Task with name \"{name}\" doesn't exist")