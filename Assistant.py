import os
import requests
import webbrowser
import speech_recognition as sr
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
def speak(text):
    print(f"Assistant: {text}")
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
        speak("I didn't understand that, please try again")
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
        speak(f"Current temperature in {city} is {temp}°C with {weather}")
    except:
        speak("Couldn't fetch weather data")

def main():
    # speak('Test 1')
    # speak('Test 2')
    speak("Hi, I'm your Desktop assistant. How can I help you?")
    while True:
        command = take_command()

        if not command:
            continue

        if "exit" in command or "quit" in command or "stop" in command:
            speak("Goodbye!")
            break
        
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
            # elif "vs code" in command:
            #     os.startfile("C:\\Program Files\\Microsoft VS Code\\Code.exe")
            #     speak("Opening Visual Studio Code")
            else:
                speak("I can only open browser, file explorer, or notepad.")
                
if __name__ == "__main__":
    main()
