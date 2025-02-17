import spacy
import random
import dateparser
from decimal import *
from delay_prediction import StationFinder
#from controller import controller

#nlp = spacy.load("en_core_web_sm") #Load language model object (sm is small version)
nlp = spacy.load("en_core_web_lg") #Load language model object 

#sentence with type
class ClassifiedSentence:
    def __init__(self,sentence,typ):
        self.sentence = sentence
        self.type = typ

    def __str__(self):
        return self.sentence + " -> " + self.type


class ReasoningEngine:

    stationFinder = StationFinder.StationFinder()

    def __init__(self):
        # Sentences we'll respond with if the user greeted us
        self.GREETINGS = ("Hello", "Hi", "Greetings")
        self.RESPONSES = ("... my day was fine thank for asking... *rolls eyes*", "WHY DO YOU ALWAYS JUST TALK AT ME", "It would be nice if you just listened to me for once...",
         "Well, that's awesome for someone like you", "I don't have the time nor the crayons to explain this to you.")

    def get_random_greeting(self):
        return random.choice(self.GREETINGS)

    def get_random_response(self):
        return random.choice(self.RESPONSES)

    # convert date to format needed for nationalrail (ddmmyy)
    def convert_date(self, d):
        # user dateparser to parse the date into a python datetime
        parsed_date = dateparser.parse(d)

        # format output string
        date = parsed_date.strftime("%d%m%y")

        return date

    # convert time to format needed for nationalrail (hhmm 24)
    def convert_time(self, t):
        # user dateparser to parse the date into a python datetime
        parsed_time = dateparser.parse(t)

        time = parsed_time.strftime("%H%M")

        return time


    trainInformation = (
        "can i book a train?",
        "i would like to book a train from cambridge to london",
        "when is the nearest tarin to bristol",
        "whats the cheapest train to birmingham",
        "find me a cheap train to newcastle",
        "i need a cheap and quick train to london tomorrow"
    )

    delayInformation = (
        "i am delayed",
        "how long am i likely to be delayed?",
        "how late is my train?",
        "my train is late",
        "how much longer is this train going to be?",
        "delay",
        "late",
        "can you help me with my train delay?",
        "how late is my train likely to be?"
    )

    affirmationTypes = (
        "yes",
        "yeah",
        "that's right",
        "right",
        "correct",
        "that's right",
        "yep",
        "aye",
    )

    refutationTypes = (
        "no",
        "nah",
        "naw",
        "no thanks",
        "no, that's not right",
        "incorrect",
        "that's wrong",
        "no, that's wrong",
        "not, that's not right"
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

        # determine if a BOOKING type
        typ = "booking"
        for previous in ReasoningEngine.trainInformation:
            example = nlp(previous)
            cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
            if cleaned_sentence.similarity(cleaned_previous) > best_score: 
                best_score = cleaned_sentence.similarity(cleaned_previous)
                print("SCORE BOOKING: ", Decimal(best_score))
              
        # determine if a DELAY type
        for previous in ReasoningEngine.delayInformation:
            example = nlp(previous)
            cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
            if cleaned_sentence.similarity(cleaned_previous) > best_score:
                best_score = cleaned_sentence.similarity(cleaned_previous)
                print("SCORE DELAY: ", Decimal(best_score))
                typ = "delay"

        # determine if a CHAT type
        for previous in self.GREETINGS:
            example = nlp(previous)
            cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
            if cleaned_sentence.similarity(cleaned_previous) > best_score:
                best_score = cleaned_sentence.similarity(cleaned_previous)
                print("SCORE CHAT: ", Decimal(best_score))
                typ = "chat"

        # TODO: better way of classifying intent?

        # 'chat' or 'query' for now
        #print(typ)
        #return ClassifiedSentence(sentence,typ)
        return typ

    # return true if user replies with affirmation, else false
    def affirmation(self, sentence):

        result = False
        
        sent = nlp(sentence)
        cleaned_sentence = nlp(' '.join([str(t) for t in sent if not t.is_stop]))
        best_score = 0

        # determine if a YES type
        for previous in ReasoningEngine.affirmationTypes:
            example = nlp(previous)
            cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
            if cleaned_sentence.similarity(cleaned_previous) > best_score:
                best_score = cleaned_sentence.similarity(cleaned_previous)
                result = True

        # determine if a NO type
        for previous in ReasoningEngine.refutationTypes:
            example = nlp(previous)
            cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
            if cleaned_sentence.similarity(cleaned_previous) > best_score:
                best_score = cleaned_sentence.similarity(cleaned_previous)
                result = False

        return result
        

    # attempts to return journey info
    # FROM / TO / DATE-OUT / TIME-OUT
    # {from: to: date: time:}
    # TODO: controller will pass in a dict of what it knows, it is this functions job to try and identify information from the text, update the dictionary and return it
    def get_journey_info(self, text, dict):
        
        pnouns = [] # stores the proper nouns detected in the text, used to count and see if it's to/from or both
        pnouns_pos = []
        
        # convert to tokens
        doc = nlp(text)

        # keeps track of position through doc
        position = 0

        # iterate through tokens, store pronouns and positions
        for token in doc:
            
            # debug to display detected tokens
            #print("Token type is " + str(token.pos_) + " @ position " + str(position)) 
            
            # if proper noun is detected
            if token.pos_ is 'PROPN':

                # store all found pronouns
                pnouns.append(token.text)

                # store position of pnoun
                pnouns_pos.append(position)
                
            # update position through token iteration
            position = position + 1

        # check if one source/destination is missing, if so and only one pronoun found, must be it
        if(len(pnouns) == 1):

            #print("Only 1 pnoun detected")

            # if only FROM is missing
            if(dict.get("from") is None and dict.get("to") is not None):
                print("Adding a from ONLY")
                dict.update({"from": self.stationFinder.getCode(pnouns[0])})
                
            # if only TO is missing
            if(dict.get("from") is not None and dict.get("to") is None):
                print("Adding a to ONLY")
                dict.update({"to": self.stationFinder.getCode(pnouns[0])}) 

            # if only one value is found, check not in first position, because can't look at backward neighbour
            if(pnouns_pos[0] > 0):

                # if previous word is "from", then must be source 
                if(token.nbor(-1).text == "from"):
                    dict.update({"from": self.stationFinder.getCode(pnouns[0])})   # add to dict         

                # if previous word is "to", then must be destination
                if(token.nbor(-1).text == "to"):
                    dict.update({"to": self.stationFinder.getCode(pnouns[0])}) 


        # otherwise if 2 pnouns found then determine to/from 
        elif(len(pnouns) < 3):

            # loop through pnouns
            for i in range(len(pnouns)):

                # check not in first position, because can't look at backward neighbour
                if(pnouns_pos[i] > 0):

                    # if previous word is "from", then must be source 
                    if(doc[pnouns_pos[i]].nbor(-1).text == "from"):
                        dict.update({"from": self.stationFinder.getCode(pnouns[i])})   # add to dict         

                    # if previous word is "to", then must be destination
                    if(doc[pnouns_pos[i]].nbor(-1).text == "to"):
                        dict.update({"to": self.stationFinder.getCode(pnouns[i])}) 
        # otherwise more than 2 pnouns found, so do nothing
        #else:
            #print("No proper nouns found")


        # iterate through entities (looking for DATE/TIME)
        for ent in doc.ents: 

            # date entity found, add to dictionary
            if(ent.label_ is "DATE"):
                formatted_date = self.convert_date(ent.text)
                dict.update({"date": formatted_date}) 

            # date entity found, add to dictionary
            if(ent.label_ is "TIME"):
                formatted_time = self.convert_time(ent.text)
                dict.update({"time": formatted_time}) 

    # attempts to return delay info
    # FROM / TO / PLANNED_DEP_TIME / DELAY_MINS
    # TODO: controller will pass in a dict of what it knows, it is this functions job to try and identify information from the text, update the dictionary and return it
    def get_delay_info(self, text, dict):
        
        pnouns = [] # stores the proper nouns detected in the text, used to count and see if it's to/from or both
        pnouns_pos = []
        
        # convert to tokens
        doc = nlp(text)

        # keeps track of position through doc
        position = 0

        # iterate through tokens, store pronouns and positions
        for token in doc:
            
            # debug to display detected tokens
            #print("Token type is " + str(token.pos_) + " @ position " + str(position)) 
            
            # if proper noun is detected
            if token.pos_ is 'PROPN':

                # store all found pronouns
                pnouns.append(token.text)

                # store position of pnoun
                pnouns_pos.append(position)
                
            # update position through token iteration
            position = position + 1

        # check if one source/destination is missing, if so and only one pronoun found, must be it
        if(len(pnouns) == 1):

            print("Only 1 pnoun detected")

            # if only FROM is missing
            if(dict.get("from") is None and dict.get("to") is not None):
                print("Adding a from ONLY")
                dict.update({"from": self.stationFinder.getCode(pnouns[0])})

            # if only TO is missing
            if(dict.get("from") is not None and dict.get("to") is None):
                print("Adding a to ONLY")
                dict.update({"to": self.stationFinder.getCode(pnouns[0])}) 

            # if only one value is found, check not in first position, because can't look at backward neighbour
            if(pnouns_pos[0] > 0):

                # if previous word is "from", then must be source 
                if(token.nbor(-1).text == "from"):
                    dict.update({"from": self.stationFinder.getCode(pnouns[0])})   # add to dict         

                # if previous word is "to", then must be destination
                if(token.nbor(-1).text == "to"):
                    dict.update({"to": self.stationFinder.getCode(pnouns[0])}) 


        # otherwise if 2 pnouns found then determine to/from 
        elif(len(pnouns) < 3):            

            # loop through pnouns
            for i in range(len(pnouns)):

                # check not in first position, because can't look at backward neighbour
                if(pnouns_pos[i] > 0):

                    # if previous word is "from", then must be source 
                    if(doc[pnouns_pos[i]].nbor(-1).text == "from"):
                        dict.update({"from": self.stationFinder.getCode(pnouns[i])})   # add to dict         
                        print("from added")

                    # if previous word is "to", then must be destination
                    if(doc[pnouns_pos[i]].nbor(-1).text == "to"):
                        dict.update({"to": self.stationFinder.getCode(pnouns[i])}) 
                        print("to added")
                   

        # otherwise more than 2 pnouns found, so do nothing
        #else:
            #print("No proper nouns found")

        # iterate through entities, looking for time entity
        if(dict.get("planned_dep_time") is None):
            
            for ent in doc.ents: 

                # date entity found, add to dictionary
                if(ent.label_ is "TIME"):
                    print("FOUND A TIME")
                    converted_time = self.convert_time(ent.text)
                    dict.update({"planned_dep_time": converted_time}) 

        else:
            # iterate through entities, looking for current delay
            for token in doc: 

                # date entity found, add to dictionary
                if(token.pos_ is "NUM"):
                    dict.update({"delay_mins": token.text}) 
