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
import psutil
import hashlib

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
    # confirming for folder deletion
    def confirmation_act1():
        speak(f"Are you sure you want to delete '{os.path.basename(paths[0])}'? (yes/no)")
        confirmation = take_command().lower()
        return "yes" in confirmation.lower()
    # confirmation for file deletion
    def confirmation_act2(path):
        speak(f"Are you sure you want to delete '{os.path.basename(path)}'? (yes/no)")
        confirmation = take_command().lower()
        return "yes" in confirmation.lower()
        
    
    try:
        if "create folder" in action:
            speak(f"Folder '{os.path.basename(paths[0])}' created.")
            os.makedirs(paths[0])
        elif "delete folder" in action:
            if not confirmation_act1():
                speak("Folder deletion cancelled.")
                return
            shutil.rmtree(paths[0])
            speak(f"Folder '{os.path.basename(paths[0])}' deleted.")
            
        elif "create file" in action:
            open(paths[0], 'w').close()
            speak(f"File '{os.path.basename(paths[0])}' created.")
        elif "delete file" in action:
            speak(f"File '{os.path.basename(paths[0])}' deleted.")
            os.remove(paths[0])
            if not confirmation_act2("file", paths[0]):
                speak("File deletion cancelled.")
                return


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

def system_monitor():
    cpu_usage = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    ram_usage = ram.percent

    status = f"\rCPU Usage: {cpu_usage}%, RAM Usage: {ram_usage}%"
    if cpu_usage > 80 or ram_usage > 80:
        status = "WARNING! "+ status
        speak(status)
    
def take_screenshot():
    timespent = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timespent}.png"
    pyautogui.screenshot(filename)
    speak(f"Screenshot taken as {filename}")

def _calculate_hash(filepath, chunk_size=8192):
    # Helper function to calculate SHA256 hash of a file
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    except (IOError, OSError):
        # Could be a permissions error or file disappeared during scan
        return None

def find_duplicate_files(directory):
    if not os.path.isdir(directory):
        speak(f"Error!!: The directory '{directory}' does not exist.")
        return

    speak(f"Scanning for duplicate files...")
    print(f"in '{directory}'")
    speak("This may take a moment...")
    hashes = {}
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_hash = _calculate_hash(filepath)
            if file_hash:
                if file_hash in hashes:
                    hashes[file_hash].append(filepath)
                else:
                    hashes[file_hash] = [filepath]

    duplicates = {k: v for k, v in hashes.items() if len(v) > 1}
    
    if not duplicates:
        speak("No duplicate files found.")
    else:
        speak(f"Found {len(duplicates)} sets of duplicate files.")
        for i, (file_list) in enumerate(duplicates.values()):
            speak(f"Set {i + 1}:")
            for f_path in file_list:
                speak(f"  - {os.path.basename(f_path)}")
                print(f"located in {os.path.dirname(f_path)}")
    speak("Scan complete.")

