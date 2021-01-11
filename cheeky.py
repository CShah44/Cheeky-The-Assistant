import pyttsx3
import datetime
import speech_recognition as sr
import pyjokes
import webbrowser
import wikipedia
# from weather import GetWeather

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def TakeCommand():

    r = sr.Recognizer()

    with sr.Microphone() as src:
        print('Listening.... speak exit to escape')
        r.pause_threshold = 1
        audio = r.listen(src)
    try:
        print('Recognizing')
        query = r.recognize_google(audio, language='en-in')
        print(f'You said {query}\n')
    except Exception as e:
        print(e)
        print('Unable to understand')
        return None
    return query


def Wish():

    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Chaitya !")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Chaitya !")

    else:
        speak("Good Evening Chaitya !")

    speak("I am Cheeky, your Assistant")

#  yet to put - hey cheeky feature to wake him
# google search
# chatterbot


def ProcessCommand(query):
    if 'joke' in query:
        joke = pyjokes.get_joke('en', 'neutral')
        speak(joke)
        print(joke)
    elif 'open google' in query:
        webbrowser.open('google.com')
        speak("There you have your Google!")
    elif 'open youtube' in query:
        webbrowser.open('youtube.com')
        speak('Here\'s your Youtube')
    elif 'open github' in query:
        webbrowser.open('github.com')
        speak('Take your Github, Developer!')
    elif 'open stackoverflow' in query:
        webbrowser.open('stackoverflow.com')
        speak('Ask your question on Stackoverflow now')
    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")
    elif 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=4)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    elif 'exit' in query:
        speak('ba bye')
        exit()


if __name__ == '__main__':

    Wish()

    while True:

        query = TakeCommand().lower()
        ProcessCommand(query)
