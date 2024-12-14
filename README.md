# About
This is a simple command-line tool for managing tasks. It allows you to:

1. View a list of tasks.
2. Add and remove tasks.
3. Mark tasks as done or undone.

Perfect for keeping track of your daily tasks with minimal setup!

# Prerequisites
- Python 3.12 or higher.
- `pip` (Python package installer).

# Installation
To install this application, follow these steps:
```bash
# Clone the repository
git clone https://github.com/artenderrr/cli-todo-app.git

# Navigate to the project directory
cd cli-todo-app

# Install package with pip
pip install .

# (Optional) Delete unnecessary files
cd ..
rm -rf cli-todo-app
```

# Usage

## Managing Single Task
```bash
todos                      # View a list of tasks

todos add "Brew coffee"    # Add a new task

todos done "Brew coffee"   # Mark a task as done

todos undone "Brew coffee" # Mark a task as not done

todos remove "Brew coffee" # Remove a task
```
* **Note**: Task names are case-sensitive, so `"brew coffee"` and `"Brew coffee"` are considered different tasks.

## Managing Multiple Tasks
```bash
todos add "Code" "Eat" "Rest"

todos done "Code" "Eat" "Rest"

todos undone "Code" "Rest"

todos remove "Code" "Eat"
```
* **Note**: You can manage as many tasks at the same time as you want!

## Managing Tasks By IDs
To speed up interaction with this app you can use unique task IDs to manage specific tasks.
```bash
todos done 4

todos undone 2 6 24 120

todos remove 3 5 8 13 21
```
* **Note**: You can find task IDs in the `todos` command output, specifically in the grey parentheses to the right of each task name.

## Managing Tasks Using Flags
```bash
todos remove --all  # Remove all tasks

todos remove -a     # Short form of --all

todos remove --done # Remove all done tasks

todos remove -d     # Short form of --done

todos done --all    # Mark all tasks as done

todos done -a       # Short form of --all
```
* **Note**: The flags `-a` and `--all` can also be used with the `todos undone` command to mark all tasks as undone.

## Getting Help
You can always get help by using `--help` flag with any existing command.
```bash
todos --help        # Show list of available commands

todos remove --help # Show usage for specific command
```

# License
This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

# Contribution
Contributions are welcome! Feel free to open issues or submit pull requests.