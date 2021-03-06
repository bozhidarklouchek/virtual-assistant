from pywhatkit.main import playonyt
import speech_recognition as sr                              # So voice can be recognized
from gtts import gTTS                                        # So the program can ssave .mp3 files
from playsound import playsound                              # So can run .mp3 files
# from datetime import datetime                              # So can tell the date/time
import requests, json                                        # required for Weather API (general use)
# import pywhatkit                                           # Required for YT videos, general info and lookup

import urllib.request                                        # Creating url's
import urllib.parse                                          # Creating url's
import re                                                    # Regex
import os

import webbrowser                                            # Required for YT videos

import geocoder


from capitals.capitals import getCapitalOrCountryName          # To find a capital/country given a capital/country
from dateAndTime.date import getDate                           # So can say the date
from dateAndTime.time import getTime, findCorrectCity
                                                               # So can say the time and timezones
from weather.weather import getWeather, findCorrectCityAndHour                         # So can tell the weather
from funFacts.facts import getFact                             # So can say fun facts
from jokes.jokes import getJoke                                # So can say jokes
from youtubeVideos.videos import clearRequest


def take_command():
    recognizeSpeech = sr.Recognizer()

    # Reading Microphone as source
    # listening the speech and store in audio_text variable

    with sr.Microphone() as source:
        spokenWords = ""
        # print("Talk")
        audio_text = recognizeSpeech.listen(source)
        # print("Time over, thanks")
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using google speech recognition
            spokenWords = recognizeSpeech.recognize_google(audio_text)
            # print("Text: " + spokenWords) #add    , language = "bg-BG"   for bg
        except: pass          
    return spokenWords


def run_bot():
    try:
        command = take_command()
    except:
        talk("Sorry, I did not get that - is your connection alright?")
        return 0
    toSay = "I'm so sorry! I couldn't understand you."
    # print(command)
    if("repeat" in command):
        repeat()

    elif("capital" in command):
        toSay = getCapitalOrCountryName(command)
        talk(toSay)

    elif("weather" in command):
        result = getWeather(command)
        if(type(result) == type("String")):
            talk(result)
        elif(type(result) == type(['list'])):
            talk("Sorry, are you asking about the weather in ")
            for i in range(len(result)):
                currCity = result[i][0]
                currCountry = result[i][1]
                talk(currCity + " in " + currCountry)
                if(i != len(result) - 1):
                    talk("or in")
            command = take_command()
            toSay = findCorrectCityAndHour(command, result)
            talk(toSay)

    elif("time" in command):
        result = getTime(command)
        if(type(result) == type("String")):
            talk(result)
        elif(type(result) == type(['list'])):
            talk("Sorry, are you asking about the time in ")
            for i in range(len(result)):
                currCity = result[i][0]
                currCountry = result[i][1]
                talk(currCity + " in " + currCountry)
                if(i != len(result) - 1):
                    talk("or in ")
            command = take_command()
            toSay = findCorrectCity(command, result)
            talk(toSay)

    elif("date" in command or ("what" in command and "today" in command)):
        toSay = getDate()
        talk(toSay)

    elif(("fun" in command and "fact" in command) or ("something" in command and "interesting" in command)):
        toSay = getFact()
        talk(toSay)

    elif(("joke" in command) or ("something" in command and "funny" in command) or ("pun" in command)):
        toSay = getJoke()
        talk(toSay)

    elif("play" in command):
        toBeSearched = clearRequest(command)
        if(toBeSearched == ""):
            talk("Sorry, I didn't get what you want me to play.")
        else:
            talk("Certainly! Let me find it in YouTube")
            playVideo(toBeSearched)

    else:
        talk(toSay)



def talk(toSay):
    try:
        os.remove("reply.mp3")
    except:
        pass
    # Free up audio resource
    toSpeak = gTTS(text=toSay, lang="en", slow=False)
    toSpeak.save("reply.mp3")
    
    # Playing the converted file and then 
    playsound('reply.mp3')
    

def repeat():
    repeatIntro = "The last thing I said was"
    try:
        os.remove("repeat.mp3")
    except:
        pass
    toSpeak = gTTS(text=repeatIntro, lang="en", slow=False)
    toSpeak.save("repeat.mp3")
    playsound('repeat.mp3')
    playsound('reply.mp3')

def playVideo(toBeSearched):
    # print(toBeSearched)
    query_string = urllib.parse.urlencode({"search_query" : toBeSearched})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'watch\?v=(\S{11})', html_content.read().decode())
    videoURL = "http://www.youtube.com/watch?v=" + search_results[0]
    webbrowser.open(videoURL, new=0, autoraise=True)

