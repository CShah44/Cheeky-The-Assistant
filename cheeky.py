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
from News import GetNews
import time
import subprocess

engine = pyttsx3.init('sapi5')  # sapi5 = speech api
voices = engine.getProperty('voices')  # Getting all the available voices
# Setting CHeeky's Voice
engine.setProperty('voice', voices[0].id)

canListen = False

# Tkinter Initialization stuff
root = Tk()
root.title('Cheeky - The Assistant')
root.geometry('1300x650')
root.resizable(False, False)

# Set the 'test' background
canvas = Canvas(root)  # creating canvas for all widgets to be placed on it
canvas.config(width=1300, height=650)  # set sizes of canvas

# Specifying Background image path
img = ImageTk.PhotoImage(Image.open('E:\Timathon\BGTEST.png'))
canvas.create_image(0, 0, image=img, anchor='nw')  # create background img

# TODO- It will open a new window
about_help_button = Button(root, text='About/Help', font=(
    'Dosis SemiBold', 20), width=15)
about_help_button_window = canvas.create_window(
    130, 600, window=about_help_button)

status_label = canvas.create_text(
    650, 40, text='Sleeping', font=('Dosis SemiBold', 20))
# canvas.itemconfigure(status_label, text='Awake')

send_command_button = Button(root, text='Send', font=(
    'Dosis SemiBold', 20), width=6, command=lambda: GetInput())
send_command_button_window = canvas.create_window(
    955, 600, window=send_command_button)

command_entry = Entry(root, font=('Dosis SemiBold', 20), width=39)
command_entry_window = canvas.create_window(
    300, 590, window=command_entry, anchor='nw')
command_entry.insert(0, "Type Something")

you_label = canvas.create_text(
    930, 80, text='YOU', anchor='nw',  font=('Dosis SemiBold', 25), fill='white')

# label containing user's command :]
user_command_label = canvas.create_text(
    360, 120, text='Start by waking Cheeky up and give him commands or start typing, e.g.: open google, open wikipedia or just chat with him',
    anchor='nw',  font=('Dosis SemiBold', 20), fill='white', width=640, justify='right')

bot_label = canvas.create_text(
    300, 280, text='CHEEKY', anchor='nw',  font=('Dosis SemiBold', 25), fill='white')

# The reply label of cheeky's response
bot_command_label = canvas.create_text(
    305, 330, text='I am sleeping, wake me up to start talking with me buddy.. You know I\'m very smart and smart bois need more sleep',
    anchor='nw',  font=('Dosis SemiBold', 20), fill='white', width=640)

# clears the entry window when it loses focus


def ClearEntry(e):
    command_entry.delete(0, END)

# sets the placeholder text for th eentry widget


def SetEntryPlaceholder(e):
    command_entry.insert(0, "Type Something")


# defining events for entry widget : Losing And Getting Focus
command_entry.bind("<FocusIn>", ClearEntry)
command_entry.bind("<FocusOut>", SetEntryPlaceholder)


def MainGUI():

    newsLabels = []  # List of all buttons containing news

    temp = GetWeather()[0]
    tempLabel = canvas.create_text(
        100, 370, text=temp, font=('Dosis SemiBold', 75))

    weatherType = GetWeather()[1]
    weatherTypeLabel = canvas.create_text(
        80, 445, text=weatherType, font=('Dosis SemiBold', 30))

    dateText = GetDate()[0] + ' ' + GetDate()[1]
    dateLabel = canvas.create_text(
        110, 500, text=dateText, font=('Dosis SemiBold', 30))

    wishUserLabel = canvas.create_text(
        20, 170, text='Good Afternoon!', anchor='nw',  font=('Dosis SemiBold', 30))

    infoLabel = canvas.create_text(
        1027, 610, text='(Click the article to read it)', anchor='nw',  font=('Dosis SemiBold', 14), fill='white')

    # creating the news buttons
    y = 80  # y co-ordinate of buttons
    for index in range(0, 5):
        title = GetNews()[index][0]
        link = GetNews()[index][1]

        b = Button(root, text=title,
                   font=('Dosis SemiBold', 12), width=31, wraplength=250, justify='center', bg='blue', fg='white', command=lambda: OpenNews(link))
        b_window = canvas.create_window(1027, y, window=b, anchor='nw')
        y += 110
        newsLabels.append(b)

    canvas.pack(fill='both', expand=True)  # Show the canvas on the screen
    root.mainloop()  # Mainloop method so that GUI is seen

    # Wishing User
    Wish()

# Function to open the news on the web


def OpenNews(link):
    webbrowser.open(link)
    return "Opened news article"

# Function to get input from the input field


def GetInput():
    query = command_entry.get().lower()  # Get the command of user from entry box
    if query:
        ProcessCommand(query)  # Process the command
        command_entry.delete(0, END)  # Clearing the entry widget
        # Setting the default text again
        command_entry.insert(0, "Type Something")
    return "Got input"


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

# Printing User's command on the screen


def PrintUserCommand(c):
    canvas.itemconfigure(user_command_label, text=c, justify='right')

# Printing cheeky's reply on the screen


def PrintBotReply(r):
    canvas.itemconfigure(bot_command_label, text=r, justify='left')

# Changes the text of the status label. (Awake, Listening, Sleeping, Recognizing)


def ChangeBotStatus(s):
    canvas.itemconfigure(status_label, text=s)


def ProcessCommand(query):
    PrintUserCommand(query)
    if 'joke' in query:
        joke = pyjokes.get_joke('en', 'neutral')
        speak(joke)
        PrintBotReply(joke)
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
    elif "restart" in query:
        subprocess.call(["shutdown", "/r"])
    elif "hibernate" in query or "sleep" in query:
        speak("Hibernating")
        subprocess.call("shutdown / h")
    elif "log off" in query or "sign out" in query:
        speak("Close all apps as I'll log off in 10 seconds")
        time.sleep(5)
        subprocess.call(["shutdown", "/l"])
    elif 'shutdown' in query:
        speak("ok, I am shutting down your pc")
        subprocess.call('shutdown / p /f')
    elif 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        PrintBotReply(results)
        speak(results)
    # TODO - Exit function
    elif 'exit' in query:
        speak('ba bye')
        # exit()
    elif query == None:
        pass
    else:
        reply = GetReply(query)
        speak(reply)
        PrintBotReply(reply)


WakeMsg = "wake up"
query = ''
WakeRes = ['I am listening', 'Cheeky is ready',
           'What do you want?', 'On your command sir!']

# THe main function
if __name__ == '__main__':

    # Make the gui
    MainGUI()

    while True:  # TODO - Move it to main function

        print('Listening')  # TODO - print listening to a label not on console

        query = TakeCommand().lower()

        if query.count(WakeMsg) > 0:
            r = random.choice(WakeRes)
            speak(r)
            try:
                ProcessCommand(query)
            except Exception:
                pass
