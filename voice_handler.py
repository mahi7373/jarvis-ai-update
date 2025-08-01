import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import tempfile

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        pygame.mixer.init()
    
    def listen(self):
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5)
            
            text = self.recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except sr.RequestError:
            return "Speech recognition service unavailable."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def speak(self, text):
        try:
            tts = gTTS(text=text, lang="en")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tts.save(tmp_file.name)
                
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                os.unlink(tmp_file.name)
        except Exception as e:
            print(f"Speech error: {e}")
            print(f"Jarvis: {text}")  # Fallback to text