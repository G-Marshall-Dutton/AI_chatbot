from flask import Flask, render_template, request
app = Flask(__name__)

posts = [
    {
        'author': 'George Orwell',
        'title': '1984',
        'content': 'First Post Content',
        'date_posted': 'October 15, 2019'
    },
    {
        'author': 'Cormac Mccarthy',
        'title': 'The Road',
        'content': 'Second Post Content',
        'date_posted': 'October 15, 2019'
    }

]

@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html')


# Wont use this template, but can refference for flask loops
@app.route("/home-old")
def home():
    return render_template('home.html', posts=posts)



@app.route("/chatbot")
def chatbot():

    AI_response = "JEZ"

    return render_template('chatbot.html', response=AI_response)


# Runs after text is sent on GUI
@app.route('/send_request_to_AI', methods=["GET"])
def background_process_test():
    userQuery = request.args.get('text')

    
    return userQuery




if __name__ == '__main__':
    app.run(debug=True)
