import webbrowser
from voice_assistant import speak, listen
from command_processor import process_command

speak("Hello SIR!")

while True:
    command = listen()
    if command:
        process_command(command)

     #command = input("What do you want to do? ").lower()
    #search_web_command(command)


    def search_web_command(command):
        command = command.lower()

        if "search" in command:
            query = ""
            if "on google" in command:
                query = command.replace("search", "").replace("on google", "").strip()
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                speak(f"Searching {query} on Google")
                webbrowser.get('chrome').open(url)

            elif "on youtube" in command:
                query = command.replace("search", "").replace("on youtube", "").strip()
                url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                speak(f"Searching {query} on YouTube")
                webbrowser.get('chrome').open(url)

            elif "on wikipedia" in command:
                query = command.replace("search", "").replace("on wikipedia", "").strip()
                url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
                speak(f"Searching {query} on Wikipedia")
                webbrowser.get('chrome').open(url)



