import os 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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

def playVideoOnYoutube(text):

    driver.get("https://www.youtube.com/")
    driver.implicitly_wait(5)
    driver.find_element_by_name("search_query").send_keys(text)
    driver.find_element_by_id("search-icon-legacy").click()
    driver.implicitly_wait(5)
    driver.find_element_by_id("video-title").click()
    
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