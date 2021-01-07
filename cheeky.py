import pyttsx3
import datetime
import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def TakeCommand():

    r = sr.Recognizer()

    with sr.Microphone() as src:
        print('Listening')
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


if __name__ == '__main__':
    speak('Hello Sir')
    TakeCommand()
