import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import wikipedia
import os
import pyjokes
import requests
from bs4 import BeautifulSoup

try:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    def greet():
        hour = int(datetime.datetime.now().hour)
        print(hour)
        if hour >= 0 and hour < 12:
            speak("Good Morning!")
        elif hour >= 12 and hour < 18:
            speak("Good Afternoon!")
        else:
            speak("Good Evening!")
        speak("Welcome, I am your personal assistant.")

    def VoiceCommand():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print(e)
            print("Unable to Recognize your voice.")
            return "None"
        return query

    def get_weather():
        city = "Your_City_Name"
        api_key = "Your_OpenWeatherMap_API_Key"
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(base_url)
        data = response.json()
        if data["cod"] != "404":
            main = data["main"]
            weather_description = data["weather"][0]["description"]
            temp = main["temp"] - 273.15  # Convert from Kelvin to Celsius
            speak(f"The temperature is {temp:.2f} degrees Celsius with {weather_description}.")
        else:
            speak("City not found.")

    def take_screenshot():
        import pyautogui
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        speak("Screenshot taken and saved.")

    if __name__ == '__main__':
        greet()
        while True:
            work = VoiceCommand().lower()
            if 'hello' in work:
                speak('Hi, how can I help you?')

            if "wikipedia" in work:
                speak("Searching Wikipedia...")
                work = work.replace("wikipedia", "")
                results = wikipedia.summary(work, sentences=5)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'open notepad' in work:
                speak('Opening Notepad for you...')
                path = ("c:\\windows\\system32\\notepad.exe")
                os.startfile(path)
            elif 'close notepad' in work:
                speak('Closing Notepad, wait...')
                os.system('c:\\windows\\system32\\taskkill.exe /F /IM notepad.exe')

            elif 'open youtube' in work:
                speak("Here you go to Youtube.")
                webbrowser.open("https://www.youtube.com")

            elif 'open google' in work:
                speak("Here you go to Google.")
                webbrowser.open("https://www.google.com")

            elif 'play music' in work:
                speak('Opening music player...')
                path = ("C:\\Program Files (x86)\\Windows Media Player\\wmplayer.exe")
                os.startfile(path)

            elif 'open mail' in work:
                speak("Here you go to mail.")
                webbrowser.open("https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox")

            elif 'open whatsapp' in work:
                speak("Opening WhatsApp for you.")
                webbrowser.open("https://web.whatsapp.com")

            elif 'time' in work:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {strTime}")

            elif 'date' in work:
                strDate = datetime.datetime.now().strftime("%Y-%m-%d")
                speak(f"Today's date is {strDate}")

            elif 'weather' in work:
                get_weather()

            elif 'screenshot' in work:
                take_screenshot()

            elif 'joke' in work:
                joke = pyjokes.get_joke()
                speak(joke)

            elif 'exit' in work:
                speak("Thanks for giving me your time. Have a nice day.")
                exit()

            else:
                speak("I did not understand the command. Please try again.")

except BaseException as ex:
    print(f"Error occurred: {ex}")

finally:
    print("Thank you...bye. Have a nice day.")

    