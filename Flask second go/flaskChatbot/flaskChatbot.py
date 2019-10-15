from flask import Flask, render_template
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
def home():
    return render_template('home.html', posts=posts)

@app.route("/chatbot")
def chatbot():
    return render_template('chatbot.html')
if __name__ == '__main__':
    app.run(debug=True)
