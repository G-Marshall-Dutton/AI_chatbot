from flask import Flask, render_template,request,make_response,jsonify
import json
from urllib.request import urlopen

from webScraper import webScraper
from nlp import nlp
from controller import controller

from VoiceControl import VoiceControl

import os
from gtts import gTTS

#Create flask shell
app = Flask(__name__)

# Initialize components (Controller, Reasoning Engine, Language Processing)
nlp = nlp.ReasoningEngine()
controller = controller.ConversationController(nlp)
voice_listener = VoiceControl.VoiceControl()




########################################################################
#
# Routes and Logic
#

# Initial SplashScreen
@app.route("/")
def index():

    # get users location on index page
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    city = data['city']
    loc = data['loc']
    print("Detected user city as " + city + " (" + loc + ")")

    # get nearest train station with google places api
    # coords format = 45.77940539999999%2C15.9516292
    locsplit = loc.split(',')
    coords = locsplit[0] + "%2C" + locsplit[1]
    g_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+coords+'&rankby=distance&type=train_station&key=AIzaSyCcTgfahn0CZbas24XqkKJbGd9n73_H_pE'
    g_response = urlopen(g_url)
    g_data = json.load(g_response)
    nearest_station = g_data['results'][0]['name']
    print("Nearest station (thanks Google) is " + nearest_station)

    # render page
    return render_template('index.html')



# Endpoint for communication... recieving and sending responses
@app.route("/chat", methods=['POST'])
def chat():
    
    # Reset status
    status = ''

    #Read in userInput as string
    userInput = request.get_json()['userMessage']

    # Active voice responses
    if(userInput == 'VOICE-ACTIVE'):
        controller.voiceActive = True
        return 'True'

    # Active voice responses
    if(userInput == 'VOICE-UNACTIVE'):
        controller.voiceActive = False
        return 'True'

    if(userInput == 'VOICE'):
        userInput = voice_listener.listen()
        print("HEARD:", userInput)
        response = controller.respond(userInput)
        string_response = isinstance(response, str )

        # Deal with normal string response from AI
        if string_response:
            # Save response as MP3
            tts = gTTS(text=response, lang='en')
            tts.save("response.mp3")
            response = make_response(jsonify({"answer": response, "question": userInput, "status" : "voiceChat"}), 200)
        # Deal with dict response from AI
        else:
            response = make_response(jsonify({"answer": response, "question": userInput, "status" : "ticketInfo"}), 200)

        # Play audio if voice active
        if(controller.voiceActive and string_response):
            # Play response.mp3 audio
            os.system("mpg321 response.mp3")

        return response

    # Pass the user input to the controller : respond deals with connection to NLP
    response = controller.respond(userInput)
    print("RESPONSE IS OF TYPE", type(response))

    # Determine if its a normal response or the scraped ticket info
    # Normal response
    if(isinstance(response, str )):
        str_response = True
        status = "ticketChat" 
        # Save response as MP3
        tts = gTTS(text=response, lang='en')
        tts.save("response.mp3")


    # Ticket info (stored in a dict)
    elif(isinstance(response, dict )):
        str_response = False
        status = "ticketInfo"

    
    response = make_response(jsonify({"answer": response, "status" : status}), 200)

    if(status == "ticketChat" and controller.voiceActive):
        # Play response.mp3 audio
        os.system("mpg321 response.mp3")

    return response
    

# Chatbot endpoint
@app.route("/chatbot")
def chatbot():
    greet = nlp.get_random_greeting()
    return render_template('chatbot.html', greeting = greet)

#
############################################################################

#RUN FLASK CHATBOT
app.run(debug=True)
