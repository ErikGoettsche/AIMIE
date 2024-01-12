import subprocess
import wolframalpha
import pyttsx3
import tkinter
import json
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen

#Setting the voice engine to pyttsx3, and voice to Female.
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProprty('Voice', voices[1].id)

#defining the speak function, and set on standby
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#Hard coding a greeting to run on startup.
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning !")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon !")
    else:
        speak("Good Evening!")
    vaname = ("Aimie 1 point 0")
    speak("I am your Assitant" + vaname)

#getting the User's preffered greeting and some text generation that I will probably skip.
def userName():
    speak("what should i call you")
    uname = takeCommand()
    speak("Welcome" + uname)
    columns = shutil.get_terminal_size().columns
#Do I need this really?
    print("#####################".center(columns))
    print("Welcome ", uname.center(columns))
    print("#####################".center(columns))

    speak("How can I help you?")

#getting AIMIE to take commands. this section has some... Interesting things to look at later. 
def takeCommand():
    #r? Really? this had better be for a damn reason.
    #aparrently r is actualy from the speech recognition module. 
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
#Tut said to use en-in, but Like, I'm not in India. gonna try it as en-us instead. this will need a rewrite to poll the system for language settings.
        query =r.recognize_google(audio, language = 'en-us')
        print(f"You said: {query}\n")
#again with the single letters?
    except Exception as e:
        print(e)
        print("I'm sorry, I don't understand")
        return "none"
    
    return query

#setting up email. this also needs completely recoded. 
def sendEmail (to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    #to avoid storing credentials in code that is going on GITHUB, this block will be written without values assigned to the variables, and commented out.
    #server.login(user, password)
    #server.sendmail(user, to, content)
    #server.close()

if __name__ == '__main__':
    clear = lambda: os.system('cls')

    clear()
    wishMe()
    userName()
#this section is going to be reworked QUITE a lot. ChatRWKV should be handling most of the language processing, and then providing specific instructions here.
    
    while True:
        query = takeCommand().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 3)
            speak("here's those results")
            print (results)
            speak (results)

        elif 'youtube' in query:
            speak("Pulling up youtube")
            webbrowser.open("youtube.com")

        elif 'google' in query:
            speak("Going to Google")
            webbrowser.open("google.com")

        elif 'stackoverflow' in query:
            speak ("pulling up stackoverflow")
            webbrowser.open("stackoverflow.com")

#Music functions are desired, but we need to use something other than the local filestructure to do it. Perhaps spotify, or maybe a media server?
        #elif 'play music' in query or "play song" in query: 
            #speak ("lets get this party started") 
            #musicDirectory = TBD 
            #songs = os.listdir(musicDirectory) 
            #print (songs) 
            #random = os.startfile(os.path.join(musicDirectory, songs [1]))

#This function was writing assuming a windows environment, the Client will be on several different environments. hardcoding for windows is hilarious, but tragic.
        #elif 'firefox' in query:
            #codepath = (filepath for firefox launcher)
            #os.startfile(codepath)

        elif 'send a mail' in query:
            try:
                speak("What do you want to say?")
                content = takeCommand()
                speak("who should we send it to?")
                to = input()    
                sendEmail(to, content)
                speak("Email sent!")
            except Exception as e:
                print(e)
                speak("I'm sorry, I couldn't send that email.")
        
        elif 'how are you' in query:
            speak("I am doing well, Thanks!")

        elif "change your name to" in query:
            query = query.replace("change my name to", "")
            vaname = query

        elif "change name" in query:
            speak("What will you be calling me?")
            vaname = takeCommand()
            speak("Very good, my name is" + vaname)

        elif "exit" in query:
            speak("It was wonderful speaking to you.")
            exit()

        elif "joke" in query:
            speak(pyjokes.get_joke())

#maybe AI just does this explicitely later?
        elif "calculate" in query:
            app_id = "Wolframalpha api id"
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1]
            answer = next(res.results).text
            print ("The answer is" + answer)
            speak ("The answer is" + answer)

        elif 'search' in query:
            query = query.replace("search", "")
            webbrowser.open(query)

        