from nlp.transformer_model import TransformerModel
from nlp.intent_classifier import IntentClassifier
from core.scratch_pad import ScratchPad

class NLUAgent:
    def __init__(self):
        self.transformer = TransformerModel()
        self.intent_model = IntentClassifier()
        self.scratch = ScratchPad()

    def detect_intent(self, text):
        self.scratch.write(f"Analyzing: {text}")
        intent = self.intent_model.predict_intent(text)
        sentiment, score = self.transformer.classify(text)
        self.scratch.write(f"Intent: {intent}, Sentiment: {sentiment}, Confidence: {score}")
        return intent
