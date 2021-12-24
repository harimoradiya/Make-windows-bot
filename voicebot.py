import pyttsx3  # pip install pyttsx3
import pywhatkit
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib
import pyjokes
import requests
import wolframalpha

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Bot Sir. Please tell me how may I help you")


# def recognize_speech_from_mic(recognizer, microphone):
#
#     if not isinstance(recognizer, sr.Recognizer):
#         raise TypeError("`recognizer` must be `Recognizer` instance")
#
#     if not isinstance(microphone, sr.Microphone):
#         raise TypeError("`microphone` must be `Microphone` instance")
#
#     # adjust the recognizer sensitivity to ambient noise and record audio
#     # from the microphone
#     with microphone as source:
#         print("Listening...")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)
#
#     # set up the response object
#     response = {
#         "success": True,
#         "error": None,
#         "transcription": None
#     }
#
#
#     try:
#         response["transcription"] = recognizer.recognize_google(audio)
#         query = re.recognize_google(audio, language='en-in')
#         print(f"User said: {query}\n")
#     except sr.RequestError:
#
#         response["success"] = False
#         response["error"] = "API unavailable"
#     except sr.UnknownValueError:
#         # speech was unintelligible
#         response["error"] = "Unable to recognize speech"
#
#     return response
def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        speak("Say that  again please")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()


if __name__ == "__main__":
    wishMe()
    while True:
        # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.nl/maps/place/" + location + "")




        elif "what is" in query or "who is" in query:
            client = wolframalpha.Client("Y6V4XA-GT8UQKHUTU")
            res = client.query(query)
            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                print("No results")

        elif 'play' in query:
            song = query.replace('play', '')
            speak('playing ' + song)
            pywhatkit.playonyt(song)

        # elif 'the time' in query:
        #     strTime = datetime.datetime.now().strftime("%H:%M:%S")
        #     speak(f"Sir, the time is {strTime}")

        elif 'time' in query:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak('Current time is ' + time)

        elif 'open code' in query:
            codePath = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'email to harry' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "harryyourEmail@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend harry bhai. I am not able to send this email")


        elif 'joke' in query:
            speak(pyjokes.get_joke())


        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you, Sir")



        elif "weather" in query:

            # Google Open weather website
            # to get API of Open weather
            api_key = "4f7d53af57fc1b6b98037db290fc347f"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            speak(" City name ")
            print("City name : ")
            city_name = takeCommand()
            url1 = base_url + "q=" + city_name + "&appid=4f7d53af57fc1b6b98037db290fc347f"
            complete_url = base_url + "&q =" + city_name + "appid =" + api_key
            response = requests.get(url1)
            x = response.json()

            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                print(" Temperature (in kelvin unit) = " + str(
                    current_temperature - 272.15) + "\n atmospheric pressure (in hPa unit) =" + str(
                    current_pressure) + "\n humidity (in percentage) = " + str(
                    current_humidiy) + "\n description = " + str(weather_description))
                speak("Temperature of " + city_name + "is " + str(current_temperature - 272.15))

            else:
                speak(" City Not Found ")

        elif "write a note" or "make a note" in query:
            speak("What should i write, sir")
            note = takeCommand()
            file = open('jarvis.txt', 'w')
            speak("Sir, Should i include date and time")
            snfm = takeCommand()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("% H:% M:% S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)

        elif "show note" in query:
            speak("Showing Notes")
            file = open("jarvis.txt", "r")
            print(file.read())
            speak(file.read(6))
