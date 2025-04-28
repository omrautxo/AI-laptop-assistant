import os
import webbrowser
import pyttsx3
import difflib  # To handle smart suggestions


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


apps = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "vs code": r"C:\Users\OM NILESH RAUT\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "notepad": "notepad.exe",
}

web_apps = {
    # Social Media
    "social_media": {
        "instagram": "https://www.instagram.com/",
        "facebook": "https://www.facebook.com/",
        "twitter": "https://twitter.com/",
        "linkedin": "https://www.linkedin.com/",
        "whatsapp": "https://web.whatsapp.com/",
        "snapchat": "https://www.snapchat.com/",
        "reddit": "https://www.reddit.com/",
        "tumblr": "https://www.tumblr.com/",
        "pinterest": "https://www.pinterest.com/",
    },

    # Video Streaming
    "video_streaming": {
        "youtube": "https://www.youtube.com/",
        "netflix": "https://www.netflix.com/",
        "hulu": "https://www.hulu.com/",
        "vimeo": "https://www.vimeo.com/",
        "twitch": "https://www.twitch.tv/",
    },

    # E-commerce & Shopping
    "e_commerce": {
        "amazon": "https://www.amazon.com/",
        "etsy": "https://www.etsy.com/",
        "aliexpress": "https://www.aliexpress.com/",
        "ebay": "https://www.ebay.com/",
        "walmart": "https://www.walmart.com/",
    },

    # News & Magazines
    "news": {
        "bbc": "https://www.bbc.com/",
        "cnn": "https://www.cnn.com/",
        "theguardian": "https://www.theguardian.com/",
        "bbc_news": "https://www.bbc.com/news",
        "forbes": "https://www.forbes.com/",
        "sky_news": "https://news.sky.com/",
    },

    # Communication & Collaboration
    "communication": {
        "zoom": "https://zoom.us/",
        "slack": "https://slack.com/",
        "discord": "https://discord.com/",
        "gmail": "https://mail.google.com/",
    },

    # Productivity & Work Tools
    "productivity": {
        "google_drive": "https://drive.google.com/",
        "dropbox": "https://www.dropbox.com/",
        "trello": "https://trello.com/",
        "notion": "https://www.notion.so/",
        "evernote": "https://www.evernote.com/",
    },

    # Tech & Developer Tools
    "tech_tools": {
        "github": "https://www.github.com/",
        "stackoverflow": "https://stackoverflow.com/",
        "gitlab": "https://gitlab.com/",
        "bitbucket": "https://bitbucket.org/",
        "docker": "https://www.docker.com/",
    },

    # Learning & Research
    "learning": {
        "wikipedia": "https://www.wikipedia.org/",
        "quora": "https://www.quora.com/",
        "medium": "https://medium.com/",
        "coursera": "https://www.coursera.org/",
        "edx": "https://www.edx.org/",
    },

    # Entertainment & Games
    "entertainment": {
        "spotify": "https://www.spotify.com/",
        "steam": "https://store.steampowered.com/",
        "epic_games": "https://www.epicgames.com/store/",
        "origin": "https://www.origin.com/",
    },

    # Finance & Stocks
    "finance": {
        "yahoo_finance": "https://finance.yahoo.com/",
        "nasdaq": "https://www.nasdaq.com/",
        "moneycontrol": "https://www.moneycontrol.com/",
        "bankrate": "https://www.bankrate.com/",
    }
}

# Register Chrome as the browser and set it as the default for web operations
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


def open_application(app_name):
    app_name = app_name.lower()

    # Check if it's an installed app first
    if app_name in apps:
        try:
            os.startfile(apps[app_name])
            speak(f"Opening {app_name}.")
        except FileNotFoundError:
            speak(f"Couldn't find {app_name}.")
    # Check if it's a web app by searching through categories
    elif any(app_name in category for category in web_apps.values()):
        # Search through categories
        for category, apps_in_category in web_apps.items():
            if app_name in apps_in_category:
                # Give category-based feedback
                if category == "social_media":
                    speak(f"Opening Social Media: {app_name}.")
                elif category == "video_streaming":
                    speak(f"Opening Video Streaming Site: {app_name}.")
                elif category == "e_commerce":
                    speak(f"Opening E-commerce site: {app_name}.")
                elif category == "news":
                    speak(f"Opening News website: {app_name}.")
                elif category == "communication":
                    speak(f"Opening Communication tool: {app_name}.")
                elif category == "productivity":
                    speak(f"Opening Productivity tool: {app_name}.")
                elif category == "tech_tools":
                    speak(f"Opening Tech tool: {app_name}.")
                elif category == "learning":
                    speak(f"Opening Learning resource: {app_name}.")
                elif category == "entertainment":
                    speak(f"Opening Entertainment website: {app_name}.")
                elif category == "finance":
                    speak(f"Opening Finance website: {app_name}.")

                webbrowser.get('chrome').open(apps_in_category[app_name])
                return
    # Google search functionality
    elif "search for" in app_name:
        query = app_name.replace("search for", "").strip()
        speak(f"Opening Google and searching for {query}.")
        webbrowser.get('chrome').open(f"https://www.google.com/search?q={query}")
    # Handle typo and smart suggestions
    else:
        # Get close matches from the available apps and websites
        all_apps = list(apps.keys()) + [app for category in web_apps.values() for app in category.keys()]
        suggestions = difflib.get_close_matches(app_name, all_apps, n=3, cutoff=0.6)
        if suggestions:
            speak(f"Did you mean one of these? {', '.join(suggestions)}")
        else:
            speak(f"Sorry Pal, I don't know how to open {app_name}.")
