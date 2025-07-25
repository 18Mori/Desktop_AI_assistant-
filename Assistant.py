import os
import requests
import webbrowser
import speech_recognition as sr
import pyttsx3
import random
from datetime import datetime
import pyautogui
import time
import shutil

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
        r.pause_threshold = 1.4
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
def manage_files(action, *paths):
    try:
        if "create folder" in action:
            os.makedirs(paths[0])
            speak(f"Folder '{os.path.basename(paths[0])}' created.")
        elif "delete folder" in action:
            shutil.rmtree(paths[0])
            speak(f"Folder '{os.path.basename(paths[0])}' deleted.")
        elif "create file" in action:
            open(paths[0], 'w').close()
            speak(f"File '{os.path.basename(paths[0])}' created.")
        elif "delete file" in action:
            os.remove(paths[0])
            speak(f"File '{os.path.basename(paths[0])}' deleted.")


        elif "open folder" in action:
            os.startfile(paths[0])
            speak(f"Opening folder...")
            speak(f"Name: {os.path.basename(paths[0])}.")

        elif "open file" in action:
                os.startfile(paths[0])
                speak(f"Opening file...")
                speak(f"Name: {os.path.basename(paths[0])}.")


        elif "rename folder" in action:
            old_name = os.path.basename(paths[0])
            os.rename(paths[0], paths[1])
            speak(f"Renamed folder '{old_name}' to '{os.path.basename(paths[1])}'.")
        elif "rename file" in action:
            old_name = os.path.basename(paths[0])
            os.rename(paths[0], paths[1])
            speak(f"Renamed file '{old_name}' to '{os.path.basename(paths[1])}'.")
        elif "copy folder" in action:
            shutil.copytree (paths[0], paths[1])
            speak(f"Copied folder '{old_name}' to '{paths[1]}'.")
        elif "copy file" in action:
            shutil.copy(paths[0], paths[1])
            speak(f"Copied file '{old_name}' to '{paths[1]}'.")
        elif "move folder" in action:
            shutil.move(paths[0], paths[1])
            speak(f"Moved folder '{old_name}' to '{paths[1]}'.")
        elif "move file" in action:
            shutil.move(paths[0], paths[1])
            speak(f"Moved file '{old_name}' to '{paths[1]}'.")
    except FileNotFoundError:
        speak("Error: The file or folder was not found.")
    except FileExistsError:
        speak("Error: A file or folder with that name already exists.")
        
    except Exception as e:
        speak(f"Error: {str(e)}")

