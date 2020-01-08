from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

# holds training data
# TODO: export to seperate file???
training_set = [
    # booking request
    ('i want to book a ticket', 'book'),
    ('i would like to book a ticket', 'book'),
    ('can i please book a ticket', 'book'),

    # timetable request
    ('what times do the trains run from', 'timetable'),
    ('when does the train for x leave', 'timetable'),
    ('what time does the train for x depart', 'timetable'),
    ('when does the train for x arrive', 'timetable'),

    # help request
    ('i need some help', 'help'),
    ('how do i use this', 'help')
]

# setup and train classifier
classifier = NaiveBayesClassifier(training_set)

while(True):
    userInput = input("Enter text: ")
    classifiedUserInput = classifier.classify(userInput)
    print("Classified as: " + classifiedUserInput)







