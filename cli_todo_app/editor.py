import click
from click.exceptions import UsageError
from functools import wraps
from cli_todo_app.tasks import Tasks
from cli_todo_app.response import Response

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
    response_data = Tasks().add_items(names)
    response = Response(response_data)
    response.show()

@click.command()
@click.argument("names", nargs=-1)
@validate_names_presence
def remove(names):
    """ Removes existing tasks from the list """
    response_data = Tasks().remove_items(names)
    response = Response(response_data)
    response.show()

@click.command()
@click.argument("names", nargs=-1)
@validate_names_presence
def done(names):
    """ Sets task's status as complete """
    response_data = Tasks().mark_items_done(names)
    response = Response(response_data)
    response.show()

@click.command()
@click.argument("names", nargs=-1)
@validate_names_presence
def undone(names):
    """ Sets task's status as not complete """
    response_data = Tasks().mark_items_not_done(names)
    response = Response(response_data)
    response.show()