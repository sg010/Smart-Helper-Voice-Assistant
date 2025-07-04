import requests
from config import weather_api_key  # Ensure the API key is stored in config.py


def get_weather(city):
    # Correct API endpoint
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no"

    try:
        # Send GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise error for HTTP issues
        data = response.json()

        # Extract weather details
        location = data["location"]["name"]
        region = data["location"]["region"]
        country = data["location"]["country"]
        temperature = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        feels_like = data["current"]["feelslike_c"]

        # Format output
        weather_info = (
            f"Weather in {location}, {region}, {country}:\n"
            f"- Condition: {condition}\n"
            f"- Temperature: {temperature}°C\n"
            f"- Feels Like: {feels_like}°C\n"
            f"- Humidity: {humidity}%"
        )
        return weather_info

    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching weather data: {e}"
    except KeyError as e:
        return "Invalid data received from WeatherAPI. Check the city name or API key."


if __name__ == "__main__":
    city = input("Enter the city name to check the weather: ").strip()
    weather_details = get_weather(city)
    print(weather_details)
