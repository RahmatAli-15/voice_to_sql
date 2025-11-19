from agents.speech_agent import SpeechAgent
from agents.voice_agent import VoiceAgent
from agents.trading_agent import TradingAgent

def main():
    stt = SpeechAgent()
    tts = VoiceAgent()
    trader = TradingAgent()

    tts.speak("Hello. I am Your Voice to Sql Analyst")

    # Record → Transcribe
    audio = stt.listen()
    text = stt.transcribe(audio).strip().lower()

    if not text:
        tts.speak("Welcome! Speak your trading question and I’ll analyze it using SQL.")
        return

    print("User:", text)

    # Exit phrases detected
    EXIT_WORDS = ["bye", "exit", "quit", "stop", "end"]
    if any(word in text for word in EXIT_WORDS):
        tts.speak("Goodbye.")
        return

    # Process ONE question ONLY
    answer = trader.ask(text)
    print("Answer:", answer)

    # Speak final answer
    tts.speak(answer)

    # EXIT after answering
    tts.speak("Goodbye.")
    return

if __name__ == "__main__":
    main()
