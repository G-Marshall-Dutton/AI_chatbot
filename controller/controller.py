        

class ConversationController():
    def __init__(self, nlp):
        # Chat : Booking : Delay 
        self.nlp = nlp
        self.context = "Chat"
        self.state = {
            'from': None,
            'to': None,
            'date': None,
            'time': None,
        }
        print("!!%s", self.state.keys())
        for k, v in self.state.items():
            print(k, v)

        self.response_needed = 4
        self.state_confirmed = False


    # Updates state
    def update_state(self, newInfo):
        self.state.update(newInfo)

    def state_not_full(self):
        for k, v in self.state.items():
            print(k, v)
            if v is None:
                return True

        return False

    
    # # Dertermnine context of user query : will return 'chat' , 'booking' , 'delay'
    # def determine_context(self, user_query):
    #     # Pass to NLP 
    #     context = nlp.
    #     return context
        
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
        elif self.state_not_full():
            response = "COULDNT GET APPROPRIATE RESPONSE"
            print("None in self.state")
            # Acquire more info
            if self.state['to'] is None:
                response = "Where are you traveling to?"

            elif self.state['from'] is None:
                response = "Where are you traveling from?"

            elif self.state['date'] is None:
                response = "What date do you want to travel?"

            elif self.state['time'] is None:
                response = "What time would you like to leave?"

            return response

        # If we have all the needed info, confirm its correct
        elif not self.state_confirmed:
            return "So you want to travel from %s to %s on the %s at %s?" % (self.state['to'], self.state['from'], self.state['date'], self.state['time'])

    # Determine how to respond
    def respond(self, user_query):
        print('In controller.respond()')
        print(self.state)

        # Recieve context from NLP : 'chat' , 'booking' , 'delay'
        context = self.nlp.classify_user_sentence(user_query)
        print('context is:', context)

        if context is "booking":
            # Get info from NLP
            print(self.state)
            self.nlp.get_journey_info(user_query, self.state)
            print(self.state)
            response = self.determine_train_response()
            print('response is:', response)
        else:
            response = "General chit chat"
        
        return response


