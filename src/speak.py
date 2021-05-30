import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    audio = ''
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=1)
        print("Escuchando...")
        audio = r.listen(source, phrase_time_limit=4)
    try:
        text = r.recognize_google(audio,language='es-ES')
        print('You: ', text)
        return text
    except:
        print('...')
        return "none"
