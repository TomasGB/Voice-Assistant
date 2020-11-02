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

speak("Hola Tomás, ¿en que te puedo ayudar?")

def notetaking(text):
    speak("¿Que nombre le pongo?")
    noteName = takeCommand()
    note = (f"{noteName}.txt")
    with open(note, 'w') as f:
        f.write(text)
    subprocess.Popen(['notepad.exe', noteName])

if __name__=='__main__':

    while True:
        query = takeCommand().lower()

        if 'gracias Hanna' in query or 'listo Hanna' in query or 'listo' in query:
            speak('Hasta luego!')
            exit()
        elif 'anotá' in query or 'escribí una nota' in query or 'escribí un memo' in query:
            speak('¿Que querés que escriba?')
            text = takeCommand()
            notetaking(text)
            speak('Listo!')
        elif 'hola' in query:
            speak('Hola!, espero que estés bien')
