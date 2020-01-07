from webScraper import webScraper

class ConversationController():
    def __init__(self, nlp):

        self.scraper = webScraper.webScraper()

        # Chat : Booking : Delay 
        self.nlp = nlp
        self.context = None
        self.state = {
            'from': None,
            'to': None,
            'date': None,
            'time': '1400',   
        }

        self.print_state
        self.reset_state

        # Booking variables
        self.response_needed = 4
        self.awaiting_confirmation = False
        self.state_confirmed = False
 
        # Delay variables
        self.delay_state = {
            'from': None,
            'to': None,
            'planned_dep_time': None,
            'delay_mins': None,   
        }
        self.delay_confirmed = False
        self.awaiting_delay_confirmation = False


    # Updates state 
    def update_state(self, newInfo):
        self.state.update(newInfo)

    # Returns True if state contains a 'none' value
    def state_not_full(self, state):
        for k, v in state.items():
            if v is None:
                return True

        return False

    # Prints state
    def print_state(self):
        for k, v in self.state.items():
            print(k, v)

    # Resets state values to 'None'
    def reset_state(self):
        print("RESETING STATE...")
        for k, v in self.state.items():
            self.state[k] = None
        self.print_state()
        
    # Extracts state relevant info and updates state
    def extract_info(self, user_query):
        # Get info
        # Update state
        return True

    # Determine train specific response based on self.state
    def determine_train_response(self):

        # If state confirmed
        if self.state_confirmed:

            # Reset context
            self.context = None

            # web scrape info 
            response = self.getTicket()
            return response

        elif not self.state_confirmed and self.awaiting_confirmation:
            # Reset state
            self.reset_state()
            self.awaiting_confirmation = False

            # Return reset message 
            response = "Let's start again... \nWhere are you traveling to?"
            return response
 
        # If state is not full
        elif self.state_not_full(self.state):
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
        # elif not self.state_confirmed:
        else:
            # Return confirmation message
            self.awaiting_confirmation = True
            return "So you want to travel from %s to %s on the %s at %s?" % (self.state['from'], self.state['to'], self.state['date'], self.state['time'])
 
 
    # Determine delay specific response based on self.delay_state
    def determine_delay_response(self):

        # If delay_confirmed
        if self.delay_confirmed:

            # Reset context
            self.context = None

            # Predict delay
            response = "There may... or may not be a delay"
            return response

        # If delay_state is not full
        elif self.state_not_full(self.delay_state):
            response = "COULDNT GET APPROPRIATE RESPONSE"
            print("None in self.delay_state")
            # Acquire more info
            if self.delay_state['to'] is None:
                response = "Where are you traveling to?"

            elif self.delay_state['from'] is None:
                response = "Where are you traveling from?"

            elif self.delay_state['planned_dep_time'] is None:
                response = "When were you supposed to leave?"

            elif self.delay_state['delay_mins'] is None:
                response = "Roughly how long have you been delayed?"

            return response

        else:
            # Return confirmation message
            self.awaiting_delay_confirmation = True
            return "So you are traveling from %s to %s. You we're supposed to leave at %s and have been delayed roughly %s minutes so far?" % (self.delay_state['from'], self.delay_state['to'], self.delay_state['planned_dep_time'], self.delay_state['delay_mins'])


    # Determine how to respond
    def respond(self, user_query):
        print("USER ASKED:", user_query)
        print('RESPONDING...')

        # If we're waiting on ticket info confirmation
        if(self.awaiting_confirmation):
            print(user_query)
            
            # NEED TO SWAP THIS FOR NLP
            if(self.nlp.affirmation(user_query)):
                self.state_confirmed = True
                self.context = "booking"
                print("CONFIRMED")
            else:
                self.state_confirmed = False
                self.context = "booking" 
                print("NOT CONFIRMED") 


        # If we're waiting on delay info confirmation
        elif(self.awaiting_delay_confirmation):
            print(user_query)
            
            # NEED TO SWAP THIS FOR NLP
            if(user_query == "yes"):
                self.delay_confirmed = True
                self.context = "delay"
                print("CONFIRMED")
            else:
                self.delay_confirmed = False
                self.context = "delay" 
                print("NOT CONFIRMED") 

        # WILL NEED TO CHANGE THIS BACK TO 'ELSE' (if we can find a different way to stay in delay self.context)
        elif(self.context == None or self.context == 'chat'):
            # Recieve self.context from NLP : 'chat' , 'booking' , 'delay'
            self.context = self.nlp.classify_user_sentence(user_query)
            print('DETERMINING self.context...')
            print('self.context:', self.context)

        if self.context is "booking": 

            # Get info from NLP
            print('STATE:', self.state)
            print('UPDATING STATE...')
            self.nlp.get_journey_info(user_query, self.state)
            print('STATE:', self.state)

            # determine appropriate response
            response = self.determine_train_response()
            print('RESPONSE:', response)

        elif self.context is "delay":

            # Get info from NLP
            print('DELAY_STATE:', self.delay_state)
            print('UPDATING DELAY_STATE...')
            self.nlp.get_delay_info(user_query, self.delay_state)   
            print('DELAY_STATE:', self.delay_state)

            # Determine appropriate response
            response = self.determine_delay_response()
            print('RESPONSE:', response)

        else:
            # determine appropriate response
            response = "General chit chat"
        
        return response

    # Returns web scrapped ticket info
    def getTicket(self):
        ticketInfo = self.scraper.scrape(self.state)
        
        return ticketInfo


