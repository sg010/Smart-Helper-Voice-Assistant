import os
import openai
import pyttsx3
import requests
import speech_recognition as sr
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
import google.generativeai as genai
from datetime import datetime
import sys
import webbrowser
from newsapi import NewsApiClient
from config import apikey, weather_api_key  # Replace with your actual API keys
from database import insert_command, insert_response, get_last_command



# Global variables
chatStr = ""  # Chat history
listening_thread = None
is_paused = False  # Flag to control pause state


api_key = "e652956fe70548d2b5b85d07348800b4"  # Replace with your actual NewsAPI key
newsapi = NewsApiClient(api_key=api_key)

# Configure the Generative AI API
genai.configure(api_key="AIzaSyDi1bkSkJ9YDXRycdvpXemeI2RwernKNhI")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize the speech engine
engine = pyttsx3.init()

# GUI Setup
root = tk.Tk()
root.title("Smart Helper")
root.geometry("700x550")
root.attributes("-alpha", 0.9)  # 90% opacity



# Apply Styles
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Arial", 12), padding=8, relief="flat", background="#1F1F1F", foreground="white")

style.configure("TButton", font=("Arial", 12), padding=8, relief="flat", background="#1F1F1F", foreground="white")
style.configure("TLabel", font=("Arial", 14), background="#121212", foreground="white")
style.configure("TFrame", background="#121212")

# Create a text box to display responses
response_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=25, width=100, font=("Arial", 12), bg="#1F1F1F", fg="white", insertbackground="white")
response_box.pack(padx=10, pady=10)
response_box.pack(padx=10, pady=10)



def say(text):
    """Convert text to speech using pyttsx3 (Windows-compatible)."""
    engine.say(text)         # Convert text to speech
    engine.runAndWait()      # Wait for the speech to finish

def takeCommand():
    """Take voice input from the user."""
    global is_paused
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
            print(f"Error: ")
            return "Some Error Occurred. Sorry from Jarvis"

def update_response_box(text):
    """Update the GUI text box with the response."""
    response_box.insert(tk.END, f"S_Helper: {text}\n\n")
    response_box.yview(tk.END)

def pause_assistant():
    """Pause the assistant (stop listening)."""
    global is_paused
    is_paused = True
    update_response_box("Voice Assistant Paused.")
    print("Voice Assistant Paused.")
    
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
        update_response_box(weather_info)
        return weather_info
    except requests.exceptions.RequestException as e:
        error_msg = f"An error occurred while fetching weather data: "
        say(error_msg)
        update_response_box(error_msg)
        return error_msg
    except KeyError:
        error_msg = "Invalid data received from the Weather API. Please check the city name or API key."
        say(error_msg)
        update_response_box(error_msg)
        return error_msg

def chat_with_ai(prompt):
    """Get a response from Google Generative AI."""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"An error occurred while generating the response: "

def chat(query):
    """Chat function to interact with OpenAI."""
    global chatStr
    openai.api_key = apikey
    chatStr += f"User: {query}\nS_Helper: "
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
        update_response_box(response_text)
        return response_text
    except Exception as e:
        error_msg = f"An error occurred: "
        say(error_msg)
        update_response_box(error_msg)
        return error_msg

def fetch_top_headlines():
    """Fetch top headlines and speak them out."""
    try:
        top_headlines = newsapi.get_top_headlines(
            language='en',
            country='us'
        )
        if top_headlines["articles"]:
            for i, article in enumerate(top_headlines["articles"][:5], start=1):  # Limit to 5 headlines
                headline = f"Headline {i}: {article['title']}"
                say(headline)
                update_response_box(headline)
        else:
            msg = "No headlines available at the moment."
            say(msg)
            update_response_box(msg)
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        say(error_msg)
        update_response_box(error_msg)

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
                update_response_box(f"Article {i}: {article['title']}")
        else:
            say(f"No articles found about {query}.")
            print(f"No articles found about {query}.")
    except Exception as e:
        error_msg = f"An error occurred: "
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
                update_response_box(f"{i}. {source['name']} - {source['country']}")

        else:
            say("No sources available at the moment.")
            print("No sources available.")
    except Exception as e:
        error_msg = f"An error occurred: "
        say(error_msg)
        print(error_msg)

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

def handle_commands():
    print("Welcome to Smart Helper Voice Assistant !")
    say("Welcome to Smart Helper Voice Assistant Created by Mister Suraj Gawade !")
    update_response_box("Welcome to Smart Helper Voice Assistant !")
    
    while True:
        query = takeCommand().lower()

        # Insert command into DB and get the command ID
        command_id = insert_command(query)

        response_text = ""

        if "hello" in query:
            response_text = "Hello! How can I assist you?"

        elif "weather in" in query:
            city = query.split("in")[-1].strip()
            response_text = getWeather(city)

        elif "date" in query:
            response_text = datetime.now().strftime("%A, %d %B %Y")

        elif "headlines" in query:
            fetch_top_headlines()
            response_text = "Here are the top headlines."

        elif "articles about" in query:
            topic = query.replace("articles about", "").strip()
            response_text = fetch_all_articles(topic)

        elif "news sources" in query:
            fetch_sources()
            response_text = "Here are some available news sources."

        elif "open calculator" in query:
            os.system("calc")
            response_text = "Opening Calculator."

        elif "close calculator" in query:
            closeCalculator()
            response_text = "Calculator has been closed."

        elif "open notepad" in query:
            os.system("notepad")
            response_text = "Opening Notepad."

        elif "close notepad" in query:
            closeNotepad()
            response_text = "Notepad has been closed."

        elif "open music" in query:
            os.system("mediaplayer")
            response_text = "Opening Music."

        elif "close music player" in query:
            closeMusicPlayer()
            response_text = "Music player has been closed."

        # Check for pause command
        elif "pause assistant" in query:
            pause_assistant()
            say("Assistant Pause !")
            return ""

        elif "quit" in query or "stop" in query:
            response_text = "Goodbye! Have a great day! Shutting down."
            say(response_text)
            update_response_box(response_text)

            # Store the final response before exiting
            insert_response(command_id, response_text)
            on_close()
            break

        else:
            response_text = chat_with_ai(query)

        # Store and display response
        say(response_text)
        update_response_box(response_text)
        insert_response(command_id, response_text)  # Save response to DB


def start_listening():
    """Start listening to commands in the background."""
    listening_thread = threading.Thread(target=handle_commands)
    listening_thread.daemon = True
    listening_thread.start()

def stop_listening():
    """Stop listening thread"""
    global listening_thread
    if listening_thread:
        listening_thread.join()

def on_close():
    """Handle window close"""
    stop_listening()
    root.quit()


# Button to start listening
start_button = tk.Button(root, text="Start Listening", command=start_listening)
start_button.pack(pady=10)

# Start the GUI event loop

root.mainloop()
