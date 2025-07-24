import os
import requests
import webbrowser
import speech_recognition as sr
import pyttsx3
import random
from datetime import datetime

Assistant_name = "Morty"

# Initialize the text-to-speech engine
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    print(f"{Assistant_name}: {text}")
    engine.say(text)
    engine.runAndWait()
# Function => to take voice commands from the user
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Processing...")
        command = r.recognize_google(audio, language='en-in').lower()
        print(f"User: {command}")
        return command
    
    except Exception as e:
        response = [
            "Yoh! My guy, I can't hear you, please repeat!",
            "I didn't understand, please repeat.",
            "Yoh! my ears ain't working. Say that again?",
            "Brah, what'd you say? I ain't hearin' nothin', repeat that!",
            "I missed that, can you say it again?",
            "Yoh! what was that? My brain lagged.",
            "My bad, I buffered. Can you say that again?"
        ]
        speak(random.choice(response))
        return ""


def check_weather(city):
    api_key = "7cb4fa203094ccbe0ebb6a0fa5f78d16"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(complete_url)
        data = response.json()
        temp = data['main']['temp']
        weather = data['weather'][0]['description']
        speak(f"Current weather in {city} is {weather} with temperatures {temp}°C")

    except:
        speak("Couldn't fetch weather data! Please check the city name or try again later.")


def main():

    greetings = [
        f"Hi, I'm {Assistant_name} your Desktop assistant. How can I help you?",
        f"Hello! I'm {Assistant_name}, ready to assist you!",
        f"Hey there! I'm {Assistant_name}, what can I do for you today?",
        f"Greetings and salutations! I'm {Assistant_name}, how may I help you?",
        f"Hi! I'm {Assistant_name}, your desktop assistant is online."
    ]
    speak(random.choice(greetings))

    while True:
        command = take_command()

        if not command:
            continue

        if "exit" in command or "quit" in command or "stop" in command:
            farewell_messages = [
                "Goodbye, and have a nice day.",
                "See you later! Take care.",
                "Farewell! Until next time.",
                "Catch you later! Stay safe."
            ]
            speak(random.choice(farewell_messages))
            break
        elif "hello" in command or "hi" in command or "hey" in command or "greetings" in command or "wassup" in command or "sup" in command:
            greetings = [
                "Hello! How can I assist you today?",
                "Hi! Your assistant is online.",
                "Sup bro, what's the move? Your assistant is locked in.",
                "Wassup, we're officially in our assistant era. Let's get this bread."
            ]
            speak(random.choice(greetings))
        elif "time" in command:
            current_time = datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {current_time}")
        elif "weather" in command:
            speak("Which city am I checking the weather?")
            city = take_command()
            if city:
                check_weather(city)
        elif "open" in command:
            if "browser" in command:
                webbrowser.open("https://www.google.com")
                speak("Opening browser")
            elif "file explorer" in command:
                os.startfile(os.path.expanduser("~\\Desktop"))
                speak("Opening explorer")
            elif "notepad" in command:
                os.startfile(os.path.join(os.environ['SystemRoot'], 'system32', 'notepad.exe'))
                speak("Opening Notepad")
            elif "spotify" in command:
                os.startfile("C:\\Users\\ADMIN\\AppData\\Roaming\\Spotify\\Spotify.exe")
                speak("Opening Spotify")
            else:
                speak("I can only open browser, file explorer, or notepad for know.")
                
if __name__ == "__main__":
    main()
