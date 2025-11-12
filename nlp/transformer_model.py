from transformers import pipeline

class TransformerModel:
    def __init__(self):
        self.classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

    def classify(self, text):
        result = self.classifier(text)[0]
        return result["label"], result["score"]
