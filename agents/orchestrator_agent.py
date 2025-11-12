from agents.nlu_agent import NLUAgent
from agents.category_agent import CategoryAgent
from agents.restaurant_agent import RestaurantAgent
from agents.food_agent import FoodAgent
from agents.address_agent import AddressAgent
from agents.payment_agent import PaymentAgent
from agents.confirmation_agent import ConfirmationAgent
from agents.order_tracking_agent import OrderTrackingAgent
from core.context_engine import ContextEngine


class OrchestratorAgent:
    def __init__(self):
        # 🧠 Load context + agents
        self.context = ContextEngine()
        self.nlu = NLUAgent()
        self.category = CategoryAgent()
        self.restaurant = RestaurantAgent()
        self.food = FoodAgent()
        self.address = AddressAgent()
        self.payment = PaymentAgent()
        self.confirm = ConfirmationAgent()
        self.track = OrderTrackingAgent()

        # ⚙️ Session control: helps us know if user has already ordered in this session
        self.session_has_completed_order = False

        # 🎬 Simple neutral greeting
        self.initial_message = (
            "Hi 👋 I'm your AI Food Assistant! 🍽️\nWould you like to order Food 🍕 or Groceries 🛒?"
        )

    def handle_message(self, text: str):
        prev = self.context.previous_state
        intent = self.nlu.detect_intent(text)
        stage = self.context.state.get("stage", "start")

        # 🧠 Only show reorder suggestion if a *previous confirmed order exists*
        has_completed_order = (
            prev
            and prev.get("stage") == "confirmed"
            and self.session_has_completed_order  # 👈 New safeguard
        )

        # 🍽️ When user says they want food
        if intent == "order_food":
            self.context.update("order_type", "food")
            self.context.update("stage", "category")

            # ✅ Only suggest reorder if user has completed at least one order in this session
            if has_completed_order:
                last_cat = prev.get("category")
                last_rest = prev.get("restaurant")
                last_item = prev.get("items", [{}])[0].get("name", "")
                last_addr = prev.get("address", {}).get("street", "")
                return (
                    f"🍴 You previously ordered {last_item} from {last_rest} ({last_cat} cuisine), "
                    f"delivered to {last_addr}.\nWould you like to reorder the same meal?"
                )

            # 🆕 Fresh order — show categories
            return self.category.get_categories("food")

        # 🧠 Handle “Yes” for reorder flow
        if text.lower() in ["yes", "yeah", "yep", "sure", "ok", "okay"] and has_completed_order:
            if stage == "start" or stage == "category":
                self.context.update("category", prev["category"])
                self.context.update("restaurant", prev["restaurant"])
                self.context.update("stage", "menu")
                item_name = prev["items"][0]["name"]
                return f"Would you like to reorder the same dish — {item_name}? 🍛"

            elif stage == "menu":
                self.context.state["items"] = prev["items"]
                self.context.update("stage", "address")
                addr = prev["address"].get("street", "your previous address")
                return f"Shall I deliver it again to {addr}? 🏠"

            elif stage == "address":
                self.context.update("address", prev["address"])
                self.context.update("payment_method", prev.get("payment_method", "Cash on Delivery"))
                self.context.update("stage", "confirmed")
                msg = self.confirm.confirm_order(self.context)
                self.context.save_memory()
                self.session_has_completed_order = True  # ✅ Mark that an order has been completed
                return msg

        # 🛒 Grocery flow
        elif intent == "order_grocery":
            self.context.update("order_type", "grocery")
            self.context.update("stage", "category")
            return self.category.get_categories("grocery")

        elif intent == "track_order":
            return self.track.track_order()

        # 🔄 Regular food order stages
        if stage == "category":
            self.context.update("category", text)
            self.context.update("stage", "restaurant")
            return self.restaurant.get_restaurants(text)

        elif stage == "restaurant":
            self.context.update("restaurant", text)
            self.context.update("stage", "menu")
            return self.restaurant.get_menu(text)

        elif stage == "menu":
            if "checkout" in text.lower():
                self.context.update("stage", "address")
                return "Please enter your delivery address 🏠"
            return self.food.handle_food_order(text, self.context)

        elif stage == "address":
            self.context.update("address", {"street": text})
            self.context.update("stage", "payment")
            return "✅ Address saved! Choose your payment method 💳"

        elif stage == "payment":
            self.context.update("payment_method", text)
            self.context.update("stage", "confirmed")
            msg = self.confirm.confirm_order(self.context)
            self.context.save_memory()
            self.session_has_completed_order = True  # ✅ Record completion in session
            return msg

        return "Would you like to order Food 🍽️ or Groceries 🛒?"
