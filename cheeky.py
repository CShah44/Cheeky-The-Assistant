import pyttsx3
import datetime
import speech_recognition as sr
import pyjokes
import webbrowser
import wikipedia
from weather import GetWeather, GetDate
from Talk import GetReply
import random
from tkinter import *
from PIL import ImageTk, Image
from News import GetNews
import time
import subprocess

engine = pyttsx3.init('sapi5')  # sapi5 = speech api
voices = engine.getProperty('voices')  # Getting all the available voices
# Setting Cheeky's Voice
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

i = ImageTk.PhotoImage(Image.open("activate.png"))
activate_button = Button(root, text='Δ', font=(
        'Dosis SemiBold', 20), width=30, height=30, borderwidth=0.5, image=i)
activate_button_window = canvas.create_window(
        750, 42, window=activate_button)

def activate_cheeky(e):
    clear_entry('e')
    canvas.itemconfigure(status_label, text='Listening')
    print('working boss')
    try:
        query = take_command().lower()
        process_command(query)
    except Exception:
        print('RETRY')

def deactivate_cheeky(e):
    canvas.itemconfigure(status_label, text='Sleeping')
    canListen = False

# clears the entry window when it loses focus
def clear_entry(e):
    command_entry.delete(0, END)


# sets the placeholder text for th eentry widget
def set_entry_placeholder(e):
    command_entry.insert(0, "Type Something")

# Function to make Cheeky speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def change_wish_text(t):
    canvas.itemconfigure(wish_user_label, text=t)

# Function to wish user according to time
def wish():
    hour = int(datetime.datetime.now().hour)
    w = ''
    if hour >= 0 and hour < 12:
        w = 'Good Morning!'

    elif hour >= 12 and hour < 18:
        w = 'Good Afternoon'

    else:
        w = 'Good Evening'

    change_wish_text(w)
    speak(w + "I am Cheeky, your Assistant")

# Function to open the news on the web
def open_news(link):
    webbrowser.open(link)
    return "Opened news article"



# Function to get input from the input field
def get_input():
    query = command_entry.get().lower()  # Get the command of user from entry box
    if query:
        process_command(query)  # Process the command
        command_entry.delete(0, END)  # Clearing the entry widget
        # Setting the default text again
        command_entry.insert(0, "Type Something")
    return "Got input"

# Function to take command from user
def take_command():
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

# Printing User's command on the screen
def print_user_command(c):
    canvas.itemconfigure(user_command_label, text=c, justify=RIGHT)


# Printing cheeky's reply on the screen
def print_bot_reply(r):
    canvas.itemconfigure(bot_command_label, text=r, justify='left')


# Changes the text of the status label. (Awake, Listening, Sleeping, Recognizing)
def change_bot_status(s):
    canvas.itemconfigure(status_label, text=s)


def process_command(query):
    print_user_command(query)
    if 'joke' in query:
        joke = pyjokes.get_joke('en', 'neutral')
        speak(joke)
        print_bot_reply(joke)
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
        print_bot_reply(results)
        speak(results)
    # TODO - Exit function
    elif 'exit' in query:
        speak('ba bye')
        exit()
    elif "locate" in query:
        query = query.replace("locate", "")
        location = query
        speak("So I am locating.. ")
        speak(location)
        webbrowser.open("https://www.google.nl / maps / place/" + location + "")
    else:
        reply = GetReply(query)
        speak(reply)
        print_bot_reply(reply)

root.bind('<KeyRelease-c>', deactivate_cheeky)

root.bind('<KeyPress-c>', activate_cheeky)

command_entry = Entry(root, font=('Dosis SemiBold', 20), width=39)
command_entry_window = canvas.create_window(
    300, 590, window=command_entry, anchor='nw')
command_entry.insert(0, "Type Something")

you_label = canvas.create_text(
    930, 80, text='YOU', anchor='nw', font=('Dosis SemiBold', 25), fill='white')

# label containing user's command :]
user_command_label = canvas.create_text(
    980, 120,
    text='Start by waking Cheeky up and give him commands or start typing, e.g.: open google, open wikipedia or just chat with him',
    anchor='ne', font=('Dosis SemiBold', 20), fill='white', width=640, justify=RIGHT)

bot_label = canvas.create_text(
    300, 280, text='CHEEKY', anchor='nw', font=('Dosis SemiBold', 25), fill='white')

# The reply label of cheeky's response
bot_command_label = canvas.create_text(
    305, 330,
    text='I am sleeping, wake me up to start talking with me buddy.. You know I\'m very smart and smart bois need more sleep',
    anchor='nw', font=('Dosis SemiBold', 20), fill='white', width=640)

# defining events for entry widget : Losing And Getting Focus
command_entry.bind("<FocusIn>", clear_entry)
command_entry.bind("<FocusOut>", set_entry_placeholder)

send_command_button = Button(root, text='Send', font=(
    'Dosis SemiBold', 20), width=6, command=lambda: get_input())
send_command_button_window = canvas.create_window(
    955, 600, window=send_command_button)

news_labels = []  # List of all buttons containing news

temp = GetWeather()[0]
temp_label = canvas.create_text(
    100, 370, text=temp, font=('Dosis SemiBold', 75))

weather_type = GetWeather()[1]
weather_type_label = canvas.create_text(
    80, 445, text=weather_type, font=('Dosis SemiBold', 30))

date_text = GetDate()[0] + ' ' + GetDate()[1]
date_label = canvas.create_text(
    110, 500, text=date_text, font=('Dosis SemiBold', 30))

wish_user_label = canvas.create_text(
    20, 170, text='Good Afternoon!', anchor='nw', font=('Dosis SemiBold', 30))

info_label = canvas.create_text(
    1027, 610, text='(Click the article to read it)', anchor='nw', font=('Dosis SemiBold', 14), fill='white')

# creating the news buttons
y = 80  # y co-ordinate of buttons
for index in range(0, 5):
    title = GetNews()[index][0]
    link = GetNews()[index][1]

    b = Button(root, text=title, bg = '#618ec2',
            font=('Dosis SemiBold', 12), width=250, wraplength=250, justify='center',
            fg='black', command=lambda: open_news('google.com'), borderwidth=0)
    b_window = canvas.create_window(1027, y, window=b, anchor='nw')
    y += 110
    news_labels.append(b)

canvas.pack(fill='both', expand=True)  # Show the canvas on the screen

# Wishing User
wish()



WakeMsg = "wake up"
query = ''
WakeRes = ['I am listening', 'Cheeky is ready',
           'What do you want?', 'On your command sir!']


root.mainloop()  # Mainloop method so that GUI is seen