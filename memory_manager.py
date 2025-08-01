import json
import os
from datetime import datetime

MEMORY_FILE = "memory.json"

class MemoryManager:
    def __init__(self):
        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "w") as f:
                json.dump({"history": []}, f)

    def load_memory(self):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)

    def save_memory(self, data):
        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def add_entry(self, user_input, jarvis_response):
        data = self.load_memory()
        data["history"].append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_input,
            "jarvis": jarvis_response
        })
        self.save_memory(data)

    def get_recent_memory(self, limit=5):
        data = self.load_memory()
        return data["history"][-limit:]

    def search_memory(self, keyword):
        data = self.load_memory()
        return [item for item in data["history"] if keyword.lower() in item["user"].lower() or keyword.lower() in item["jarvis"].lower()]
