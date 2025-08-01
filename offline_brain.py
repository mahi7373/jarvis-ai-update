# offline_brain.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class OfflineBrain:
    def __init__(self):
        print("🔌 Loading Offline Brain (Phi-2 from HuggingFace)...")
        model_name = "microsoft/phi-2"  # Small but powerful model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def generate(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(**inputs, max_length=200)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
class OfflineBrain:
    def process(self, query):
        # Simple offline logic (can be improved with local AI models)
        responses = {
            "hello": "Hi! I am your offline Jarvis.",
            "how are you": "I am running perfectly without the internet!",
            "who are you": "I am Jarvis, your AI assistant (Offline Mode)."
        }
        return responses.get(query.lower(), "Offline Brain: Sorry, I don’t understand that.")
