from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
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

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
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

def auth_googleCalendar():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    
    return service

def getEvents(n, service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        speak('No hay ningun evento próximo.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(event['summary'])
        speak(event['summary'])
        if event['start'].get('dateTime') == None:
            pass
        else:
            print(event['start'].get('dateTime'))
            #speak(event['start'].get('dateTime'))


if __name__=='__main__':

    service = auth_googleCalendar()
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
            elif 'eventos' in query or 'tengo algo' in query or 'calendario' in query:
                getEvents(5, service)






