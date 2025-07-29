# 🤖 Smart Helper Voice Assistant

Smart Helper is a Python-based desktop **voice assistant** that listens to voice commands, processes them using AI (OpenAI & Google Gemini), and performs various tasks like fetching weather, reading news, opening applications, and more — all through an interactive **GUI interface built with Tkinter**.

---

## 📌 Features

- 🎤 **Voice Recognition** – Convert spoken input to text using Google Speech Recognition.
- 🧠 **AI Chatbot Integration** – Uses OpenAI's GPT and Google Gemini APIs for intelligent conversations.
- 📰 **News Updates** – Fetch latest headlines and articles using NewsAPI.
- 🌤️ **Weather Reports** – Get real-time weather data from WeatherAPI.
- 🗣️ **Text-to-Speech** – Responses are spoken aloud using `pyttsx3`.
- 🖥️ **Application Control** – Open or close system apps like Notepad, Calculator, Media Player.
- ⏯️ **Pause/Resume Assistant** – Supports both GUI buttons and voice commands to pause or resume.
- 📅 **Date Inquiry** – Provides current date on request.
- 🗃️ **Command Logging** – Stores user commands and responses in a local database.
- 🖼️ **Tkinter GUI** – Sleek, scrollable response window with control buttons (Start, Pause, Resume).

---

## 🔧 Technologies Used

| Category       | Tools / Libraries                      |
|----------------|----------------------------------------|
| Language       | Python 3.x                             |
| GUI            | Tkinter                                |
| AI/LLM         | Google Gemini                          |
| Speech         | `speech_recognition`, `pyttsx3`        |
| APIs           | WeatherAPI, NewsAPI                    |
| Network        | `requests`                             |
| Threads        | `threading`                            |
| Data Storage   | SQLite (via custom `database.py`)      |

---

## 🚀 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/smart-helper.git
cd smart-helper
