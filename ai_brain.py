import json
import datetime

class AIBrain:
    def __init__(self, memory_file="memory.json"):
        self.memory_file = memory_file
        self.memory = self.load_memory()

    def load_memory(self):
        try:
            with open(self.memory_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_memory(self):
        with open(self.memory_file, "w") as file:
            json.dump(self.memory, file, indent=4)

    def think(self, query):
        if query in self.memory:
            return f"📖 मैंने पहले सीखा था: {self.memory[query]}"
        plan = self.generate_plan(query)
        self.memory[query] = plan
        self.save_memory()
        return plan

    def generate_plan(self, query):
        steps = [
            f"स्टेप 1: '{query}' के लिए रिसर्च करो",
            f"स्टेप 2: '{query}' को करने के लिए ज़रूरी टूल इस्तेमाल करो",
            f"स्टेप 3: रिज़ल्ट चेक करो और रिपोर्ट बनाओ"
        ]
        return {
            "query": query,
            "plan": steps,
            "time": str(datetime.datetime.now())
        }
