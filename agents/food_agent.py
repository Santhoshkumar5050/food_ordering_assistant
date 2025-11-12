class FoodAgent:
    def handle_food_order(self, text, context):
        restaurant = context.state["restaurant"]
        category = context.state["category"]
        from agents.restaurant_agent import RestaurantAgent
        data = RestaurantAgent().restaurants

        for item in data.get(category, {}).get(restaurant, []):
            if item["name"].lower() in text.lower():
                context.add_item(item)
                total = context.get_total()
                return f"🛍️ {item['name']} added! 💰 Total: ₹{total}. Type 'checkout' when ready."

        # Suggest previous item if exists
        prev = context.previous_state
        if prev and prev.get("items"):
            return f"Would you like to reorder {prev['items'][0]['name']} again?"
        return "Please choose an item from the menu."
