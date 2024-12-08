import click
from cli_todo_app.tasks import Tasks
from cli_todo_app.editor import add, remove, done, undone

def show_tasks():
    """ Shows a list of tasks sorted by completion status """
    tasks = sorted(Tasks().items, key=lambda task: task["done"])
    if tasks:
        for task in tasks:
            click.echo(f"[{"x" if task["done"] else " "}] {task["name"]}")
    else:
        click.echo("You have no todos yet.")

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """ Entry point of application """
    if not ctx.invoked_subcommand:
        show_tasks()

cli.add_command(add)
cli.add_command(remove)
cli.add_command(done)
cli.add_command(undone)