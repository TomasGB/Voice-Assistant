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
from speak import *
import subprocess
import functionalities as func


os.system('cls')
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

days = ["lunes""martes","miercoles","jueves","viernes","sabado","domingo"]
months = ["enero","febrero","marzo","abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def voiceToDate(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count('today') > 0:
        return today
    
    day = -1
    dayOfWeek = -1
    month = -1
    year = today.year -1

    for word in text.split():
        if word in months:
            month = months.index(word) + 1
        elif word in days:
            dayOfWeek = days.index(word) - 1
        elif word.isdigit():
            day = int(word)
        else:
            pass
    
    if month < today.month and month != -1:
        year = year + 1
    if day < today.day and month == -1 and day != -1:
        month = month + 1
    if month == -1 and day == -1 and dayOfWeek != -1:
        currDayOfWeek = today.weekday()
        dif = dayOfWeek - currDayOfWeek

        if dif < 0:
            dif += 7
            if text.count('next') >= 1:
                dif += 7
        return today + datetime.timedelta(dif)
    if month == -1 or day == -1:
        return None

    return datetime.date( month=month, day=day, year= year)

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
        #if 'hanna' in query or 'jana' in query or 'ana' in query:
        print("Hanna: Hola Tomás, ¿en que te puedo ayudar?")
        speak("Hola Tomás, ¿en que te puedo ayudar?")
        
        query = takeCommand().lower()
            
        if 'gracias hanna' in query or 'listo hanna' in query or 'listo' in query or 'isto' in query:
            speak('Hanna: Hasta luego!')
            exit()
        elif 'anotá' in query or 'anota' in query or 'escribí una nota' in query or 'escribí un memo' in query:
            speak('Hanna: ¿Que querés que escriba?')
            text = takeCommand().lower()
            func.takeNote(text)
            speak('Listo!')
        elif 'qué hora es' in query or 'me decís la hora' in query:
            currentTime = datetime.datetime.now().strftime("%H:%M")
            print(f"Hanna: Son las, {currentTime}, horas")
            speak(f"Son las, {currentTime}, horas")
        elif 'qué día es' in query or 'que día es' in query or 'me decis el dia' in query:
            currentDate = datetime.datetime.now().strftime("%d, del ,%m")
            print(f"Hanna: Hoy es el, {currentDate}")
            speak(f"Hoy es el, {currentDate}")
        elif 'abri youtube' in query or 'abrir youtube' in query:
            youtubeURL = "https://www.youtube.com/"
            func.openWebsite(youtubeURL)
        elif 'abri twitch' in query or 'abrir twitch' in query:
            twitchURL = "https://www.twitch.tv/"
            func.openWebsite(twitchURL)
        elif 'quien es' in query or 'busca sobre' in query or 'wikipedia' in query or 'quiero saber sobre' in query:
            speak("buscando...")
            func.getInformation(query)
        elif 'cancion' in query or 'canción' in query:
            print('Hanna: ¿que canción busco?')
            speak('¿que canción busco?')
            song = takeCommand().lower()
            print(f"Hanna: Buscando la cancion, {song}")
            speak(f"Buscando la cancion, {song}")
            func.playVideoOnYoutube(song)
        elif 'video' in query :
            print('Hanna: ¿Que video busco?')
            speak('¿que video busco?')
            video = takeCommand().lower()
            print(f"Hanna:  Buscando el video, {video}")
            speak(f"buscando la video, {video}")
            func.playVideoOnYoutube(song)   
        elif 'eventos' in query or 'tengo algo' in query or 'calendario' in query:
            getEvents(5, service)

