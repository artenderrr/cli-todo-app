import os
import json
from json.decoder import JSONDecodeError
from cli_todo_app.vacant_ids import VacantIDs

class Tasks:
    def __init__(self):
        self.file_path = Tasks.get_file_path()
        self.items = self.load_items()

    @property
    def all_item_names(self):
        return [i["name"] for i in self.items]

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
        file_path = os.path.join(script_path, "data/todos.json")
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
        # item should contain only three key-value pairs
        if not len(item.items()) == 3:
            return False
        # item should contain "id", "name" and "done" keys
        if not all(key in item for key in ("id", "name", "done")):
            return False
        # value of "id" should be integer
        if not isinstance(item["id"], int):
            return False
        # value of "name" should be string
        if not isinstance(item["name"], str):
            return False
        # value of "done" should be boolean
        if not isinstance(item["done"], bool):
            return False
        return True
    
    @staticmethod
    def get_valid_task_names(names):
        valid_task_names = set()
        invalid_task_names = set()
        for name in names:
            if name.isdigit():
                invalid_task_names.add(name)
            else:
                valid_task_names.add(name)
        return [*valid_task_names], [*invalid_task_names]
    
    def dump_items(self):
        """ Dumps tasks to the file """
        with open(self.file_path, "w") as f:
            json.dump(self.items, f, indent=4)
    
    def add_item(self, name):
        """ Adds new task with the given name to the list if the name is unique and returns completion status """
        if not self.has_item_with_name(name):
            new_task = {
                "id": VacantIDs().get_vacant_id(),
                "name": name,
                "done": False
            }
            self.items.append(new_task)
            self.dump_items()
            return True
        return False
    
    def add_items(self, names):
        """ Adds new tasks using .add_item() for each name from given ones and returns response with metadata """
        response = {"added": [], "already exist": []}
        names, response["invalid names"] = Tasks.get_valid_task_names(names)
        for name in names:
            success = self.add_item(name)
            response["added" if success else "already exist"].append(name)
        return response

    def has_item_with_name(self, name):
        """ Checks if task with given name already exists """
        return next((True for i in self.items if i["name"] == name), False)
    
    def remove_item(self, name):
        """ Removes task with the given name from the list if it exists and returns completion status """
        if self.has_item_with_name(name):
            for i in range(len(self.items)):
                if self.items[i]["name"] == name:
                    VacantIDs().add_vacant_id(self.items[i]["id"])
                    self.items.pop(i)
                    break
            self.dump_items()
            return True
        return False
    
    def get_task_name_by_id(self, task_id):
        """ Returns task name by its ID if task with such ID exists, else None """
        return next((task["name"] for task in self.items if task["id"] == task_id), None)
    
    def get_names_with_ids_replaced(self, names):
        """ Replaces IDs with actual task names, removes duplicate task names or IDs and returns result and IDs that are nonexistent (if present) """
        names_with_ids_replaced = set()
        nonexistent_ids = set()
        for name in names:
            if name.isdigit(): # this means that current 'name' contains ID
                task_id = int(name)
                name_from_id = self.get_task_name_by_id(task_id)
                if name_from_id:
                    names_with_ids_replaced.add(name_from_id)
                else:
                    nonexistent_ids.add(name)
            else:
                names_with_ids_replaced.add(name)
        return [*names_with_ids_replaced], [*nonexistent_ids]
    
    def remove_items(self, names):
        """ Removes tasks using .remove_item() for each name from given ones and returns Response object """
        response = {"removed": [], "don't exist": []}
        names, response["nonexistent ids"] = self.get_names_with_ids_replaced(names)
        for name in names:
            success = self.remove_item(name)
            response["removed" if success else "don't exist"].append(name)
        return response
    
    def remove_all_items(self):
        """ Removes all tasks using .remote_items() and returns Response object """
        response = self.remove_items(self.all_item_names)
        VacantIDs().clear_vacant_ids()
        return response
    
    def remove_done_items(self):
        """ Removes all tasks that are marked as done using .remove_items() and returns Response object """
        done_item_names = [i["name"] for i in self.items if i["done"]]
        response = self.remove_items(done_item_names)
        return response
    
    def mark_item_done(self, name):
        """ Marks task with the given name as done and returns completion status """
        if self.has_item_with_name(name):
            for i in self.items:
                if i["name"] == name:
                    if not i["done"]:
                        i["done"] = True
                        self.dump_items()
                        return "done"
                    else:
                        return "already done"
        return "don't exist"
    
    def mark_items_done(self, names):
        """ Marks tasks as done using .mark_item_done() for each name from given ones and returns Response object"""
        response = {"done": [], "already done": [], "don't exist": []}
        names, response["nonexistent ids"] = self.get_names_with_ids_replaced(names)
        for name in names:
            status = self.mark_item_done(name)
            response[status].append(name)
        return response
    
    def mark_all_items_done(self):
        """ Marks all tasks as done using .mark_items_done() and return Response object """
        response = self.mark_items_done(self.all_item_names)
        return response
    
    def mark_item_not_done(self, name):
        """ Marks task with the given name as not done and returns completion status """
        if self.has_item_with_name(name):
            for i in self.items:
                if i["name"] == name:
                    if i["done"]:
                        i["done"] = False
                        self.dump_items()
                        return "undone"
                    else:
                        return "already undone"
        return "don't exist"
    
    def mark_items_not_done(self, names):
        """ Marks tasks as not done using .mark_item_not_done() for each name from given ones and returns Response object"""
        response = {"undone": [], "already undone": [], "don't exist": []}
        names, response["nonexistent ids"] = self.get_names_with_ids_replaced(names)
        for name in names:
            status = self.mark_item_not_done(name)
            response[status].append(name)
        return response
    
    def mark_all_items_not_done(self):
        """ Marks all tasks as not done using .mark_items_not_done() and returns Response object """
        response = self.mark_items_not_done(self.all_item_names)
        return response