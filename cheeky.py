import pyttsx3
import datetime
import speech_recognition as sr
import pyjokes
import webbrowser
import wikipedia
from weather import GetWeather, GetDate
from Talk import GetReply, InitializeBot
import random
from tkinter import *
from PIL import ImageTk, Image

engine = pyttsx3.init('sapi5')  # sapi5 = speech api
voices = engine.getProperty('voices')  # Getting all the available voices
# Setting CHeeky's Voice
engine.setProperty('voice', voices[0].id)

# Tkinter Initialization stuff
root = Tk()
root.title('Cheeky - The Assistant')
root.geometry('1300x650')
root.resizable(False, False)

# Set the 'test' background
# Specifying Background image path
img = ImageTk.PhotoImage(Image.open('E:\Timathon\BGTEST.png'))
# TODO - Still in test phase
bg = Label(root, image=img)
bg.place(x=0, y=0)
bg.pack()

tempLabel = Label(root, text=GetWeather()[0], font=('Dosis SemiBold', 25))
# tempLabel.place(x=5, y=75)
tempLabel.pack()

dayLabel = Label(root, text=GetDate()[0], font=('Dosis SemiBold', 20))
# dayLabel.place(x=5, y=40)
dayLabel.pack()

dateLabel = Label(root, text=GetDate()[1], font=('Dosis SemiBold', 20))
# dateLabel.place(x=5, y=25)
dateLabel.pack()

root.mainloop()  # Mainloop method so that GUI is seen


# Function to make Cheeky speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to take command from user


def TakeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as src:
        r.adjust_for_ambient_noise(src)
        r.pause_threshold = 0.5
        audio = r.listen(src)
    try:
        print('Recognizing')
        query = r.recognize_google(audio, language='en-in')
        print(f'You said {query}\n')
    except Exception as e:
        print('Unable to understand')
        return ' '
    return query

# Function to wish user according to time


def Wish():

    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Cheeky, your Assistant")


def ProcessCommand(query):
    if 'joke' in query:
        joke = pyjokes.get_joke('en', 'neutral')
        speak(joke)
        print(joke)
    elif 'open google' in query:
        webbrowser.open_new_tab('google.com')
        speak("There you have your Google!")
    elif 'open youtube' in query:
        webbrowser.open_new_tab('youtube.com')
        speak('Here\'s your Youtube')
    elif 'open github' in query:
        webbrowser.open_new_tab('github.com')
        speak('Take your Github, Developer!')
    elif 'open stackoverflow' in query:
        webbrowser.open_new_tab('stackoverflow.com')
        speak('Ask your questions on Stackoverflow now')
    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")
    elif 'google' in query:
        query = query.replace('google')
        webbrowser.open_new_tab('https://www.google.com/search?q=' + query)
        speak('Check your google.. I searched for you')
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
    elif query == None:
        pass
    else:
        reply = GetReply(query)
        speak(reply)
        print(reply)


def SetInfo():
    pass
    # TODO - Set labels with value of weather, date, day, news, etc.


WakeMsg = "hello world"
query = ''
WakeRes = ['I am listening', 'Cheeky is ready',
           'What do you want?', 'On your command sir!']

# THe main function
if __name__ == '__main__':

    # Initialized the chatbot stuff
    InitializeBot()
    # Wishing User
    Wish()
    # Initializing Labels with weather, news, date data
    SetInfo()

    while True:

        print('Listening')  # TODO - print listening to a label not on console

        # query = TakeCommand().lower()

        if query.count(WakeMsg) > 0:
            r = random.choice(WakeRes)
            speak(r)
            try:
                ProcessCommand(query)
            except Exception:
                pass
