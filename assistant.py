import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import subprocess
import re

# Initialize text-to-speech engine with default driver
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

# Assistant name (customizable)
ASSISTANT_NAME = "Assistant"

def speak(text):
    """Speak the given text."""
    print(f"{ASSISTANT_NAME}: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for a voice command and return the text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
            return ""
        except sr.RequestError:
            speak("I'm having trouble connecting to the speech service.")
            return ""

def process_command(command):
    """Process the voice command and perform actions."""
    if not command:
        return

    # Check if assistant's name is mentioned
    if ASSISTANT_NAME.lower() not in command and "hey" not in command:
        return

    command = command.replace(ASSISTANT_NAME.lower(), "").strip()

    # Greetings
    if "hello" in command or "hi" in command:
        speak("Hey there! How can I help you today?")

    # Time
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")

    # Web search
    elif "search" in command:
        query = re.sub(r"search( for)?", "", command).strip()
        if query:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            speak(f"Searching for {query}.")
        else:
            speak("What would you like me to search for?")

    # Open websites
    elif "open" in command:
        if "youtube" in command:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube.")
        elif "wikipedia" in command:
            webbrowser.open("https://www.wikipedia.org")
            speak("Opening Wikipedia.")
        else:
            speak("I can open YouTube or Wikipedia. Which one would you like?")

    # Open applications (Windows-specific)
    elif "start" in command or "open" in command:
        if "notepad" in command:
            subprocess.Popen("notepad.exe")
            speak("Opening Notepad.")
        elif "calculator" in command:
            subprocess.Popen("calc.exe")
            speak("Opening Calculator.")
        else:
            speak("I can open Notepad or Calculator. What would you like?")

    # Who are you
    elif "who are you" in command:
        speak(f"I am {ASSISTANT_NAME}, your personal AI assistant, here to make your life easier!")

    # Exit
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        exit()

    else:
        speak("I'm not sure how to help with that. Try something like 'time', 'search', or 'open YouTube'.")

def main():
    """Main loop to run the assistant."""
    speak(f"{ASSISTANT_NAME} online. How can I assist you?")
    
    while True:
        command = listen()
        process_command(command)

if __name__ == "__main__":
    main()