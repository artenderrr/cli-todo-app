import click
from cli_todo_app.tasks import Tasks

@click.command()
@click.argument("name")
def add(name):
    """ Add new task to the list """
    success = Tasks().add_item(name)
    if success:
        click.echo(f"Added new task with name \"{name}\"")
    else:
        click.echo(f"Task with name \"{name}\" already exists")

@click.command()
@click.argument("name")
def remove(name):
    """ Removes existing task from the list """
    success = Tasks().remove_item(name)
    if success:
        click.echo(f"Removed task with name \"{name}\"")
    else:
        click.echo(f"Task with name \"{name}\" doesn't exist")

@click.command()
@click.argument("name")
def done(name):
    """ Sets task's status as complete """
    status = Tasks().mark_item_done(name)
    if status == "marked as done":
        click.echo(f"Done task with name \"{name}\"")
    elif status == "already marked as done":
        click.echo(f"Task with name \"{name}\" is already done")
    elif status == "task doesn't exist":
        click.echo(f"Task with name \"{name}\" doesn't exist")

@click.command()
@click.argument("name")
def undone(name):
    """ Sets task's status as not complete """
    status = Tasks().mark_item_not_done(name)
    if status == "marked as not done":
        click.echo(f"Undone task with name \"{name}\"")
    elif status == "already marked as not done":
        click.echo(f"Task with name \"{name}\" is not done yet")
    elif status == "task doesn't exist":
        click.echo(f"Task with name \"{name}\" doesn't exist")