def main():
    greetings = [
        f"Hi, I'm {Assistant_name} your Desktop assistant. How can I help you?",
        f"Hello! I'm {Assistant_name}, ready to assist you!",
        f"Hi, I'm {Assistant_name}, your personal assistant. How can I help you?",
        f"Hello! I'm {Assistant_name}, how may I help you?",
        f"Hey there! I'm {Assistant_name}, what can I do for you today?"
    ]
    speak(random.choice(greetings))

    while True:
        command = take_command()

        if not command:
            continue

        if "exit" in command or "quit" in command or "stop" in command or "that is all" in command:
            farewell_messages = [
                "Have a nice day, sir",
                "See you later! Sir.",
                "Until next time.",
                "Catch you later!"
            ]
            speak(random.choice(farewell_messages))
            break
        elif "hello" in command or "hi" in command or "hey" in command or "greetings" in command or "what's up" in command:
            greetings = [
                "Hello! How can I assist you today?",
                "Sup bro, what's the move?",
                "Hello, Sir! Your assistant is locked in.",
                "Wassup, we're officially in our assistant era. Let's get this bread."
            ]
            speak(random.choice(greetings))
                
        elif "time" in command:
            current_time = datetime.now().strftime("%H:%M")
            speak(f"The current time is {current_time}")
        elif "weather" in command:
            speak("Which city am I checking the weather?")
            city = take_command()
            if city:
                check_weather(city)

        elif "date" in command:
            current_date = datetime.now().strftime("%Y-%m-%d")
            speak(f"Today's date is {current_date}")


        # File management
        elif "create folder" in command:
            speak("Folder name?")
            path = take_command().replace(" ", "_")
            manage_files("create folder", path)

        elif "open folder" in command:
            speak("Which folder should I open?")
            path = take_command().replace(" ", "_")
            if os.path.isdir(path):
                manage_files("open folder", path)
            else:
                speak(f"Folder {path} does not exist.")
        elif "open file" in command:
            speak("Which file should I open?")
            path = take_command().replace(" ", "_") + ".txt"
            if os.path.isfile(path):
                manage_files("open file", path)
            else:
                speak(f"File {path} does not exist.")
        # Creating files
        elif "create file" in command:
            speak("File name?")
            path = take_command().replace(" ", "_") + ".txt"
            manage_files("create file", path)
        # Deleting folders
        elif "delete folder" in command:
            speak("Which folder should I delete?")
            path = take_command().replace(" ", "_")
            if os.path.isdir(path):
                manage_files("delete folder", path)
            else:
                speak(f"Folder {path} does not exist.")
        # Deleting files
        elif "delete file" in command:
            speak("Which file should I delete?")
            path = take_command().replace(" ", "_") + ".txt"
            
            if os.path.isfile(path):
                manage_files("delete file", path)
            else:
                speak(f"File {path} does not exist.")
        # Copying files
        elif "copy file" in command:
            speak("What is the file name to copy?")
            source_path = take_command().replace(" ", "_") + ".txt"
            if not os.path.isfile(source_path):
                speak(f"File '{source_path}' does not exist.")
                continue

            speak("Where should I copy it to? Please specify the destination folder.")
            dest_folder = take_command().replace(" ", "_")
            if not os.path.isdir(dest_folder):
                speak(f"Destination folder '{dest_folder}' does not exist or is not a directory.")
                continue
            manage_files("copy file", source_path, dest_folder)
        # Copying folders
        elif "copy folder" in command:
            speak("What is the folder name to copy?")
            source_path = take_command().replace(" ", "_")
            if not os.path.isdir(source_path):
                speak(f"Folder '{source_path}' does not exist.")
                continue

            speak("Where should I copy it to? Please specify the destination folder.")
            dest_folder = take_command().replace(" ", "_")
            if not os.path.isdir(dest_folder):
                speak(f"Destination folder '{dest_folder}' does not exist or is not a directory.")
                continue
            manage_files("copy folder", source_path, dest_folder)
        # Renaming files
        elif "rename file" in command:
            speak("What is the current file name, to rename?")
            old_path = take_command().replace(" ", "_") + ".txt"
        
            if not os.path.isfile(old_path):
                speak(f"File {old_path} is not found.")
                continue

            speak(f"What should I rename it to?")
            new_path = take_command().replace(" ", "_") + ".txt"
            if os.path.exists(new_path):
                speak(f"A file or folder named '{new_path}' already exists. Please choose a different name.")
                continue
            manage_files("rename file", old_path, new_path)
        # Renaming folders
        elif "rename folder" in command:
            speak("What is the current folder name, to rename?")
            old_path = take_command().replace(" ", "_")
        
            if not os.path.isdir(old_path):
                speak(f"Folder {old_path} is not found.")
                continue

            speak(f"What should I rename it to?")
            new_path = take_command().replace(" ", "_")
            if os.path.exists(new_path):
                speak(f"A file or folder named '{new_path}' already exists. Please choose a different name.")
                continue
            manage_files("rename folder", old_path, new_path)
        # Moving files
        elif "move file" in command:
            speak("What is the file name to move?")
            source_path = take_command().replace(" ", "_") + ".txt"
            if not os.path.isfile(source_path):
                speak(f"{source_path} is not found")
                continue
            speak("Where should I move it to? Please specify the destination of folder.")
            dest_folder = take_command().replace(" ", "_")
            if not os.path.isdir(dest_folder):
                speak(f"Destination folder {dest_folder} is not found or not a destination.")
                continue
            manage_files("move file", source_path, dest_folder)
        # Moving folders
        elif "move folder" in command:
            speak("What is the folder name, to move?")
            source_path = take_command().replace(" ", "_")
            if not os.path.isdir(source_path):
                speak(f"{source_path} is not found")
                continue
            speak("Where should I move it to? Please specify it's destination.")
            dest_folder = take_command().replace(" ", "_")
            if not os.path.isdir(dest_folder):
                speak(f"Destination folder {dest_folder} is not found or not a destination.")
                continue
            manage_files("move folder", source_path, dest_folder)


        elif "search" in command:
            if "on youtube" in command:
                speak("What do you want to search on YouTube?")
                query = take_command()
                if query:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                    speak(f"Searching for {query} on YouTube")
                    query = take_command()

            else:
                speak("What do you want to search for?")
                query = take_command()
                if query:
                    webbrowser.open(f"https://www.google.com/search?q={query}")
                    speak(f"Searching for {query} on Google")
            
        elif "open" in command:
            if "file explorer" in command:
                os.startfile(os.path.expanduser("~\\Desktop"))
                speak("Opening explorer")
            elif "notepad" in command:
                os.startfile(os.path.join(os.environ['SystemRoot'], 'system32', 'notepad.exe'))
                speak("Opening Notepad")
            elif "spotify" in command:
                os.startfile("C:\\Users\\ADMIN\\AppData\\Roaming\\Spotify\\Spotify.exe")
                speak("Opening Spotify")
                if "play" in command:
                    pyautogui.press("playpause")
                    time.sleep(3)
                    speak("Playing music on Spotify")
                elif "pause" in command:
                    time.sleep(3)
                    pyautogui.press("playpause")
                    speak("Paused music on Spotify")
            else:
                speak("I can only open browser, file explorer, or notepad for know.")
                
if __name__ == "__main__":
    main()
