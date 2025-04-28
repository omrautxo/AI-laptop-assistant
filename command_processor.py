import os
import pyjokes
import webbrowser
import subprocess
import platform
from datetime import datetime
from pathlib import Path
import psutil
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from system_control import open_application
from voice_assistant import speak
from memory import remember, recall_memory

# System audio control
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import ctypes

# --- Spotify Setup ---
CLIENT_ID = "7396db1db37d476ba8ad6e25e0f81f88"
CLIENT_SECRET = "57af8f26c14b4fed8277d8306c15eb74"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "user-library-read user-read-playback-state user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))


# --- System Control ---
def shutdown_system():
    speak("Shutting down the system...")
    os.system("shutdown /s /f /t 1")


def restart_system():
    speak("Restarting the system...")
    os.system("shutdown /r /f /t 1")


def lock_computer():
    speak("Locking the system...")
    ctypes.windll.user32.LockWorkStation()


def get_volume_interface():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))
    except Exception as e:
        speak("Failed to get volume control.")
        print("Volume Interface Error:", e)
        return None


def mute_system():
    volume_interface = get_volume_interface()
    if volume_interface:
        volume_interface.SetMute(1, None)
        speak("System muted.")


def unmute_system():
    volume_interface = get_volume_interface()
    if volume_interface:
        volume_interface.SetMute(0, None)
        # Check if volume is 0 and set to minimum if needed
        current_volume = volume_interface.GetMasterVolumeLevelScalar()
        if current_volume < 0.05:
            volume_interface.SetMasterVolumeLevelScalar(0.1, None)
            speak("System unmuted and volume raised to 10%.")
        else:
            speak("System unmuted.")


def set_volume(volume):
    try:
        volume = max(0, min(100, volume))  # Clamp between 0-100
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
        volume_interface.SetMasterVolumeLevelScalar(volume / 100, None)
        speak(f"Volume set to {volume} percent.")
    except Exception as e:
        speak("Failed to set volume.")
        print("Volume Error:", e)


def sleep_system():
    speak("Putting the system to sleep...")
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


def hibernate_system():
    speak("Hibernating the system...")
    os.system("shutdown /h")


def open_app(app_name):
    open_application(app_name)


# --- Spotify Music Control ---
def play_music():
    try:
        devices = sp.devices()
        if not devices['devices']:
            speak("No active Spotify device found.")
            return
        sp.start_playback()
        speak("Playing music.")
    except spotipy.exceptions.SpotifyException as e:
        speak("Spotify error: " + str(e))


def pause_music():
    try:
        sp.pause_playback()
        speak("Music paused.")
    except spotipy.exceptions.SpotifyException as e:
        speak("Spotify error: " + str(e))


def next_song():
    try:
        sp.skip_to_next()
        speak("Skipping to next song.")
    except spotipy.exceptions.SpotifyException as e:
        speak("Spotify error: " + str(e))


def previous_song():
    try:
        sp.skip_to_previous()
        speak("Going to previous song.")
    except spotipy.exceptions.SpotifyException as e:
        speak("Spotify error: " + str(e))


# --- Weather Function ---
def get_weather(city):
    API_KEY = "98a9405cce908733a8f87bbecf299694"
    URL = "https://api.openweathermap.org/data/2.5/weather"
    try:
        res = requests.get(URL, params={"q": city, "appid": API_KEY, "units": "metric"})
        data = res.json()
        if res.status_code == 200:
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            return f"{weather.capitalize()} in {city}. Temp: {temp}°C, feels like {feels_like}°C."
        else:
            return "City not found."
    except Exception as e:
        return f"Weather fetch failed: {e}"


# --- Command Processor ---
def process_command(command):
    command = command.lower()
    try:
        if "hello" in command:
            speak("Hey pal! How can I help you?")

        elif "weather in" in command:
            city = command.split("weather in")[-1].strip()
            speak(get_weather(city))

        elif "shutdown" in command:
            shutdown_system()
        elif "restart" in command:
            restart_system()
        elif "lock" in command:
            lock_computer()
        elif "mute" in command:
            mute_system()
        elif "unmute" in command:
            unmute_system()

        elif "volume" in command:
            try:
                volume = int(command.split("volume")[-1].strip())
                set_volume(volume)
            except:
                speak("Please provide volume like volume 50.")

        elif "sleep" in command:
            sleep_system()
        elif "hibernate" in command:
            hibernate_system()
        elif "open" in command:
            app_name = command.replace("open", "").strip()
            open_app(app_name)
            speak(f"Opening {app_name}")

        elif "play music" in command:
            play_music()
        elif "pause music" in command:
            pause_music()
        elif "next song" in command:
            next_song()
        elif "previous song" in command:
            previous_song()

        elif "tell me a joke" in command:
            speak(pyjokes.get_joke())

        elif "how are you" in command:
            speak("I'm always awesome, because I have you as my creator!")

        elif "search for" in command:
            query = command.replace("search for", "").strip()
            if query:
                speak(f"Searching for {query}")
                webbrowser.open(f"https://www.google.com/search?q={query}")
            else:
                speak("Please specify what to search for.")

        elif "remember that" in command:
            note = command.replace("remember that", "").strip()
            remember(note)
            speak(f"Okay, I will remember that: {note}")

        elif "what did i ask you to remember" in command or "do you remember anything" in command:
            memories = recall_memory()
            for m in memories:
                speak(m)

        elif "open downloads folder" in command:
            os.startfile(str(Path.home() / "Downloads"))
            speak("Opening Downloads folder.")
        elif "open documents folder" in command:
            os.startfile(str(Path.home() / "Documents"))
            speak("Opening Documents folder.")
        elif "list files in downloads" in command:
            files = os.listdir(str(Path.home() / "Downloads"))
            speak("Files in your Downloads folder:")
            for f in files[:5]:
                speak(f)

        elif "time" in command:
            speak("Current time is " + datetime.now().strftime("%I:%M %p"))
        elif "date" in command:
            speak("Today is " + datetime.now().strftime("%A, %B %d, %Y"))

        elif "exit" in command or "quit" in command:
            speak("Goodbye Sir. Call me when you need me.")
            exit()

        else:
            speak("Sorry, I didn't understand that.")
    except Exception as e:
        speak("An error occurred.")
        print("Command error:", e)
