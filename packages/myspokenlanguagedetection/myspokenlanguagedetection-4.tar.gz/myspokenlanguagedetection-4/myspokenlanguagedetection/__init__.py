import glob
import speech_recognition as sr
from langdetect import detect
from langdetect import detect_langs
import numpy as np

def myspolangdet(m,p):
    soundi=p+"/"+m+".wav"
    AUDIO_FILE = (soundi)
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        r.energy_threshold = 50
        r.dynamic_energy_threshold = False
        audio = r.record(source, duration=15) # read the entire audio file
    variables = ["en-US", "es-ES", "fr-FR", "it-IT", "de-DE", "pt-PT", "ru-RU","sv-SE","ja-JP"]
    for y in variables:
        try:
            x=r.recognize_google(audio,language = y)
            now=len(x.split())
            if now>20:
                b=detect_langs(x)
                c=detect(x)
                if c=="fr":
                    c="French"
                elif c=="en":
                    c="English"
                elif c=="es":
                    c="Spanih"
                elif c=="it":
                    c="Italian"
                elif c=="de":
                    c="Deutsch"
                elif c=="ru":
                    c="Russian"
                elif c=="pt":
                    c="Portuguese"
                elif c=="sv":
                    c="Swedish"
                elif c=="jp":
                    c="Japanese"
                else:
                    c="Out of the list"
                print("probability degree:", b)
                print("the language could be:",c)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Speech Recognition service; {0}".format(e))   
