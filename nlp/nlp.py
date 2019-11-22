import spacy
import random
#from controller import controller

nlp = spacy.load("en_core_web_sm") #Load language model object (sm is small version)
#controller = controller.ConversationController()

#sentence with type
class ClassifiedSentence:
    def __init__(self,sentence,typ):
        self.sentence = sentence
        self.type = typ

    def __str__(self):
        return self.sentence + " -> " + self.type


class ReasoningEngine:

    def __init__(self):
        # Sentences we'll respond with if the user greeted us
        self.GREETINGS = ("Hello", "Hi", "Greetings")
        self.RESPONSES = ("... my day was fine thank for asking... *rolls eyes*", "WHY DO YOU ALWAYS JUST TALK AT ME", "It would be nice if you just listened to me for once...",
         "Well, that's awesome for someone like you", "I don't have the time nor the crayons to explain this to you.")

    def get_random_greeting(self):
        return random.choice(self.GREETINGS)

    def get_random_response(self):
        return random.choice(self.RESPONSES)


    trainInformation = (
        "can i book a train?",
        "i would like to book a train from cambridge to london",
        "when is the nearest tarin to bristol",
        "whats the cheapest train to birmingham",
        "find me a cheap train to newcastle",
        "i need a cheap and quick train to london tomorrow"
    )


    def make_decision(self,classifiedSentence):
        # is looking for train ticket? if query.type == 'query'
        if classifiedSentence.type == 'query':
            self.extract_information_from_classified_sentence(classifiedSentence)
            return random.choice(ReasoningEngine.trainInformation)
        # is wanting train delay prediction? if query.type == 'delay'

        # is just chatting
        if classifiedSentence.type == 'chat':
            return random.choice(self.GREETINGS)


    #assign sentence a type (greeting or not)
    def classify_user_sentence(self,sentence):
        sent = nlp(sentence)
        cleaned_sentence = nlp(' '.join([str(t) for t in sent if not t.is_stop]))
        best_score = 0
        typ = "booking"
        for previous in ReasoningEngine.trainInformation:
            example = nlp(previous)
            cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
            if cleaned_sentence.similarity(cleaned_previous) > best_score:
                best_score = cleaned_sentence.similarity(cleaned_previous)

        for previous in self.GREETINGS:
            example = nlp(previous)
            cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
            if cleaned_sentence.similarity(cleaned_previous) > best_score:
                typ = "chat"

        # TODO: add delay
        # TODO: better way of classifying intent?

        # 'chat' or 'query' for now
        print(typ)
        return ClassifiedSentence(sentence,typ)

    # attempts to return journey info
    # FROM / TO / DATE-OUT / TIME-OUT
    # {frm: to: date: time:}
    # TODO: controller will pass in a dict of what it knows, it is this functions job to try and identify information from the text, update the dictionary and return it
    def get_journey_info(self, text, dict):
        doc = nlp(text)
        for token in doc:
            print("Token is:" + str(token.pos_))
            #if token.pos_ is 'PROPN':
            #    print("PNOUN is: " + str(token.text))
              


    # OLD CODE
    # def extract_information_from_classified_sentence(self, classifiedSentence):
    #     query = classifiedSentence
    #     knowledge = {}

    #     #MANUALLY CHECK FOR DESTINATION AND DEPARTURE THROUGH PARSE 
    #     if query.sentence.find("to")!=-1:
    #         print(query.sentence.find("to"))
    #         to = query.sentence.split("to")[1].split(" ")[1] # please ignore how bad this is.... please
    #         knowledge.update({"to":to})
    #     if query.sentence.find("from")!=-1:
    #         frm = query.sentence.split("from")[1].split(" ")[1] # please ignore how bad this is.... please
    #         knowledge.update({"frm":frm})

    #     #controller.updateKnowledge(knowledge)

