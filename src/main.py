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
import triggers as trig
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

        if query in trig.WAKE_TRIGGERS:
            print("Hanna: Hola , ¿en que te puedo ayudar?")
            speak("Hola, ¿en que te puedo ayudar?")
            query = takeCommand().lower()

            if  query in trig.NOTE_TAKING_TRIGGERS:
                print('Hanna: ¿Que querés que escriba?')
                speak('¿Que querés que escriba?')
                text = takeCommand().lower()
                print('Hanna: ¿Que nombre le pongo?')
                func.takeNote(text)
                speak('Listo!')

            elif query in trig.TIME_TRIGGERS:
                currentTime = datetime.datetime.now().strftime("%H:%M")
                print(f"Hanna: Son las, {currentTime}, horas")
                speak(f"Son las, {currentTime}, horas")

            elif query in trig.DAY_TRIGGERS:
                currentDate = datetime.datetime.now().strftime("%d, del ,%m")
                print(f"Hanna: Hoy es el, {currentDate}")
                speak(f"Hoy es el, {currentDate}")

            elif query in trig.WHEATHER_TRIGGERS:

                print('Hanna: ¿En que ciudad?')
                speak('¿En que ciudad?')

                city = takeCommand().lower()
                func.weatherRequest(city, weather_Key)

            elif query in trig.YOUTUBE_TRIGGERS:
                youtubeURL = "https://www.youtube.com/"
                func.openWebsite(youtubeURL, driver)

            elif query in trig.TWITCH_TRIGGERS:
                twitchURL = "https://www.twitch.tv/"
                func.openWebsite(twitchURL, driver)

            elif query in trig.WIKIPEDIA_TRIGGERS:
                print('Hanna: Buscando...')
                speak("buscando...")
                func.getInformation(query)

            elif query in trig.SONG_TRIGGERS:
                print('Hanna: ¿que canción busco?')
                speak('¿que canción busco?')
                song = takeCommand().lower()
                print(f"Hanna: Buscando la cancion, {song}")
                speak(f"Buscando la cancion, {song}")
                t = threading.Thread(
                    target=func.playVideoOnYoutube, args=(song, driver,))
                t.start()
                #func.playVideoOnYoutube(song, driver)

            elif query in trig.VIDEO_TRIGGERS:
                print('Hanna: ¿Que video busco?')
                speak('¿que video busco?')
                video = takeCommand().lower()
                print(f"Hanna:  Buscando el video, {video}")
                speak(f"buscando la video, {video}")
                t = threading.Thread(
                    target=func.playVideoOnYoutube, args=(video, driver,))
                t.start()
                #func.playVideoOnYoutube(video, driver)

            elif query in trig.GOOGLE_CALENDAR_TRIGGERS:
                print("Hanna: Buscando eventos...")
                speak("Buscando eventos")
                func.getEvents(10, service)

            elif query in trig.CHECK_STREAMERS_TRIGGERS:
                func.checkStreamers()

            elif query in trig.READ_TWEETS_TRIGGERS:
                func.getLatestTweets(api)

            elif query in trig.READ_TRENDS_TRIGGERS:
                func.getTrendsOnTwitter(api)

            elif query in trig.PUBLISH_TWEET_TRIGGERS:
                func.publishTweet(api)

        elif query in trig.SLEEP_TRIGGERS:
            print('Hanna: Hasta luego!')
            speak('Hasta luego!')
            break
        else:
            pass
