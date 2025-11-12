import json
from datetime import datetime

class ScratchPad:
    def __init__(self):
        self.logs = []

    def write(self, thought, action=None, result=None):
        self.logs.append({
            "time": datetime.now().isoformat(),
            "thought": thought,
            "action": action,
            "result": result
        })

    def save(self, path="data/scratch_pad.json"):
        with open(path, "w") as f:
            json.dump(self.logs, f, indent=2)
