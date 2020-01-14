import spacy
import random
import dateparser
from decimal import *
from KnowledgeBase import KnowledgeBase

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from pandas import DataFrame
import re
import numpy as np

from delay_prediction import StationFinder

from datetime import timedelta
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
        self.kb = KnowledgeBase.KnowledgeBase()
        self.similarityThreshold = 0.05
        self.context_similarity_threshold = 0.3 # this was 0.15
        self.GREETINGS = ("Hello", "Hi", "Greetings")
        self.RESPONSES = ("... my day was fine thank for asking... *rolls eyes*", "WHY DO YOU ALWAYS JUST TALK AT ME", "It would be nice if you just listened to me for once...",
         "Well, that's awesome for someone like you", "I don't have the time nor the crayons to explain this to you.")

    def get_random_greeting(self):
        greeting = random.choice(self.GREETINGS) + ". I'm Thomas! I can help you with cheap train tickets and estimated arrival times, but you can ask me anything and I'll give you my best answer! So how can help?"
        return greeting

    def get_random_response(self):
        return random.choice(self.RESPONSES)

    # convert date to format needed for nationalrail (ddmmyy)
    def convert_date(self, d):
        
        # Check if date is given 'days'
        days_found = False
        if('days' in d):
            days_found = True
            elements = d.split(' ')
            days = elements[0]
            print(days)

        # user dateparser to parse the date into a python datetime, prefering futrue dates if ambiguous 
        parsed_date = dateparser.parse(d,settings={'PREFER_DATES_FROM': 'future'})

        if(days_found):
            days = int(days)*2
            parsed_date = parsed_date + timedelta(days=days)

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
        "I want to book a ticket",
        "can i book a train?",
        "can i book a ticket?",
        "can i book",
        "can i have",
        "ticket",
        "book",
        "reserve",
        "order",
        "i would like to book a train from cambridge to london",
        "when is the nearest tarin to bristol",
        "whats the cheapest train to birmingham",
        "find me a cheap train to newcastle",
        "i need a cheap and quick train to london tomorrow",
        "I need to get a train",
        "I need a train",
        "I need to catch a train",
        "find me train tickets",
        "find me chep trains",
        "find me cheap tickets"
    )

    delayInformation = (
        "I'm delayed",
        "i am delayed",
        "how long am i likely to be delayed?",
        "how late is ",
        "I'm late",
        "how much longer is this going to be?",
        "delay",
        "delayed",
        "late",
        "can you help me with my delay?",
        "how late am I likely to be?",
        "do you know when will I arrive",
        "when will i get there"
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
        "sure",
        "yup",
        "you got it"
        "uh huh",
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
        "not, that's not right",
        "nuh uh",
        "nope",
        "no way",
        "nowhere"
    )

    # KNOWLEDGE BASE-------------------------------------------------

  


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
        confident = False

        # determine if a BOOKING type
        typ = "booking"
        for previous in ReasoningEngine.trainInformation:
            example = nlp(previous)
            cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
            similarity = cleaned_sentence.similarity(cleaned_previous) 
            if similarity > best_score: 
                best_score = similarity
                print("SCORE BOOKING: ", Decimal(best_score))

                # Break if confident enough
                confident = best_score > 1 - self.context_similarity_threshold
                if(confident):
                    print("CONFIDENT")
                    break
              
        # determine if a DELAY type
        if not confident:
            for previous in ReasoningEngine.delayInformation:
                example = nlp(previous)
                cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
                similarity = cleaned_sentence.similarity(cleaned_previous) 
                if similarity > best_score:
                    best_score = similarity
                    print("SCORE DELAY: ", Decimal(best_score))
                    typ = "delay"
                    
                     # Break if confident enough
                    confident = best_score > 1 - self.context_similarity_threshold
                    if(confident):
                        print("CONFIDENT")
                        break

        # determine if a CHAT type
        if not confident:
            for q, a in self.kb.chatKnowledge.items():
                example = nlp(q)
                cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
                similarity = cleaned_sentence.similarity(cleaned_previous)
                if similarity > best_score:
                    best_score = similarity
                    print("SCORE CHAT: ", Decimal(best_score))
                    typ = "chat"
                    break

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
        confidence_threshold = 0.22

        # determine if a YES type
        for previous in ReasoningEngine.affirmationTypes:
            example = nlp(previous)
            cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
            similarity = cleaned_sentence.similarity(cleaned_previous)
            confident = similarity > 1- confidence_threshold  
            if similarity > best_score and confident:
                print("AFFIRMAION SIMILARITY", Decimal(similarity))
                best_score = similarity
                result = True

        # # determine if a NO type
        # for previous in ReasoningEngine.refutationTypes:
        #     example = nlp(previous)
        #     cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
        #     similarity = cleaned_sentence.similarity(cleaned_previous)
        #     if similarity > best_score:
        #         best_score = similarity
        #         result = False

        return result


    # return true if user replies with affirmation, else false
    def refutation(self, sentence):

        result = False
        
        sent = nlp(sentence)
        cleaned_sentence = nlp(' '.join([str(t) for t in sent if not t.is_stop]))
        best_score = 0
        confidence_threshold = 0.22

        # determine if a NO type
        for previous in ReasoningEngine.refutationTypes:
            example = nlp(previous)
            cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
            similarity = cleaned_sentence.similarity(cleaned_previous)
            confident = similarity > 1 - confidence_threshold 
            if similarity > best_score and confident:
                best_score = similarity
                result = True

        # # determine if a YES type
        # for previous in ReasoningEngine.affirmationTypes:
        #     example = nlp(previous)
        #     cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
        #     similarity = cleaned_sentence.similarity(cleaned_previous)
        #     if similarity > best_score:
        #         best_score = similarity
        #         result = False

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

            # If FROM and TO are both missing
            if(dict.get("from") is None and dict.get("to") is None):
                print("Adding a from ONLY")
                dict.update({"to": self.stationFinder.getCode(pnouns[0])})

            # if only FROM is missing
            elif(dict.get("from") is None and dict.get("to") is not None):
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
                    if(dict['from'] == dict['to']):
                        dict['from'] = None


        # otherwise if 2 pnouns found then determine to/from 
        elif len(pnouns) < 3 and len(pnouns) > 0:

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

            # Deal with pronouns we havent assigned yet
            if(dict['from'] is None):
                dict.update({"from": self.stationFinder.getCode(pnouns[0])})

            if(dict['to'] is None):
                dict.update({"to": self.stationFinder.getCode(pnouns[0])})

        # otherwise more than 2 pnouns found, so do nothing
        #else:
            #print("No proper nouns found")

        print("ABOUT TO PRINT ENTS")
        # iterate through entities (looking for DATE/TIME)
        for ent in doc.ents: 
            print("ENT IS:", ent.label_, ent.text)
            # date entity found, add to dictionary
            if(ent.label_ is "DATE"):
                formatted_date = self.convert_date(ent.text)
                dict.update({"date": formatted_date}) 

            # date entity found, add to dictionary
            if(ent.label_ is "TIME"):
                formatted_time = self.convert_time(ent.text)
                dict.update({"time": formatted_time}) 


        # if everything else is found except time and NER isn't picking it up, detect nums and dateparse them + neighbour
        if(dict.get("from") is not None and dict.get("to") is not None and dict.get("date") is not None and dict.get('time') is None):
            for token in doc:
                if token.pos_ is "NUM":
                    new_time = token.text + token.nbor(1).text
                    formatted_time = self.convert_time(new_time)
                    dict.update({"time": formatted_time}) 
                    


        # # Compare user input to knowledge base to determine appropriate response
        # sent = nlp(text)
        # cleaned_sentence = nlp(' '.join([str(t) for t in sent if not t.is_stop]))
        # best_score = 0

        # response = "DIDNT GET RESPONSE"
        # for q, a in self.kb.bookingKnowledge.items():
        #     example = nlp(q)
        #     cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
        #     if cleaned_sentence.similarity(cleaned_previous) > best_score:
        #         best_score = cleaned_sentence.similarity(cleaned_previous)
        #         response = a
        
        # return response



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

            # If FROM and TO are both missing
            if(dict.get("from") is None and dict.get("to") is None):
                print("Adding a from ONLY")
                dict.update({"to": self.stationFinder.getCode(pnouns[0])})

            # if only FROM is missing
            elif(dict.get("from") is None and dict.get("to") is not None):
                print("Adding a from ONLY")
                dict.update({"from": self.stationFinder.getCode(pnouns[0])})

            # if only TO is missing
            elif(dict.get("from") is not None and dict.get("to") is None):
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

        # if everything else is found except time and NER isn't picking it up, detect nums and dateparse them + neighbour
        if(dict.get("from") is not None and dict.get("to") is not None and dict.get("delay_mins") is not None and dict.get('planned_dep_time') is None):
            for token in doc:
                if token.pos_ is "NUM":
                    new_time = token.text + token.nbor(1).text
                    formatted_time = self.convert_time(new_time)
                    dict.update({"planned_dep_time": formatted_time}) 


    def get_chat_response(self, user_query):

        sent = nlp(user_query)
        cleaned_sentence = nlp(' '.join([str(t) for t in sent if not t.is_stop]))
        best_score = 0

        for q, a in self.kb.chatKnowledge.items():
            example = nlp(q)
            cleaned_previous = nlp(' '.join([str(t) for t in example if not t.is_stop]))
            similarity = cleaned_sentence.similarity(cleaned_previous)

            # THIS CODE IS JUST FOR DEBUGGING EMPTY VECTOR WARNING
            # if similarity == 0.0:
            #     print(cleaned_previous.text)
            #     input("Press Enter to continue...")
            if similarity > best_score:
                best_score = similarity
                response = a

                # Break if confident enough
                confident = best_score > 1 - self.similarityThreshold
                if(confident):
                    print("CONFIDENT")
                    print("SCORE CHAT RESPONSE: ", Decimal(best_score))
                    break
        
        return response


    def get_chat_response_from_model(self, user_query):
        print("RESPONDING FROM MODEL")

        # Generic words
        stops = stopwords.words('english')
        # used to reduce word to its lemma
        stemmer = SnowballStemmer('english')

        myDict = {'USER_QUERY' : user_query}
        df = DataFrame(list(myDict.items()),columns = ['USER QUERY','Question'])

        # Clean up data by removing stop words and reduce others to their lemma
        df['cleaned'] = df['Question'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in stops]).lower())

        user_query = df.cleaned[0]

        print("USER CLEANED:", user_query)


        # Predict answer from the model
        response = str(self.kb.chat_model.predict([user_query]))
        # Format string
        response = response.replace('[', '').replace(']','').replace('\'', '').replace('"','')
        return response


    def determine_context_from_model(self, user_query):
        print("DETERMINING CONTEXT FROM MODEL")

        # Generic words
        stops = stopwords.words('english')
        # used to reduce word to its lemma
        stemmer = SnowballStemmer('english')

        myDict = {'USER_QUERY' : user_query}
        df = DataFrame(list(myDict.items()),columns = ['USER QUERY','Question'])

        # Clean up data by removing stop words and reduce others to their lemma
        df['cleaned'] = df['Question'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in stops]).lower())

        user_query = df.cleaned[0]

        print("CONTEXT CLEANED:", user_query)


        # Predict answer from the model
        response = str(self.kb.context_model.predict([user_query]))
        # Format string
        response = response.replace('[', '').replace(']','').replace('\'', '').replace('"','')
        return response
