from webScraper import webScraper

class ConversationController():
    def __init__(self, nlp):

        self.scraper = webScraper.webScraper()

        # Chat : Booking : Delay 
        self.nlp = nlp
        self.context = "Chat"
        self.state = {
            'from': "CBN",
            'to': "NRW",
            'date': '200220',
            'time': '0845',
        }

        self.response_needed = 4
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

    
    # # Dertermnine context of user query : will return 'chat' , 'booking' , 'delay'
    # def determine_context(self, user_query):
    #     # Pass to NLP 
    #     context = nlp.
    #     return context


    # Prints state
    def print_state(self):
        for k, v in self.state.items():
            print(k, v)
        
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
        # elif not self.state_confirmed:
        else:
            response = self.getTicket()
            return response
            #return "So you want to travel from %s to %s on the %s at %s?" % (self.state['to'], self.state['from'], self.state['date'], self.state['time'])

    # Determine how to respond
    def respond(self, user_query):
        print('RESPONDING...')

        # Recieve context from NLP : 'chat' , 'booking' , 'delay'
        context = self.nlp.classify_user_sentence(user_query)
        print('DETERMINING CONTEXT...')
        print('CONTEXT:', context)

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

    # Returns web scrapped ticket info
    def getTicket(self):
        ticketInfo = self.scraper.scrape(self.state)
        
        return ticketInfo


