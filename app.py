from tkinter import *
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import tkinter.messagebox as tmsg
import threading
import speech_recognition as sr
import pyautogui as bot
import pyttsx3
import pywhatkit as web_bot

def Window_size(width,height):
    app.geometry(f"{width}x{height}")
    app.minsize(width,height)
    app.maxsize(width,height)

def Exit_app():
    app.destroy()

def Developer():
    tmsg.showinfo(
        "Developer",
        "Designed and created by Nishant Maity"
    )

def help_guid():
    tmsg.showinfo(
        "Help",
        "Turn on toggle button and say commands"
    )

def Features():
    tmsg.showinfo(
        "Features",
        """
        > Next slide
        > Previous slide
        > FullScreen Mode
        > Google Search
        > Youtube Search
        """
    )

def Next_page():
    tmsg.showinfo(
        "Next Page Commands",
        """
        next page, forward,
        next, right
        """
    )

def Previous_page():
    tmsg.showinfo(
        "Previous Page Commands",
        """
        previous page, backward,
        previous, left, back
        """
    )

def full_screen_mode():
    tmsg.showinfo(
        "Fullscreen Commands",
        """
        fullscreen, big, f11,
        full
        """
    )

def Google_search_commands():
    tmsg.showinfo(
        "Google Search Commands",
        """
        Search, google search,
        jarvis, google
        """
    )

def Youtube_search_commands():
    tmsg.showinfo(
        "Youtube Search Commands",
        """
        play, yt,
        youtube
        """
    )

### Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech speed

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

recognizer = sr.Recognizer()


def listen_command():
    """Listen for voice commands."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  ### Adjust for background noise
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        return command
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Sorry, there was an issue with the speech service.")
        return ""
    
listening = False

def control_presentation():
    """
    Control the presentation 
    based on voice commands.
    """
    speak("Bot Activated")
    global listening

    while listening:
        command = listen_command()

        Next_commands = [
            "next page","forward",
            "next","right"
        ]

        if any(word in command for word  in Next_commands):
            bot.press("right")
            speak("Next slide")
        
        Previous_commands = [
            "previous","back",
            "backward","left"
        ]

        if any(word in command for word  in Previous_commands):
            bot.press("left")
            speak("Previous slide")
        
        Fullscreen_commands = [
            "full","full screen",
            "f11","big"
        ]

        if any(word in command for word  in Fullscreen_commands):
            bot.press("f11")
            speak("full screen mode")
        
        Google_search_commands = [
            "google","search",
            "google search","jarvis"
        ]

        if any(word in command for word  in Google_search_commands):
            speak("searching")
            search_command = command.replace("search" ,"").\
                replace("google search","").replace("jarvis",'').\
                replace("hey jarvis",'').replace("google","")
            web_bot.search(search_command)
        
        
        Yt_search_commands = [
            "play","youtube",
            "yt"
        ]

        if any(word in command for word  in Yt_search_commands):
            speak("searching")
            yt_search_command = command.replace("play" ,"").\
                replace("youtube","").replace("yt",'')
            web_bot.playonyt(yt_search_command)
        

        elif "exit" in command or "quit" in command:
            bot.press("f11")
            speak("Exiting presentation control.")
            

### ppt controller function
def ppt_controller_bot():
    if Bot_var.get() == 1:
        global listening
        if not listening:
            listening = True
            threading.Thread(target=control_presentation).start()
        else:
            tmsg.showinfo("Info", "Already listening for commands.")
    else:
        listening = False



### app window
app = ttkb.Window(themename="vapor")



Menu_bar = Menu(app)

services = Menu(Menu_bar)
services['bg']='#303841'
services['fg']='#d3d6db'

Menu_bar.add_command(label="Developer",command=Developer)
services.add_command(label="Features",command=Features)
services.add_command(label="How to use",command=help_guid)

Menu_bar.add_cascade(label="Services",menu=services)

app_info = Menu(Menu_bar)
app_info['bg']='#303841'
app_info['fg']='#d3d6db'

app_info.add_command(label="Next Page",command=Next_page)
app_info.add_command(label="Previous Page",command=Previous_page)
app_info.add_command(label="Fullscreen Mode",command=full_screen_mode)
app_info.add_command(label="Google Search",command=Google_search_commands)
app_info.add_command(label="Youtube Search",command=Youtube_search_commands)

Menu_bar.add_cascade(label="Command info",menu=app_info)
Menu_bar.add_command(label="Exit App",command=Exit_app)


app.config(menu=Menu_bar)

App_title = ttkb.Label(
    master=app,
    text="Voice Presentation Controller",
    foreground="#ff9a3c",
    font=("arial",14)
).pack(pady=20)

### creating frame
App_body_frame = ttkb.Frame()
App_body_frame.pack(anchor="w",padx=13)

Next_page_info = ttkb.Label(
    master=App_body_frame,
    text="Say Next for next page",
    foreground="#ffffff",
    font=("arial",11)
).grid(row=0,column=0,sticky="w",pady=9)

Previous_page_info = ttkb.Label(
    master=App_body_frame,
    text="Say Previous for Previous page",
    foreground="#ffffff",
    font=("arial",11)
).grid(row=1,column=0,sticky="w")

More_info = ttkb.Label(
    master=App_body_frame,
    text="for more rmation click on menu button",
    foreground="#ffffff",
    font=("arial",11)
).grid(row=2,column=0,sticky="w",pady=9)

Bot_activate_info = ttkb.Label(
    master=App_body_frame,
    text="Press button to activate bot",
    foreground="#ffffff",
    font=("arial",11)
).grid(row=3,column=0,sticky="w")

Bot_var = IntVar()

Bot_Activate_Button = ttkb.Checkbutton(
    master=App_body_frame,
    text="Activate Bot",
    bootstyle="warning, roundtoggle",
    onvalue=1,
    variable=Bot_var,
    offvalue=0,
    command=ppt_controller_bot
).grid(row=4,column=0,pady=11,sticky="w")

developer_label = ttkb.Label(
    master=app,
    text="Developer Nishant Maity",
    font=("arial",9),
    bootstyle="warning"
).pack(pady=9,side="bottom")

app.title("Presentation Controller Bot")
if __name__=="__main__":
    Window_size(490,290)
app.mainloop()