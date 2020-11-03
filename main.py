import os
import datetime
import time
import pyaudio
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from playsound import playsound
from speak import *
import subprocess
import wikipedia


os.system('cls')

pathChromeDriver = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(pathChromeDriver)

def takeNote(text):
    speak("¿Que nombre le pongo?")
    noteName = takeCommand()
    note = (f"{noteName}.txt")
    with open(note, 'w') as f:
        f.write(text)
    subprocess.Popen(['notepad.exe', noteName])

def getTime():
    currentTime = datetime.datetime.now().strftime("%H:%M")
    speak(f"Son las, {currentTime}, horas")

def getDate():
    currentDate = datetime.datetime.now().strftime("%d, del ,%m")
    speak(f"Hoy es el, {currentDate}")

def openWebsite(website):
    driver.get(website)

def getInformation(text):
    text = text.replace("wikipedia", "")
    results = wikipedia.summary(text, sentences=1)
    speak("según wikipedia")
    print("results")
    speak(results)

if __name__=='__main__':
    
    while True:
        query = takeCommand().lower()
        if 'hanna' in query:
            speak("Hola Tomás, ¿en que te puedo ayudar?")
            query = takeCommand().lower()

            if 'gracias hanna' in query or 'listo hanna' in query or 'listo' in query:
                speak('Hasta luego!')
                exit()
            elif 'anotá' in query or 'escribí una nota' in query or 'escribí un memo' in query:
                speak('¿Que querés que escriba?')
                text = takeCommand().lower
                takeNote(text)
                speak('Listo!')
            elif 'que hora es' in query or 'me decís la hora' in query:
                getTime()
            elif 'que día es' in query or 'me decís el día' in query:
                getDate()
            elif 'abrí youtube' in query:
                youtubeURL = "https://www.youtube.com/"
                openWebsite(youtubeURL)
            elif 'abrí twitch' in query:
                twitchURL = "https://www.twitch.tv/"
                openWebsite(twitchURL)
            elif 'quien es' in query or 'buscá sobre' in query or 'wikipedia' in query or 'quiero saber sobre' in query:
                speak("buscando...")
                getInformation(query)




