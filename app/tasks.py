import os
import json
from json.decoder import JSONDecodeError

class Tasks:
    def __init__(self):
        self.file_path = Tasks.get_file_path()
        self.items = self.load_items()

    def load_items(self):
        """ Loads tasks from file and returns them as a list of dictionaries """
        try:
            with open(self.file_path, encoding="utf-8") as f:
                loaded_items = json.load(f)
                valid_items = self.get_valid_items(loaded_items)
                return valid_items
        except (FileNotFoundError, JSONDecodeError):
            return []
    
    @staticmethod
    def get_file_path():
        """ Generates an absolute path to the tasks file relative to this script directory """
        script_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_path, "../data/todos.json")
        return file_path
    
    @staticmethod
    def get_valid_items(items):
        """ Filters loaded items to get only valid ones """
        # loaded items should be represented as a list
        if not isinstance(items, list):
            return []
        return [*filter(Tasks.validate_item, items)]

    @staticmethod
    def validate_item(item):
        """ Validates single given item from loaded ones """
        # item should be dictionary
        if not isinstance(item, dict):
            return False
        # item should contain only two key-value pairs
        if not len(item.items()) == 2:
            return False
        # item should contain "name" and "done" keys
        if "name" not in item or "done" not in item:
            return False
        # value of "name" should be string
        if not isinstance(item["name"], str):
            return False
        # value of "done" should be boolean
        if not isinstance(item["done"], bool):
            return False
        return True
    
    def dump_items(self):
        """ Dumps tasks to the file """
        with open(self.file_path, "w") as f:
            json.dump(self.items, f, indent=4)
    
    def add_item(self, name):
        """ Adds new task with the given name to the list if the name is unique and returns completion status """
        if not self.has_item_with_name(name):
            new_task = {
                "name": name,
                "done": False
            }
            self.items.append(new_task)
            self.dump_items()
            return True
        return False

    def has_item_with_name(self, name):
        """ Checks if task with given name already exists """
        return next((True for i in self.items if i["name"] == name), False)