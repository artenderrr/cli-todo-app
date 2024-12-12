import click
from click.exceptions import UsageError
from functools import wraps
from cli_todo_app.tasks import Tasks
from cli_todo_app.response import Response

def validate_parameters(func):
    @wraps(func)
    def wrapper(**kwargs):
        specified = len([*filter(None, kwargs.values())])
        if len(kwargs) == 1 and not kwargs["names"]:
            raise UsageError("Missing argument 'NAMES'")
        elif len(kwargs) > 1 and not specified:
            raise UsageError("Missing parameters")
        elif len(kwargs) > 1 and specified > 1:
            raise UsageError("Too many parameters")
        func(**kwargs)
    return wrapper

def get_context(command, parameters):
    specified_parameter = next(parameter for parameter, value in parameters.items() if value)
    context = f"{command}_{specified_parameter}"
    return context

@click.command()
@click.argument("names", nargs=-1)
@validate_parameters
def add(names):
    """ Add new tasks to the list """
    response_data = Tasks().add_items(names)
    response = Response(response_data)
    response.show()

@click.command()
@click.argument("names", nargs=-1)
@click.option("-a", "--all", "all_tasks", is_flag=True, default=False)
@click.option("-d", "--done", "done_tasks", is_flag=True, default=False)
@validate_parameters
def remove(names, all_tasks, done_tasks):
    """ Removes existing tasks from the list """
    context = get_context("remove", locals())
    if all_tasks:
        response_data = Tasks().remove_all_items()
    elif done_tasks:
        response_data = Tasks().remove_done_items()
    elif names:
        response_data = Tasks().remove_items(names)
    response = Response(response_data, context)
    response.show()

@click.command()
@click.argument("names", nargs=-1)
@click.option("-a", "--all", "all_tasks", is_flag=True, default=False)
@validate_parameters
def done(names, all_tasks):
    """ Sets task's status as complete """
    context = get_context("done", locals())
    if all_tasks:
        response_data = Tasks().mark_all_items_done()
    elif names:
        response_data = Tasks().mark_items_done(names)
    response = Response(response_data, context)
    response.show()

@click.command()
@click.argument("names", nargs=-1)
@click.option("-a", "--all", "all_tasks", is_flag=True, default=False)
@validate_parameters
def undone(names, all_tasks):
    """ Sets task's status as not complete """
    context = get_context("undone", locals())
    if all_tasks:
        response_data = Tasks().mark_all_items_not_done()
    elif names:
        response_data = Tasks().mark_items_not_done(names)
    response = Response(response_data, context)
    response.show()