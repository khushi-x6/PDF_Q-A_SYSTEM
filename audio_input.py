import speech_recognition as sr

def record_and_transcribe():
    """
    Uses microphone to record and convert to text using Google Speech-to-Text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from Google STT service: {e}"
