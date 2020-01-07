from webScraper import webScraper

class ConversationController():
    def __init__(self, nlp):

        self.scraper = webScraper.webScraper()

        # Chat : Booking : Delay 
        self.nlp = nlp
        self.context = "Chat"
        self.state = {
            'from': None,
            'to': None,
            'date': None,
            'time': '1430',   
        }

        self.print_state
        self.reset_state

        self.response_needed = 4
        self.awaiting_confirmation = False
        self.state_confirmed = False


    # Updates state 
    def update_state(self, newInfo):
        self.state.update(newInfo)

    # Returns True if state contains a 'none' value
    def state_not_full(self):
        for k, v in self.state.items():
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
        # elif not self.state_confirmed:
        else:
            # Return confirmation message
            self.awaiting_confirmation = True
            return "So you want to travel from %s to %s on the %s at %s?" % (self.state['to'], self.state['from'], self.state['date'], self.state['time'])

    # Determine how to respond
    def respond(self, user_query):
        print('RESPONDING...')

        # If we're waiting on ticket info confirmation
        if(self.awaiting_confirmation):
            print(user_query)
            
            # NEED TO SWAP THIS FOR NLP
            if(user_query == "yes"):
                self.state_confirmed = True
                context = "booking"
                print("CONFIRMED")
            else:
                self.state_confirmed = False
                context = "booking" 
                print("NOT CONFIRMED") 
        else:
            # Recieve context from NLP : 'chat' , 'booking' , 'delay'
            context = self.nlp.classify_user_sentence(user_query)
            print('DETERMINING CONTEXT...')
            print('CONTEXT:', context)

        if context is "booking":

            # Get info from NLP
            print('STATE:', self.state)
            print('UPDATING STATE...')
            self.nlp.get_journey_info(user_query, self.state)
            print('STATE:', self.state)

            # determine appropriate response
            response = self.determine_train_response()
            print('RESPONSE:', response)

        elif context is "delay":
            # Determine appropriate response
            response = "Stuff about delays"

        else:
            # determine appropriate response
            response = "General chit chat"
        
        return response

    # Returns web scrapped ticket info
    def getTicket(self):
        ticketInfo = self.scraper.scrape(self.state)
        
        return ticketInfo


