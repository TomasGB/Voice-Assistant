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
from apiCredentials import twitchUser_ID, twitchUser_SECRET, twitter_key, twitter_keySecret, twitter_acces_token,twitter_acces_tokenSecret
import json
from twitchAPI import Twitch
import tweepy


pathChromeDriver = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(pathChromeDriver)


def openWebsite(website):
    driver.get(website)

def playVideoOnYoutube(text):

    driver.get("https://www.youtube.com/")
    driver.implicitly_wait(5)
    driver.find_element_by_name("search_query").send_keys(text)
    driver.find_element_by_id("search-icon-legacy").click()
    driver.implicitly_wait(6)
    driver.find_element_by_id("video-title").click()
    
    ads = 0
    while True and ads<3:
        try:
            skipBtn = driver.find_element_by_class_name('ytp-ad-skip-button-container')
            skipBtn.click()
            ads+=1
        except:
            ads+=1
            continue
    
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
        print(f"Hanna: {event['summary']}")
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
        print(f"Hanna: Hoy el clima en {city} es, {description} y hacen {temp} grados.")
        speak(f"Hoy el clima en {city}es, {description} y hacen {temp} grados.")

def checkStreamers():
    twitch = Twitch(twitchUser_ID, twitchUser_SECRET)
    twitch.authenticate_app([])

    streamers = ["alexelcapo","ibai", "babybouge","haannahr","sana","goncho","coscu"]

    for streamer in streamers:
        try:
            # get ID of user
            user_info = twitch.get_users(logins=[streamer])
            usuario_id = user_info['data'][0]['id']
            #check if it's live
            isLive = twitch.get_streams(user_id=usuario_id)

            counter=0
            if isLive['data'][0]['type'] == 'live':
                print(f'Hanna: {streamer}')
                speak({streamer})
                counter+=1
            
            if counter == 0:
                print('Hanna: Nadie esta stremeando')
                speak('Nadie esta stremeando')
            elif counter == 1:
                print('Hanna: Esta stremeando')
                speak('Esta stremeando')
            else:
                print('Hanna: Estan stremeando')
                speak('Estan stremeando')
        
        except:
            pass

def AuthTwitter():
    consumerKey = twitter_key
    consumerKeySecret = twitter_keySecret
    authTwitter = tweepy.OAuthHandler(consumerKey,consumerKeySecret)
    authTwitter.set_access_token(twitter_acces_token, twitter_acces_tokenSecret)
    api = tweepy.API(authTwitter, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    return api

def getLatestTweets(api):
	tweets = api.home_timeline(count=5)
	for status in tweets:
		print('-----------------------------------------------')
		print(f'@{status.user.screen_name}: {status.text}')
		speak(f'{status.user.screen_name}: {status.text}')

def getTrendsOnTwitter(api):
	ARGENTINA_WOE_ID = 468739
	argentina_trends = api.trends_place(ARGENTINA_WOE_ID)
	trends = json.loads(json.dumps(argentina_trends, indent=1))

	print('----------------------------------------------')
	for trend in trends[0]["trends"]:
		print (trend["name"])
		speak(trend["name"])

def publishTweet(api):
	print('Hanna: ¿Qué querés twitter?')
	speak('¿Qué querés twitter?')
	text = takeCommand().lower()
	print(f'hanna: vas a twittear, {text}')
	speak(f'Vas a twittear, {text}')
	
	print('Hanna: ¿Estás de acuerdo?')
	speak('¿Estás de acuerdo?')
	answ=takeCommand().lower()

	if answ == 'si' or answ == 'sí':
		api.update_status(f'{text}')
	else:
		pass