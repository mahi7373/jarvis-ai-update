import json
import os
import requests
from datetime import datetime

class BrainManager:
    def __init__(self):
        self.memory_file = "memory.json"
        self.current_brain = "offline"  # offline or online
        self.memory = self.load_memory()
    
    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {"conversations": [], "preferences": {}}
    
    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def switch_to_offline(self):
        self.current_brain = "offline"
        return "Switched to offline brain"
    
    def switch_to_online(self):
        self.current_brain = "online"
        return "Switched to online brain"
    
    def think(self, query):
        # Save conversation to memory
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "brain_type": self.current_brain
        }
        
        if self.current_brain == "offline":
            response = self.offline_brain(query)
        else:
            response = self.online_brain(query)
        
        conversation["response"] = response
        self.memory["conversations"].append(conversation)
        self.save_memory()
        
        return response
    
    def offline_brain(self, query):
        # Simple offline responses
        query_lower = query.lower()
        
        if "hello" in query_lower or "hi" in query_lower:
            return "Hello! I'm Jarvis, your offline AI assistant."
        elif "time" in query_lower:
            return f"Current time is {datetime.now().strftime('%H:%M:%S')}"
        elif "date" in query_lower:
            return f"Today is {datetime.now().strftime('%Y-%m-%d')}"
        elif "weather" in query_lower:
            return "I need online mode to check weather."
        elif "youtube" in query_lower or "video" in query_lower:
            return "Video processing available. What would you like me to do?"
        else:
            return f"I understand you said: {query}. How can I help you?"
    
    def online_brain(self, query):
        # Simulate online AI (replace with actual API)
        try:
            # This would be replaced with actual AI API call
            return f"Online AI response to: {query}"
        except:
            return "Online brain temporarily unavailable. Switching to offline mode."