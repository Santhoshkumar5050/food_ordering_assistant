import json
import os

class MemoryManager:
    def __init__(self, path="data/memory.json"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def save_memory(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def load_memory(self):
        if not os.path.exists(self.path):
            return None
        with open(self.path, "r") as f:
            return json.load(f)
