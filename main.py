from brain_manager import BrainManager
from voice_handler import VoiceHandler
from video_processor import VideoProcessor

# Initialize components
jarvis_brain = BrainManager()
voice_handler = VoiceHandler()
video_processor = VideoProcessor()

print("🤖 Jarvis AI Ready! (Dual Brain + Voice + Video)")
print("Commands: 'switch brain', 'create video', 'voice mode', 'exit'")

while True:
    mode = input("\nInput Mode (text/voice): ").lower()
    
    if mode == "voice":
        query = voice_handler.listen()
        print(f"🗣️ You: {query}")
    else:
        query = input("🗣️ You: ")
    
    if "exit" in query.lower() or "quit" in query.lower():
        voice_handler.speak("Goodbye!")
        break
    elif "switch to offline" in query.lower():
        jarvis_brain.switch_to_offline()
        voice_handler.speak("Switched to offline brain")
        continue
    elif "switch to online" in query.lower():
        jarvis_brain.switch_to_online()
        voice_handler.speak("Switched to online brain")
        continue
    elif "create video" in query.lower():
        text = input("Enter text for video: ")
        video_path = video_processor.create_video_from_text(text)
        response = f"Video created: {video_path}"
    elif "create short" in query.lower():
        text = input("Enter text for YouTube Short: ")
        video_path = video_processor.create_youtube_short(text)
        response = f"YouTube Short created: {video_path}"
    else:
        response = jarvis_brain.think(query)
    
    print(f"🤖 Jarvis ({jarvis_brain.current_brain}): {response}")
    voice_handler.speak(response)
