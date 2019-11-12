import spacy
import random


nlp = spacy.load("en_core_web_sm") #Load language model object (sm is small version)

# call object on our text, returns a 'Doc'
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

# print("%s" %(spacy.explain("IN")))
# for token in doc:
#     print("%10s%10s%10s%10s%10s%10s%10s%10s" %(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#             token.shape_, token.is_alpha, token.is_stop))
    # Text: The original word text.
    # Lemma: The base form of the word.
    # POS: The simple part-of-speech tag.
    # Tag: The detailed part-of-speech tag.
    # Dep: Syntactic dependency, i.e. the relation between tokens.
    # Shape: The word shape – capitalization, punctuation, digits.
    # is alpha: Is the token an alpha character?
    # is stop: Is the token part of a stop list, i.e. the most common words of the language?


#sentence with type
class Query:
    def __init__(self):
        self.sentence = None
        self.type = None
    def __init__(self,sentence,type):
        self.sentence = sentence
        self.type = type



# Sentences we'll respond with if the user greeted us
GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up","sup bro", "hey")

#respond to sentence based on type
def respond(query):
    if(query.type == "greeting"):
        print(random.choice(GREETING_KEYWORDS))
    else:
        print("wat...")

#assign sentence a type (greeting or not)
def classify_user_sentence(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_KEYWORDS:
            return Query(sentence,"greeting")
    return Query(sentence,None)

userInput = input("INTRODUCE YOURSELF: ")
respond(classify_user_sentence(userInput))


# creating Dialogue
# from spacy.tokens import Doc
# words = ["hello", "world", "!"]
# spaces = [True, False, False]
# doc = Doc(nlp.vocab, words=words, spaces=spaces)

# print(doc)