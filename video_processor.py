import moviepy.editor as mp
import os
from gtts import gTTS

class VideoProcessor:
    def __init__(self):
        self.output_dir = "videos"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def create_video_from_text(self, text, filename="output.mp4"):
        # Create audio from text
        tts = gTTS(text=text, lang="en")
        audio_file = "temp_audio.mp3"
        tts.save(audio_file)
        
        # Create video with audio
        audio_clip = mp.AudioFileClip(audio_file)
        video_clip = mp.ColorClip(size=(1280, 720), color=(0, 0, 0), duration=audio_clip.duration)
        final_video = video_clip.set_audio(audio_clip)
        
        output_path = os.path.join(self.output_dir, filename)
        final_video.write_videofile(output_path, fps=24)
        
        # Cleanup
        os.remove(audio_file)
        audio_clip.close()
        video_clip.close()
        final_video.close()
        
        return output_path
    
    def create_youtube_short(self, text, filename="short.mp4"):
        # Create vertical video for YouTube Shorts
        tts = gTTS(text=text, lang="en")
        audio_file = "temp_audio.mp3"
        tts.save(audio_file)
        
        audio_clip = mp.AudioFileClip(audio_file)
        video_clip = mp.ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=audio_clip.duration)
        final_video = video_clip.set_audio(audio_clip)
        
        output_path = os.path.join(self.output_dir, filename)
        final_video.write_videofile(output_path, fps=24)
        
        # Cleanup
        os.remove(audio_file)
        audio_clip.close()
        video_clip.close()
        final_video.close()
        
        return output_path