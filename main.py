import os
import datetime
import time
import pyaudio
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from playsound import playsound
from speech import *
import subprocess
import wikipedia


os.system('cls')

speak('Hola Tomás, ¿en que te puedo ayudar?')

def notetaking(text):
    speak('¿Que nombre le pongo?')
    noteName = command()
    note = (f"{noteName}.txt")
    with open(note, 'w') as f:
        f.write(text)
    subprocess.Popen(['notepad.exe', noteName])

if __name__=='__main__':
    speak('Hola')
    while True:
        query = command().lower()

        if 'anotá' in query or 'escribí una nota' in query or 'escribí un memo' in query:
            notetaking(query)
            speak('Listo!')
        elif 'Hola Hanna' in query:
            speak('Hola!, espero que estés bien')
