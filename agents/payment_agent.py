class PaymentAgent:
    def save_payment(self, context, method):
        context.update("payment_method", method)
        return f"✅ Payment method set to {method}"
