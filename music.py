import spotipy
from spotipy.oauth2 import SpotifyOAuth

from system_control import speak

# Set your credentials here
CLIENT_ID = "7396db1db37d476ba8ad6e25e0f81f88"
CLIENT_SECRET = "57af8f26c14b4fed8277d8306c15eb74"
REDIRECT_URI = "http://127.0.0.1:8888/callback"# This is your redirect URI
SCOPE = "user-library-read user-read-playback-state user-modify-playback-state"

# Authenticate using Spotify OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

def play_music():
    sp.start_playback()  # Play music on the currently active device
    speak("Playing music")

def pause_music():
    sp.pause_playback()  # Pause the current playback
    speak("Music paused")

def next_song():
    sp.skip_to_next()  # Skip to the next song
    speak("Skipping to next song")

def previous_song():
    sp.skip_to_previous()  # Go back to the previous song
    speak("Going to previous song")
