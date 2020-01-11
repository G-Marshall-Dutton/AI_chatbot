import csv
import pprint

import pandas as pd
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2


class KnowledgeBase():
    def __init__(self):
        
        self.to_responses = [
            'Where are you going?',
            'Where would you like to go?',
            'Where are you traveling to?',
            'Where are you headed?',
        ]

        self.from_responses= [
            'Where are you coming from?',
            'Where are you traveling from?',
            'Which station are you coming from?',
            'travelling from where?',
        ]

        self.dep_time_responses = [
            'When would you like to leave?',
            'What time do you want to leave?',
            'What time would you like to depart?',
            'Departing at what time?'
        ]

        self.date_responses = [
            'What date would you like to travel?',
            'What date is this for?',
            'Can I have the date you\'re leaving?',
            'When are you traveling?'
        ]


        self.delay_to_responses = [
            'Where are you going?',
            'Which station are you traveling to?',
            'Where are you traveling to?',
            'Where are you headed?',
        ]

        self.delay_dep_time_responses = [
            'When was your train supposed to depart?',
            'What time was your train scheduled to depart?',
            'When was the train supposed to leave?'
        ]

        self.delayed_by_responses = [
            'How long has your journey been delayed so far?',
            'How delayed are you at the moment?',
            'How many minutes are you delayed?',
            'For roughly how long have you been delayed?'

        ]

        self.chatKnowledge = {

        }

        


        self.bookingKnowledge = {
            'Can I book a train' : 'Sure thing! Where are you going?',
            'I want to go to' : 'where would you like to go?' 
        }


        self.delayKknowledge = {

        }

        #self.readCSV()
        self.readTSV()
        self.chat_model = self.trainModel()



    # Fills self.chatKnowledge with additional question answers pairs from QA1.csv
    def readCSV(self):
       
        with open('QA1.csv', mode='r') as infile:
            reader = csv.reader(infile)

            for rows in reader:
                self.chatKnowledge.update({rows[0]:rows[1]}) 



    def readTSV(self):
        with open('qna_chitchat_witty.tsv') as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            
            first = True
            myDict ={}

            for row in reader:

                if(first):
                    myDict.update({row['Question'] : row['Answer']})
                    prev_answer = row['Answer']
                    first = False

                elif(row['Answer'] != prev_answer):
                    prev_answer = row['Answer']
                    myDict.update({row['Question'] : row['Answer']})
            
            self.chatKnowledge.update(myDict)
            print("DICT LENGTH:", len(myDict))


    # FAILED ATTEMPT AT SPEED IMPROVMENT
    # COMBINES QUESTIONS WITH THE SAME ANSWER INTO THE SAME KEY TO REDUCE DICT SIZE WITHOUT LOOSING ANY INFORMATION
    def readTSV2(self):
        with open('qna_chitchat_witty.tsv') as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            
            first = True
            myDict ={}

            for row in reader:
                current_question = row['Question']
                current_answer = row['Answer']
               
                if(first):
                    key_string = row['Question']
                    prev_question = row['Question']
                    prev_answer = row['Answer']
                    first = False

                # Update key string if answers match
                elif(current_answer == prev_answer):
                    key_string = key_string + ' ' + current_question
                
                else:
                    myDict.update({key_string : prev_answer})
                    prev_answer = current_answer
                    key_string = current_question

            pprint.pprint(myDict)
            self.chatKnowledge.update(myDict)
            print("DICT LENGTH:", len(myDict))



    def trainModel(self):
        print('BUILDING MODEL...')

        # Read all data into pandas DataFrame
        data1 = pd.read_csv('qna_chitchat_witty.tsv', sep='\t')

        # Read additional data into pandas DataFrame
        data2 = pd.read_csv('QA1.csv')

        # Combine datasets
        data = pd.concat([data1, data2])

        # Generic words
        stops = stopwords.words('english')
        # used to reduce word to its lemma
        stemmer = SnowballStemmer('english')

        # Clean up data by removing stop words and reduce others to their lemma
        data['cleaned'] = data['Question'] #.apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in stops]).lower())

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(data['cleaned'], data.Answer, test_size=0.2)

        # Initialise training pipeline
        #
        # TfidVectorizer() : Vectorises each training example. Also applies a weight to each word, high weighting form uncommon words, low weighting for common words
        #                    ngrem_range(1, 2) - Compares each word individually as well as pairs of consecutive words
        #
        # SelectKBest()    : Decides on the best features in our data by determining the level of dependancy those features have on one another. 
        #                    Features with low dependancies are assigned a higher weighting than those with high dependancies.
        #                    Uses chi2 ('chi squared') algorithm to determine k best features
        #
        # LinearSVC()      : This is the classifier
        pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True, analyzer = 'word')), 
                             ('chi',  SelectKBest(chi2, k='all')),
                             ('clf', LinearSVC(C=1.5, penalty='l2', max_iter=7000, dual=False))])



        model = pipeline.fit(X_train, y_train)
        print('MODEL BUILT.')
        print('TESTING ACCURACY...')
        print('ACCURACY:', model.score(X_test, y_test))
        #input('PRESS ENTER TO CONTINUE...')

        return model



        # 74.33% - (1,1) , 'all' , max_iter=7000
