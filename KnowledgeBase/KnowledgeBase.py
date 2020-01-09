import csv
import pprint

class KnowledgeBase():
    def __init__(self):
        
        

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
                    prev_question = row['Question']
                    first = False

                elif(row['Question'] != prev_question):
                    myDict.update({row['Question'] : row['Answer']})

            self.chatKnowledge.update(myDict)





# with open('QA1.csv', mode='r') as infile:
#     reader = csv.reader(infile)

#     mydict = {rows[0]:rows[1] for rows in reader}

#     pprint.pprint(mydict)