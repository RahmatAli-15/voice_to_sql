import os
import logging
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
from elevenlabs import VoiceSettings

load_dotenv()

class VoiceAgent:
    def __init__(self, voice_id="2qfp6zPuviqeCOZIE9RZ", model_id="eleven_multilingual_v2"):
        self.voice_id = voice_id
        self.model_id = model_id

        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            logging.warning("ELEVENLABS_API_KEY missing — TTS disabled.")
            self.client = None
        else:
            self.client = ElevenLabs(api_key=api_key)

        self.settings = VoiceSettings(stability=0.5, similarity_boost=0.8)

    def speak(self, text):
        if not text:
            return
        if not self.client:
            print("(TTS disabled):", text)
            return

        audio = self.client.text_to_speech.convert(
            text=text,
            voice_id=self.voice_id,
            model_id=self.model_id,
            voice_settings=self.settings,
            output_format="mp3_44100_128"
        )
        play(audio)
