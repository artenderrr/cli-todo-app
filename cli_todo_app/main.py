import click
from cli_todo_app.tasks import Tasks
from cli_todo_app.editor import add, remove, done, undone

def show_tasks():
    """ Shows a list of tasks sorted by completion status """
    tasks = sorted(Tasks().items, key=lambda task: (task["done"], task["name"]))
    longest_task_name = max((task["name"] for task in tasks), key=len, default="")
    if tasks:
        for task in tasks:
            status = "x" if task["done"] else " "
            fill = " " * (len(longest_task_name) - len(task["name"]) + 1)
            task_id = click.style(f"({task["id"]})", fg="bright_black")
            click.echo(f"[{status}] {task["name"]}" + fill + task_id)
    else:
        click.echo("You don't have any tasks yet.")

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """ Show task list. """
    if not ctx.invoked_subcommand:
        show_tasks()

cli.add_command(add)
cli.add_command(remove)
cli.add_command(done)
cli.add_command(undone)