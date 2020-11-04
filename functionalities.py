import os 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from playsound import playsound
from speak import *
import subprocess
import wikipedia
import datetime
import time
import pyaudio


pathChromeDriver = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(pathChromeDriver)
def openWebsite(website):
    driver.get(website)

def takeNote(text):
    speak("¿Que nombre le pongo?")
    noteName = takeCommand()
    note = (f"{noteName}.txt")
    with open(note, 'w') as f:
        f.write(text)
    subprocess.Popen(['notepad.exe', noteName])

def getInformation(text):
    text = text.replace("wikipedia", "")
    results = wikipedia.summary(text, sentences=1)
    speak("según wikipedia")
    print("results")
    speak(results)