import os
import json
from json.decoder import JSONDecodeError

class VacantIDs:
    def __init__(self):
        self.file_path = VacantIDs.get_file_path()
        self.items = self.load_items()

    @staticmethod
    def get_file_path():
        script_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_path, "data/vacant_ids.json")
        return file_path

    def load_items(self):
        try:
            with open(self.file_path, encoding="utf-8") as f:
                loaded_items = json.load(f)
                valid_items = VacantIDs.get_valid_items(loaded_items)
                return valid_items
        except (FileNotFoundError, JSONDecodeError):
            return []
    
    def dump_items(self):
        with open(self.file_path, "w") as f:
            json.dump(self.items, f)
        
    @staticmethod
    def get_valid_items(items):
        if not isinstance(items, list):
            return []
        return [*filter(lambda item: type(item) == int and item > 0, items)]

    def get_vacant_id(self):
        if len(self.items) > 1:
            vacant_id = self.items.pop()
        else:
            vacant_id = self.items[0]
            self.items[0] += 1
        self.dump_items()
        return vacant_id
        
    def add_vacant_id(self, vacant_id):
        self.items.append(vacant_id)
        self.dump_items()