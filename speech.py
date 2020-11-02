import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', 165)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    audio = ''
    with sr.Microphone() as source:
        print('Listening...')
        audio = r.listen(source, phrase_time_limit=4)
    try:
        text = r.recognize_google(audio, language='en-US')
        print('You: ', text)
        return text
    except:
        print('...')
        return 'none'
    return text
