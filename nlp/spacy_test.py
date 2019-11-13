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
    def __init__(self,sentence,type):
        self.sentence = sentence
        self.type = type



class ReasoningEngine:

    def __init__(self):
        # Sentences we'll respond with if the user greeted us
        self.GREETINGS = ("hello", "hi", "greetings", "sup", "what's up","It's so nice to see not everyone is obsessed with appearances", "hey")
        self.RESPONSES = ("... my day was fine thank for asking... *rolls eyes*", "WHY DO YOU ALWAYS JUST TALK AT ME", "It would be nice if you just listened to me for once...",
         "Well, that's awesome for someone like you", "I don't have the time nor the crayons to explain this to you.")

    def getRandomGreeting(self):
        return random.choice(self.GREETINGS)

    def getRandomPassAggResponse(self):
        return random.choice(self.RESPONSES)

    #respond to sentence based on type
    def respond(self,query):
        if(query.type == "greeting"):
            print(random.choice(self.GREETINGS))
        else:
            print("wat...")

    #assign sentence a type (greeting or not)
    def classify_user_sentence(self,sentence):
        for word in sentence.split():
            if word.lower() in self.GREETINGS:
                return Query(sentence,"greeting")
        return Query(sentence,None)

    #userInput = input("INTRODUCE YOURSELF: ")
    #respond(classify_user_sentence(userInput))

# creating Dialogue
# from spacy.tokens import Doc
# words = ["hello", "world", "!"]
# spaces = [True, False, False]
# doc = Doc(nlp.vocab, words=words, spaces=spaces)

# print(doc)