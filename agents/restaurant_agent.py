import json

class RestaurantAgent:
    def __init__(self, path="data/restaurants.json"):
        with open(path, "r") as f:
            self.restaurants = json.load(f)

    def get_restaurants(self, category):
        category = category.strip().lower()
        for cat, rest_data in self.restaurants.items():
            if category in cat.lower():
                names = list(rest_data.keys())
                return f"🍴 Restaurants: {', '.join(names)}"
        return "No restaurants found for this category."

    def get_menu(self, restaurant):
        restaurant = restaurant.strip().lower()
        for cat, rest_data in self.restaurants.items():
            for rest_name, menu in rest_data.items():
                if restaurant in rest_name.lower():
                    menu_str = "\n".join([f"{i['name']} (₹{i['price']})" for i in menu])
                    return f"📜 Menu for {rest_name}:\n\n{menu_str}"
        return "No menu found for this restaurant."
