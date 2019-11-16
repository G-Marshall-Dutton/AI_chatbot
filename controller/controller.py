from durable.lang import *



# with ruleset('have_all_train_info'):
#     @when_all(c.to << m.to != '',
#               c.frm << m.frm != '')
#     # the event pair will only be observed once
#     def getTicket(c):
#         print('Getting Ticket for journey...')
#         print('%15s:%10s\n%15s:%10s'%('Leaving From',c.frm.frm,'Arriving At',c.to.to))
        

class ConversationController():
    def __init__(self):
        self.state = {}
        self.response_needed = 4
        self.state_confirmed = False


    # Updates state
    def update_state(self, newInfo):
        self.state.update(newInfo)

    # Dertermnine what kind of question was asked. i.e. was it train related?
    def determine_topic(self, user_query):
        return "train"

    # Extracts state relevant info and updates state
    def extract_info(self, user_query):
        # Get info
        # Update state
        return True

    # Determine train specific response based on self.state
    def determine_train_response(self):

        # If state confirmed
        if self.state_confirmed:

            # web scrape info 
            return "web scraped info"

        # If state is not full
        elif (len(self.state) < self.response_needed):

            # Acquire more info
            if not 'to' in self.state:
                response = "Where are you traveling to?"
            elif not 'from' in self.state:
                response = "Where are you traveling from?"
            elif not 'date' in self.state:
                response = "What date do you want to travel?"
            elif not 'time' in self.state:
                response = "What time would you like to leave?"

            return response

        # If we have all the needed info, confirm its correct
        elif not self.state_confirmed:
            return "So you want to travel from %s to %s on the %s at %s" % (self.state['to'], self.state['from'], self.state['date'], self.state['time'])

    
    def respond(self, user_query):
        topic = self.determine_topic(user_query)
        if topic is "train":
            self.extract_info(user_query)
            response = self.determine_train_response()
        else:
            response = "General chit chat"
        
        return response
    
    # Takes in a dictionary where keys are fields we can use to specify train ticket details ie( 'to' , 'frm' , 'time' ....)
    # def updateKnowledge(self,newKnowledge): 
    #     for field in newKnowledge:
    #         self.knowledge.update(newKnowledge)
    #         print("ADDED -> ",newKnowledge)
    #         #Update ruleset with new data
    #         post('have_all_train_info', {field:newKnowledge.get(field)})




# controller = ConversationController()
# controller.updateKnowldge({'to':"norwich"})
# controller.updateKnowldge({'frm':"bristol"})