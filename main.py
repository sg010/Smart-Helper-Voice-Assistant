import os
import openai
import webbrowser
import pyttsx3
import requests
import speech_recognition as sr
import google.generativeai as genai
from datetime import datetime
import sys
from newsapi import NewsApiClient
from config import apikey, weather_api_key  # Replace with your actual API keys


# Global variables
chatStr = ""  # Chat history

api_key = "e652956fe70548d2b5b85d07348800bu4"  # Replace with your actual NewsAPI key
newsapi = NewsApiClient(api_key=api_key)

# Configure the Generative AI API
genai.configure(api_key="AIzaSyDi1bkSkJ9YDuXRycdvpXemeI2RwernKNhI")
model = genai.GenerativeModel("gemini-1.5-flash")

def say(text):
    """Convert text to speech using pyttsx3 (Windows-compatible)."""
    engine = pyttsx3.init()  # Initialize the pyttsx3 engine
    engine.say(text)         # Convert text to speech
    engine.runAndWait()      # Wait for the speech to finish


def takeCommand():
    """Take voice input from the user."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(f"Error: {e}")
            return "Some Error Occurred. Sorry from Jarvis"


def getWeather(city):
    """Fetch the weather details from the Weather API."""
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract weather details
        location = data["location"]["name"]
        region = data["location"]["region"]
        country = data["location"]["country"]
        temperature = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        feels_like = data["current"]["feelslike_c"]
        humidity = data["current"]["humidity"]

        weather_info = (
            f"Weather in {location}, {region}, {country}:\n"
            f"- Condition: {condition}\n"
            f"- Temperature: {temperature}°C\n"
            f"- Feels Like: {feels_like}°C\n"
            f"- Humidity: {humidity}%"
        )
        say(weather_info)
        return weather_info
    except requests.exceptions.RequestException as e:
        error_msg = f"An error occurred while fetching weather data: {e}"
        say(error_msg)
        return error_msg
    except KeyError:
        error_msg = "Invalid data received from the Weather API. Please check the city name or API key."
        say(error_msg)
        return error_msg

def chat_with_ai(prompt):
    """Get a response from Google Generative AI."""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"An error occurred while generating the response: {e}"

def chat(query):
    """Chat function to interact with OpenAI."""
    global chatStr
    openai.api_key = apikey
    chatStr += f"User: {query}\nJarvis: "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response_text = response["choices"][0]["text"].strip()
        chatStr += response_text + "\n"
        say(response_text)
        return response_text
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        say(error_msg)
        return error_msg

def fetch_top_headlines():
    """Fetch top headlines and speak them out."""
    try:
        top_headlines = newsapi.get_top_headlines(
            language='en',
            country='us'
        )
        if top_headlines["articles"]:
            say("Here are the top headlines:")
            for i, article in enumerate(top_headlines["articles"][:5], start=1):  # Limit to 5 headlines
                say(f"Headline {i}: {article['title']}")
                print(f"Headline {i}: {article['title']}")
        else:
            say("No headlines available at the moment.")
            print("No headlines available.")
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        say(error_msg)
        print(error_msg)

def fetch_all_articles(query):
    """Fetch articles related to a specific query and speak them out."""
    try:
        all_articles = newsapi.get_everything(
            q=query,
            language='en',
            sort_by='relevancy',
            page=1
        )
        if all_articles["articles"]:
            say(f"Here are the top articles about {query}:")
            for i, article in enumerate(all_articles["articles"][:5], start=1):  # Limit to 5 articles
                say(f"Article {i}: {article['title']}")
                print(f"Article {i}: {article['title']}")
        else:
            say(f"No articles found about {query}.")
            print(f"No articles found about {query}.")
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        say(error_msg)
        print(error_msg)

def fetch_sources():
    """Fetch available news sources and speak them out."""
    try:
        sources = newsapi.get_sources(language='en')
        if sources["sources"]:
            say("Here are some available news sources:")
            for i, source in enumerate(sources["sources"][:10], start=1):  # Limit to 10 sources
                say(f"{i}. {source['name']} from {source['country']}")
                print(f"{i}. {source['name']} - {source['country']}")
        else:
            say("No sources available at the moment.")
            print("No sources available.")
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        say(error_msg)
        print(error_msg)

def get_date():
    return datetime.now().strftime("%A, %d %B %Y")

def closeMusicPlayer():
    """Closes the music player by terminating its process."""
    process_name = "Microsoft.Media.Player.exe"  # Process name for Windows Media Player
    try:
        # Use taskkill to terminate the process
        result = os.system(f'taskkill /f /im {process_name}')
        if result == 0:
            print(f"{process_name} has been successfully closed.")
        else:
            print(f"Failed to close {process_name}. It might not be running.")
    except Exception as e:
        print(f"An error occurred while closing the music player: {e}")

def closeCalculator():
    """Closes the music player by terminating its process."""
    process_name = "CalculatorApp.exe"  # Process name for Windows Media Player
    try:
        # Use taskkill to terminate the process
        result = os.system(f'taskkill /f /im {process_name}')
        if result == 0:
            print(f"{process_name} has been successfully closed.")
        else:
            print(f"Failed to close {process_name}. It might not be running.")
    except Exception as e:
        print(f"An error occurred while closing the calculator: {e}")

def closeNotepad():
    """Closes the music player by terminating its process."""
    process_name = "notepad.exe"  # Process name for Windows Media Player
    try:
        # Use taskkill to terminate the process
        result = os.system(f'taskkill /f /im {process_name}')
        if result == 0:
            print(f"{process_name} has been successfully closed.")
        else:
            print(f"Failed to close {process_name}. It might not be running.")
    except Exception as e:
        print(f"An error occurred while closing the notepad: {e}")

if __name__ == "__main__":
    print("Welcome to Jarvis A.I")
    say("Welcome to Jarvis A.I")
    while True:
        query = takeCommand().lower()

        sites = [["youtube", "https://www.youtube.com"],
                 ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if "reset chat" in query:
            chatStr = ""
            say("Chat history has been reset.")
            print("Chat history has been reset.")

        elif "hello" in query:
            say("hello, sir! How Can I Help You.")

        elif "date" in query:
            date= get_date()
            print(get_date())
            say(date)

        elif "weather in" in query:
            city = query.split("in")[-1].strip()  # Extract the city name from the query
            weather_details = getWeather(city)  # Fetch weather details using get_weather function
            print(weather_details) # Print details to the console
            say(weather_details)  # Speak the weather details

        elif "headlines" in query:
            fetch_top_headlines()

        elif "articles about" in query:
            topic = query.replace("articles about", "").strip()
            fetch_all_articles(topic)

        elif "news sources" in query:
            fetch_sources()

        elif "open calculator" in query:
            os.system("calc")
            say("Opening Calculator.")

        elif "close calculator" in query:
            closeCalculator()
            say("Calculator has been closed.")

        elif "open notepad" in query:
            os.system("notepad")
            say("Opening Notepad.")

        elif "close notepad" in query:
            closeNotepad()
            say("Notepad has been closed")

        elif "open music" in query:
            os.system("mediaplayer")
            say("opening Music Music.")

        elif "close music player" in query:
            closeMusicPlayer()
            say("Music player has been closed.")

        elif "quit" in query or "stop" in query:
            say("Goodbye, Sir! Have a great day! Shutting down.")
            print("Shutting down.")
            sys.exit()

        else:
            response = chat_with_ai(query)
            say(response)
            print(response)

