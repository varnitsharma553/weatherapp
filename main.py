from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
import requests
from datetime import datetime

API_KEY = "7c25863428d4d231e2d6ca18911d4581"

class WeatherLayout(BoxLayout):
    weather_text = StringProperty("Enter a city name")
    background_image = StringProperty("bg.jpg")

    def get_weather(self):
        city = self.ids.city_input.text.strip()

        if not city:
            self.weather_text = "❌ Please enter a city name"
            return

        try:
            weather_url = (
                f"https://api.openweathermap.org/data/2.5/weather"
                f"?q={city}&appid={API_KEY}&units=metric"
            )

            data = requests.get(weather_url).json()

            if data.get("cod") != 200:
                self.weather_text = "❌ City not found"
                return

            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            temp_min = data["main"]["temp_min"]
            temp_max = data["main"]["temp_max"]

            humidity = data["main"]["humidity"]
            weather = data["weather"][0]["description"]
            if "rain" in weather.lower():
                self.background_image = "rain.jpg"
            elif "cloud" in weather.lower():
                self.background_image = "cloudy.jpg"
            elif "clear" in weather.lower():
                self.background_image = "sun.jpg"
            elif "snow" in weather.lower():
                self.background_image = "snow.jpg"
            else:
                self.background_image = "bg.jpg"

            rain = data.get("rain", {}).get("1h", 0)

            sunrise = datetime.fromtimestamp(
                data["sys"]["sunrise"]
            ).strftime("%H:%M:%S")

            sunset = datetime.fromtimestamp(
                data["sys"]["sunset"]
            ).strftime("%H:%M:%S")

            if "thunderstorm" in weather.lower():
                icon = "⛈️"
            elif "rain" in weather.lower():
                icon = "🌧️"
            elif "snow" in weather.lower():
                icon = "❄️"
            elif "cloud" in weather.lower():
                icon = "☁️"
            elif "clear" in weather.lower():
                icon = "☀️"
            else:
                icon = "🌤️"
            wind_speed = data["wind"]["speed"]
            wind_deg = data["wind"].get("deg", 0)

            visibility = data.get("visibility", 0) / 1000
            country = data["sys"]["country"]

            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]

            aqi_url = (
                f"https://api.openweathermap.org/data/2.5/air_pollution"
                f"?lat={lat}&lon={lon}&appid={API_KEY}"
            )

            aqi_data = requests.get(aqi_url).json()

            aqi = aqi_data["list"][0]["main"]["aqi"]

            aqi_status = {
                1: "Good 😀",
                2: "Fair 🙂",
                3: "Moderate 😐",
                4: "Poor 😷",
                5: "Very Poor 🤢"
            }.get(aqi, "Unknown")

            current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            self.weather_text = f"""
 {current_time}

City: {city}
Country: {country}

Temperature: {temp} °C
Feels Like: {feels_like} °C
Min Temp: {temp_min} °C
Max Temp: {temp_max} °C

Humidity: {humidity}%

Wind Speed: {wind_speed} m/s
Wind Direction: {wind_deg}°

Visibility: {visibility} km

Rain (1h): {rain} mm

AQI: {aqi}
Air Quality: {aqi_status}

Sunrise: {sunrise}
Sunset: {sunset}

Condition:
{icon} {weather}
"""


        except Exception as e:
            self.weather_text = f"❌ Error:\n{e}"

class WeatherApp(App):
    def build(self):
        return WeatherLayout()

WeatherApp().run()