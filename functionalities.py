import os 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from speak import speak, takeCommand
import subprocess
import wikipedia
import datetime
from datetime import datetime as dt
from dateutil.parser import parse as dtparse
import time
import pyaudio
import requests

#pathChromeDriver = "C:\Program Files (x86)\chromedriver.exe"
pathChromeDriver = "C:/Program Files (x86)/chromedriver.exe"
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

def getEvents(n, service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No hay ningun evento próximo.')
        speak('No hay ningun evento próximo.')
    for event in events:
        #start = event['start'].get('dateTime', event['start'].get('date'))
        print(event['summary'])
        speak(event['summary'])
        if event['start'].get('dateTime') == None:
            pass
        else:
            timeFormat = f'%d del %m, a las %H:%M %p'
            time = event['start'].get('dateTime') 
            print(f'Hanna: {dt.strftime(dtparse(time), format=timeFormat)}')
            speak(dt.strftime(dtparse(time), format=timeFormat))
    
    print('Hanna: Esos son todos los eventos.')
    speak('Esos son todos los eventos.')

def weatherRequest(city,key):
    
    apiLink = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&lang=sp"

    api_link = requests.get(apiLink)
    apiData = api_link.json()
    if apiData['cod'] == '404':
        print('Hanna: No hay datos disponibles')
        speak(' No hay datos disponibles')
    else:
        temp = int((apiData['main']['temp'])- 273.15)
        description = apiData['weather'][0]['description']
        print(f"Hanna: Hoy en {city}, está {description} y hacen {temp} grados.")
        speak(f"Hoy en {city}, está {description} y hacen {temp} grados.")