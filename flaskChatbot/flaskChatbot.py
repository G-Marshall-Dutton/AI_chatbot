from flask import Flask, render_template,request,make_response,jsonify
import json
from nlp import nlp
from controller import controller

#Create flask shell
app = Flask(__name__)

# Initialize components (Controller, Reasoning Engine, Language Processing)
controller = controller.ConversationController()
re = nlp.ReasoningEngine()


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

    # Trun message into '' (object with sentence and type ie. hello and chat, or i want train and question)
    query = re.classify_user_sentence(userInput)
    response=re.make_decision(query)


    # DO SOMETHING WITH USER MESSAGE
    #response = re.get_random_response()
    res = make_response(jsonify({"answer": response}), 200)

    return res
    

# Chatbot endpoint
@app.route("/chatbot")
def chatbot():
    greet = re.get_random_greeting()
    return render_template('chatbot.html', greeting = greet)

#
############################################################################

#RUN FLASK CHATBOT
app.run(debug=True)
