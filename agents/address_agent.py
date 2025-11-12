class AddressAgent:
    def get_address_prompt(self, prev=None):
        if prev and prev.get("address"):
            addr = prev["address"].get("street", "")
            return f"Would you like to deliver to your previous address: {addr}?"
        return "Please enter your new delivery address 🏠"
