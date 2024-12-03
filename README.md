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
```

# Usage
```bash
todos # View a list of tasks

todos add "Brew coffee" # Add a new task

todos done "Brew coffee" # Mark a task as done

todos undone "Brew coffee" # Mark a task as not done

todos remove "Brew coffee" # Remove a task
```
* **Note**: Task names are case-sensitive, so `"brew coffee"` and `"Brew coffee"` are considered different tasks.

# License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

# Contribution
Contributions are welcome! Feel free to open issues or submit pull requests.