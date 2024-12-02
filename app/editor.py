import click
from app.tasks import Tasks

@click.command()
@click.argument("name")
def add(name):
    """ Add new task to the list """
    Tasks().add_item(name)
    click.echo(f"Added new task: {name}")