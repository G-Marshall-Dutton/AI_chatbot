from flask import Flask, render_template,request,make_response,jsonify
import json
import sys
sys.path.append('/Users/georgemarshall-dutton/AI_chat_bot/nlp')
import spacy_test


app = Flask(__name__)

re = spacy_test.ReasoningEngine()

@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html')


# Wont use this template, but can refference for flask loops
@app.route("/home-old")
def home():
    return render_template('home.html')



# Endpoint for communication... recieving and sending responses
@app.route("/chat", methods=['POST'])
def chat():
    data = request.get_json()['userMessage']
    
    # DO SOMETHING WITH USER MESSAGE
    response = re.getRandomPassAggResponse()
    res = make_response(jsonify({"answer": response}), 200)

    return res
    


@app.route("/chatbot")
def chatbot():
    greet = re.getRandomGreeting()
    return render_template('chatbot.html', greeting = greet)




if __name__ == '__main__':
    app.run(debug=True)
