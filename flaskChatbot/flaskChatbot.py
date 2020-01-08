from flask import Flask, render_template,request,make_response,jsonify
import json
from urllib.request import urlopen

from webScraper import webScraper
from nlp import nlp
from controller import controller



#Create flask shell
app = Flask(__name__)

# Initialize components (Controller, Reasoning Engine, Language Processing)
nlp = nlp.ReasoningEngine()
controller = controller.ConversationController(nlp)





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
    #Read in userInput as string
    userInput = request.get_json()['userMessage']

    # Pass the user input to the controller : respond deals with connection to NLP
    response = controller.respond(userInput)

    # Determine if its a normal response or the scraped ticket info
    # Normal response
    if(isinstance(response, str )):
        status = "ticketChat" 
    # Ticket info (stored in a dict)
    elif(isinstance(response, dict )):
        status = "ticketInfo"


    response = make_response(jsonify({"answer": response, "status" : status}), 200)
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
