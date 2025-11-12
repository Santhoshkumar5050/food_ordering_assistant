# agents/grocery_agent.py
import json

class GroceryAgent:
    def __init__(self):
        with open("data/grocery_list.json") as f:
            self.groceries = json.load(f)

    def handle_grocery_order(self, user_input, context):
        items = [item["name"] for item in self.groceries[:5]]
        return "Here are some groceries you can order:\n" + "\n".join(items)
