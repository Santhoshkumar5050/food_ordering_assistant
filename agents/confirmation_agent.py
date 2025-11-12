class ConfirmationAgent:
    def confirm_order(self, context):
        s = context.summary()
        return (
            f"✅ Order confirmed for {s['items']}.\n"
            f"Delivering to: {s['address'].get('street', 'unknown')}.\n"
            f"💰 Total: ₹{s['total']} | Payment: {s['payment'] or 'COD'}.\n"
            "🚀 Your order will arrive soon!"
        )
