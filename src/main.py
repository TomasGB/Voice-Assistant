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
from speak import speak, takeCommand
import subprocess
from apiCredentials import weather_Key
import functionalities as func
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import threading

os.system('cls')
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

pathChromeDriver = "C:/Program Files (x86)/chromedriver.exe"


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


if __name__ == '__main__':
    service = auth_googleCalendar()
    api = func.AuthTwitter()
    driver = webdriver.Chrome(pathChromeDriver)
    driver.minimize_window()

    while True:
        query = takeCommand().lower()

        if 'hanna' in query or 'jana' in query or 'ana' in query:
            print("Hanna: Hola , ¿en que te puedo ayudar?")
            speak("Hola, ¿en que te puedo ayudar?")
            query = takeCommand().lower()

            if 'anotá' in query or 'anota' in query or 'escribí una nota' in query or 'escribí un memo' in query:
                print('Hanna: ¿Que querés que escriba?')
                speak('¿Que querés que escriba?')
                text = takeCommand().lower()
                print('Hanna: ¿Que nombre le pongo?')
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

            elif 'como esta el clima' in query or 'como esta el dia' in query or 'como esta el día' in query or 'clima' in query:

                print('Hanna: ¿En que ciudad?')
                speak('¿En que ciudad?')

                city = takeCommand().lower()
                func.weatherRequest(city, weather_Key)

            elif 'abri youtube' in query or 'abrir youtube' in query:
                youtubeURL = "https://www.youtube.com/"
                func.openWebsite(youtubeURL, driver)

            elif 'abri twitch' in query or 'abrir twitch' in query:
                twitchURL = "https://www.twitch.tv/"
                func.openWebsite(twitchURL, driver)

            elif 'quien es' in query or 'busca sobre' in query or 'wikipedia' in query or 'quiero saber sobre' in query:
                print('Hanna: Buscando...')
                speak("buscando...")
                func.getInformation(query)

            elif 'cancion' in query or 'canción' in query:
                print('Hanna: ¿que canción busco?')
                speak('¿que canción busco?')
                song = takeCommand().lower()
                print(f"Hanna: Buscando la cancion, {song}")
                speak(f"Buscando la cancion, {song}")
                t = threading.Thread(
                    target=func.playVideoOnYoutube, args=(song, driver,))
                t.start()
                #func.playVideoOnYoutube(song, driver)

            elif 'video' in query:
                print('Hanna: ¿Que video busco?')
                speak('¿que video busco?')
                video = takeCommand().lower()
                print(f"Hanna:  Buscando el video, {video}")
                speak(f"buscando la video, {video}")
                t = threading.Thread(
                    target=func.playVideoOnYoutube, args=(video, driver,))
                t.start()
                #func.playVideoOnYoutube(video, driver)

            elif 'eventos' in query or 'tengo algo' in query or 'calendario' in query:
                print("Hanna: Buscando eventos...")
                speak("Buscando eventos")
                func.getEvents(10, service)

            elif 'hay alguien haciendo stream' in query or 'quien esta en vivo' in query:
                func.checkStreamers()

            elif 'leeme los ultimos tweets' in query or 'leeme tweets' in query or 'léeme tweets' in query or 'léeme tweet' in query:
                func.getLatestTweets(api)

            elif 'cuales son las tendencias' in query or 'de que se habla en twitter' in query:
                func.getTrendsOnTwitter(api)

            elif 'tweeteá' in query or 'twiteá' in query or 'publicá un tweet' in query or 'publicá un twit' in query:
                func.publishTweet(api)

        elif 'gracias hanna' in query or 'listo hanna' in query or 'listo' in query or 'isto' in query:
            print('Hanna: Hasta luego!')
            speak('Hasta luego!')
            break
        else:
            pass
