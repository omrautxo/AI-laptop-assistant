import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
engine.setProperty('rate', 170)


def speak(text):
    engine.say(text)
    engine.runAndWait()


import speech_recognition as sr
import time


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)  # reduced from 1 to 0.3s
        audio = recognizer.listen(source, phrase_time_limit=4)  # Stop after 4 sec

    try:
        start_time = time.time()
        command = recognizer.recognize_google(audio)
        end_time = time.time()
        print(f"🗣️ You said: {command}")
        print(f"⏱️ Recognition took: {round(end_time - start_time, 2)}s")
        return command.lower()
    except sr.UnknownValueError:
        print("Didn't catch that.")
        return ""
    except sr.RequestError:
        print("Network error.")
        return ""
