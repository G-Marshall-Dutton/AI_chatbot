from flask import Flask, render_template,request,make_response,jsonify
import json
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
    return render_template('index.html')

# Endpoint for communication... recieving and sending responses
@app.route("/chat", methods=['POST'])
def chat():
    #Read in userInput as string
    userInput = request.get_json()['userMessage']

    # Pass the user input to the controller : respond deals with connection to NLP
    response = controller.respond(userInput)
    response = make_response(jsonify({"answer": response}), 200)
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
