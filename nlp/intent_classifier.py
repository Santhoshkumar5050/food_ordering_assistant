from sentence_transformers import SentenceTransformer, util

class IntentClassifier:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.intents = {
            "order_food": ["I want food", "I'm hungry", "show menu", "order food"],
            "checkout": ["checkout", "confirm order", "place order", "finish order"],
            "address": ["my address", "deliver to", "send to"],
            "payment": ["cash", "UPI", "card", "payment"],
        }
        self.embeddings = {k: self.model.encode(v) for k, v in self.intents.items()}

    def predict_intent(self, text):
        query_vec = self.model.encode(text)
        best_intent, best_score = "unknown", -1
        for intent, vectors in self.embeddings.items():
            score = max(util.cos_sim(query_vec, vectors).tolist()[0])
            if score > best_score:
                best_intent, best_score = intent, score
        return best_intent if best_score > 0.4 else "unknown"
