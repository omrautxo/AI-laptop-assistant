import os
import webbrowser

from system_control import apps, speak, web_apps


def open_application(app_name):
    app_name = app_name.lower()

    # Predefined apps for local opening (not websites)
    if app_name in apps:
        try:
            os.startfile(apps[app_name])
        except FileNotFoundError:
            speak(f"{app_name} not found, opening it on Chrome instead.")
            webbrowser.get('chrome').open(f"https://www.google.com/search?q={app_name}")

    # Predefined websites (example like GitHub, etc.)
    elif app_name in web_apps:
        speak(f"Opening {app_name} in Chrome.")
        webbrowser.get('chrome').open(web_apps[app_name])

    # If it's not found in either category, default to Google search
    else:
        speak(f"I couldn't find {app_name}, searching it on Google.")
        # Open a Google search in Chrome
        webbrowser.get('chrome').open(f"https://www.google.com/search?q={app_name}")
