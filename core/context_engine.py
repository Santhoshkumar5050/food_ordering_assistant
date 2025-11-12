import json
from datetime import datetime
import os

class ContextEngine:
    def __init__(self, memory_path="data/memory.json"):
        self.path = memory_path
        self.state = {
            "intent": None,
            "stage": "start",
            "order_type": None,
            "category": None,
            "restaurant": None,
            "items": [],
            "address": {},
            "payment_method": None,
            "timestamp": datetime.now().isoformat()
        }
        self.previous_state = self.load_memory()

    def update(self, key, value):
        self.state[key] = value

    def add_item(self, item):
        self.state["items"].append(item)

    def get_total(self):
        return sum([i["price"] for i in self.state["items"]])

    def summary(self):
        items = ", ".join([i["name"] for i in self.state["items"]]) or "none"
        total = self.get_total()
        address = self.state.get("address", {})
        return {
            "items": items,
            "total": total,
            "restaurant": self.state.get("restaurant"),
            "address": address,
            "payment": self.state.get("payment_method")
        }

    def save_memory(self):
        with open(self.path, "w") as f:
            json.dump(self.state, f, indent=2)

    def load_memory(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    return json.load(f)
            except Exception:
                return None
        return None