def find_large_files(directory, min_size_mb=100):
    if not os.path.isdir(directory):
        speak(f"Error!!: The directory '{directory}' does not exist.")
        return

    speak(f"Scanning for files larger than {min_size_mb} MB in '{directory}'...")
    large_files = []
    min_size_bytes = min_size_mb * 1024 * 1024
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                file_size = os.path.getsize(filepath)
                if file_size > min_size_bytes:
                    large_files.append((filepath, file_size / (1024 * 1024)))
            except (IOError, OSError):
                continue
    
    if not large_files:
        speak(f"No files larger than {min_size_mb} MB found.")
    else:
        speak(f"Found {len(large_files)} files larger than {min_size_mb} MB.")
        large_files.sort(key=lambda x: x[1], reverse=True)
        for f_path, f_size_mb in large_files:
            speak(f"  - {os.path.basename(f_path)} - {f_size_mb:.2f} MB")
    speak("Scan complete.")

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
                "Hello, locked in, Sir.",
                "Hey there! What can I do for you?"
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

        elif "system monitor" in command or "system status" in command:
            speak("Checking system status...")
            system_monitor()
            speak("System status check, complete.")

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
        # Calculator and system commands
        elif "calculator" in command:
            os.startfile(os.path.join(os.environ['SystemRoot'], 'system32', 'calc.exe'))
            speak("Opening Calculator")
        elif "command prompt" in command or "cmd" in command:
            os.startfile(os.path.join(os.environ['SystemRoot'], 'system32', 'cmd.exe'))
            speak("Opening Command Prompt")
        elif "task manager" in command:
            os.startfile(os.path.join(os.environ['SystemRoot'], 'system32', 'Taskmgr.exe'))
            speak("Opening Task Manager")

        elif "restart" in command:
            speak("Are you sure you want to restart the computer? (yes/no)")
            confirmation = take_command().lower()
            if "yes" in confirmation:
                speak("Restarting the computer.")
                os.system("shutdown /r /t 1")
            else:
                speak("Restart cancelled.")
        elif "hibernate" in command:
            speak("Are you sure you want to hibernate the computer? (yes/no)")
            confirmation = take_command().lower()
            if "yes" in confirmation:
                speak("Hibernating the computer.")
                os.system("shutdown /h")
            else:
                speak("Hibernate cancelled.")
        elif "sleep" in command:
            speak("Are you sure you want to put the computer to sleep? (yes/no)")
            confirmation = take_command().lower()
            if "yes" in confirmation:
                speak("Putting the computer to sleep.")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            else:
                speak("Sleep cancelled.")
        elif "shutdown" in command:
            speak("Are you sure you want to shut down the computer? (yes/no)")
            confirmation = take_command().lower()
            if "yes" in confirmation:
                speak("Shutting down the computer.")
                os.system("shutdown /s /t 1")
            else:
                speak("Shutdown cancelled.")

        elif "screenshot" in command:
            take_screenshot()

            # File scanning
        elif "find duplicate file" in command:
            speak("Which directory should I scan for duplicate files?")
            print("Say 'Desktop','Documents','Downloads','Pictures','Videos','Music'.")
            scan_dir_input = take_command()
            if scan_dir_input:
                scan_dir = ""
                if "desktop" in scan_dir_input:
                    scan_dir = os.path.expanduser("~\\OneDrive\\Desktop")
                elif "documents" in scan_dir_input:
                    scan_dir = os.path.expanduser("~\\OneDrive\\Documents")
                elif "downloads" in scan_dir_input:
                    scan_dir = os.path.expanduser("~\\OneDrive\\Downloads")
                elif "pictures" in scan_dir_input:
                    scan_dir = os.path.expanduser("~\\OneDrive\\Pictures")
                elif "videos" in scan_dir_input:
                    scan_dir = os.path.expanduser("~\\OneDrive\\Videos")
                elif "music" in scan_dir_input:
                    scan_dir = os.path.expanduser("~\\OneDrive\\Music")
                else:
                    scan_dir = scan_dir_input
                
                if os.path.isdir(scan_dir):
                    find_duplicate_files(scan_dir)
                else:
                    speak(f"Sorry, I couldn't find the directory '{scan_dir}'.")
            else:
                speak("I didn't catch the directory name. Please try again.")
        elif "find large file" in command:
            speak("Which directory should I scan for large files?")
            print("Say 'Desktop','Documents','Downloads','Pictures','Videos','Music'.")
            scan_dir_input = take_command()
            if not scan_dir_input:
                speak("I didn't catch the directory name. Please try again.")
                continue
            
            scan_dir = ""
            if "desktop" in scan_dir_input:
                scan_dir = os.path.expanduser("~\\OneDrive\\Desktop")
            elif "document" in scan_dir_input:
                scan_dir = os.path.expanduser("~\\OneDrive\\Documents")
            elif "download" in scan_dir_input:
                scan_dir = os.path.expanduser("~\\OneDrive\\Downloads")
            elif "picture" in scan_dir_input:
                scan_dir = os.path.expanduser("~\\OneDrive\\Pictures")
            elif "video" in scan_dir_input:
                scan_dir = os.path.expanduser("~\\OneDrive\\Videos")
            elif "music" in scan_dir_input:
                scan_dir = os.path.expanduser("~\\OneDrive\\Music")
            else:
                scan_dir = scan_dir_input
            if not os.path.isdir(scan_dir):
                speak(f"Sorry, I couldn't find the directory '{scan_dir}'.")
                continue
            speak("What is the minimum file size in MB?")

            size_str = input("Enter minimum file size in MB (default is 100MB): ").strip()
            try:
                min_size = int(size_str)
                find_large_files(scan_dir, min_size)
            except (ValueError, TypeError):
                find_large_files(scan_dir)
                
if __name__ == "__main__":
    main()
