import json

class CategoryAgent:
    def __init__(self, path="data/categories.json"):
        with open(path, "r") as f:
            self.categories = json.load(f)

    def get_categories(self, order_type):
        items = "\n".join(self.categories.get(order_type, []))
        return f"📋 {order_type.capitalize()} Categories:\n\n{items}"
