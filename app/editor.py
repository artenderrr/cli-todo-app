import click
from app.tasks import Tasks

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