import requests

API_KEY = "98a9405cce908733a8f87bbecf299694"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            weather = data['weather'][0]['description']
            temperature = data['main']['temp']
            feels_like = data['main']['feels_like']
            return f"The weather in {city} is {weather} with a temperature of {temperature}°C, feels like {feels_like}°C."
        else:
            return f"Couldn't fetch weather info for {city}. Please try another city."
    except Exception as e:
        return "Sorry pal, couldn't connect to the weather service."
