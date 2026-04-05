import os
import json
from datetime import datetime


class PersonRegistry:
    def __init__(self, save_path="backend/storage/persons"):
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)

        self.registry_file = os.path.join(
            self.save_path,
            "person_registry.json"
        )

        if not os.path.exists(self.registry_file):
            with open(self.registry_file, "w") as f:
                json.dump({}, f)

    def load_registry(self):
        with open(self.registry_file, "r") as f:
            return json.load(f)

    def save_registry(self, data):
        with open(self.registry_file, "w") as f:
            json.dump(data, f, indent=2)

    def register_person(self, person_id, image_path):
        data = self.load_registry()

        data[str(person_id)] = {
            "image": image_path,
            "time": str(datetime.now())
        }

        self.save_registry(data)

    def get_person(self, person_id):
        data = self.load_registry()
        return data.get(str(person_id), None)

    def get_all(self):
        return self.load_registry()