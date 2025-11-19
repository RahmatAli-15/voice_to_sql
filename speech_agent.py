import speech_recognition as sr
import logging

class SpeechAgent:
    def __init__(self, timeout=10, phrase_time_limit=8):
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit

    # -----------------------------------------
    # Microphone Listening (CLI mode only)
    # -----------------------------------------
    def listen(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as src:
                r.adjust_for_ambient_noise(src, duration=1)
                print("🎤 Listening...")
                audio = r.listen(
                    src,
                    timeout=self.timeout,
                    phrase_time_limit=self.phrase_time_limit
                )
                return audio
        except Exception as e:
            logging.error(f"Microphone error: {e}")
            return None

    # -----------------------------------------
    # Transcribe microphone audio
    # -----------------------------------------
    def transcribe(self, audio):
        if audio is None:
            return ""
        try:
            return sr.Recognizer().recognize_google(audio)
        except Exception as e:
            logging.error(f"STT Transcribe Error: {e}")
            return ""

    # -----------------------------------------
    # Transcribe audio **from WAV file**
    # (For Streamlit audio recorder)
    # -----------------------------------------
    def transcribe_from_file(self, file_path):
        try:
            r = sr.Recognizer()
            with sr.AudioFile(file_path) as source:
                audio = r.record(source)
            return r.recognize_google(audio)
        except Exception as e:
            logging.error(f"STT File Transcribe Error: {e}")
            return ""
