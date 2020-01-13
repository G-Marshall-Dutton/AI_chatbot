from webScraper import webScraper
from delay_prediction.DelayController import DelayController
from delay_prediction.StationFinder import StationFinder
import random
from datetime import datetime
import dateparser

class ConversationController():
    def __init__(self, nlp):

        self.scraper = webScraper.webScraper()
        self.delay_controller = DelayController()
        self.nlp = nlp
        self.sf = StationFinder()

        self.context = None

        self.voiceActive = False
        
        # Chat : Booking : Delay 
        self.state = {
            'from': None,
            'to': None,
            'date': None,
            'time': None,   
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

        self.lock_booking = False
        self.lock_delay = False


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

    # Prints delay state
    def print_delay_state(self):
        for k, v in self.delay_state.items():
            print(k, v)

    # Resets state values to 'None'
    def reset_state(self):
        print("RESETING STATE...")
        for k, v in self.state.items():
            self.state[k] = None
        self.print_state()

    # Resets state values to 'None'
    def reset_delay_state(self):
        print("RESETING STATE...")
        for k, v in self.delay_state.items():
            self.delay_state[k] = None
        self.print_delay_state()
        
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

            # Reset state
            self.state_confirmed = False
            self.awaiting_confirmation = False

            # web scrape info 
            response = self.getTicket()

            # Reset state
            self.reset_state()

            return response

        elif self.awaiting_confirmation:
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
                response = 'Sure! ' + random.choice(self.nlp.kb.to_responses)

            elif self.state['from'] is None:
                response = random.choice(self.nlp.kb.from_responses)

            elif self.state['date'] is None:
                self.lock_booking = True
                response = random.choice(self.nlp.kb.date_responses)

            elif self.state['time'] is None:
                self.lock_booking = True
                response = random.choice(self.nlp.kb.dep_time_responses)

            return response

        # If we have all the needed info, confirm its correct
        # elif not self.state_confirmed:
        else:
            # Return confirmation message
            self.lock_booking = False
            self.awaiting_confirmation = True
            date = datetime.strptime( self.state['date'][0:4] + '20' + (self.state['date'])[4:6], '%d%m%Y')
            date = date.strftime("%d %B, %Y")
            return "So you want to travel from %s to %s on the %s at %s?" % (self.sf.getStation(self.state['from']), self.sf.getStation(self.state['to']), date, self.state['time'])
 
 
    # Determine delay specific response based on self.delay_state
    def determine_delay_response(self):

        # If delay_confirmed
        if self.delay_confirmed:

            # Reset context
            self.context = None

            # Reset delay confirmation
            self.delay_confirmed = False
            self.awaiting_delay_confirmation = False

            # Convert 'London' into station code (London is edge case, dont need to do this for other stations)
            if(self.delay_state['from'] == 'London'):
                self.delay_state['from'] = 'LIVST'
            elif(self.delay_state['to'] == 'London'):
                self.delay_state['to'] = 'LIVST'


            # Predict delay
            response = self.delay_controller.get_delay(self.delay_state)

            self.reset_delay_state()
            return response

        elif self.awaiting_delay_confirmation:
            # Reset state
            self.reset_delay_state()
            self.awaiting_delay_confirmation = False

            # Return reset message 
            response = "Let's start again... \nWhere are you traveling to?"
            return response

        # If delay_state is not full
        elif self.state_not_full(self.delay_state):
            response = "COULDNT GET APPROPRIATE RESPONSE"
            print("None in self.delay_state")
            # Acquire more info
            if self.delay_state['to'] is None:
                response = 'Let me try and help. ' + random.choice(self.nlp.kb.delay_to_responses)

            elif self.delay_state['from'] is None:
                response = random.choice(self.nlp.kb.from_responses)

            elif self.delay_state['planned_dep_time'] is None:
                self.lock_delay = True
                response = random.choice(self.nlp.kb.delay_dep_time_responses)

            elif self.delay_state['delay_mins'] is None:
                self.lock_delay = True
                response = random.choice(self.nlp.kb.delayed_by_responses)

            return response

        else:
            # Return confirmation message
            self.lock_delay = False
            self.awaiting_delay_confirmation = True
            return "So you are traveling from %s to %s. You we're supposed to leave at %s and have been delayed roughly %s minutes so far?" % (self.sf.getStation(self.delay_state['from']), self.sf.getStation(self.delay_state['to']), self.delay_state['planned_dep_time'], self.delay_state['delay_mins'])


    # Determine how to respond
    def respond(self, user_query):
        print("USER ASKED:", user_query)
        print('RESPONDING...')

        # If we're waiting on ticket info confirmation
        if(self.awaiting_confirmation):
            print(user_query)

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
            if(self.nlp.affirmation(user_query)):
                self.delay_confirmed = True
                self.context = "delay"
                print("CONFIRMED")
            else:
                self.delay_confirmed = False
                self.context = "delay" 
                print("NOT CONFIRMED") 

        # Stay in booking state if locked
        elif(self.lock_booking):
            self.context = 'booking'

        # Stay in delay state if locked
        elif(self.lock_delay):
            self.context ='delay'

        # If user is responding with YES - and not awaiting confirmation
        elif(self.nlp.affirmation(user_query)):
            print("AFFIRMATION")
            self.context = 'chat'
         # If user is responding with NO - and not awaiting confirmation
        elif(self.nlp.refutation(user_query)):
            print("REFUTATION")
            self.context = 'chat'


        else:
            # Store previous context
            prev_context = self.context

            # Recieve self.context from NLP : 'chat' , 'booking' , 'delay'
            self.context = self.nlp.classify_user_sentence(user_query)

            # Dont allow swap from booking to delay
            if(prev_context == 'booking' and self.context == 'delay'):
                self.context = 'booking'
            elif(prev_context == 'delay' and self.context == 'booking'):
                self.context = 'delay'
            
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
            response = self.nlp.get_chat_response_from_model(user_query)
        
        return response

    # Returns web scrapped ticket info
    def getTicket(self):
        new_state = {
            'to' : self.sf.getShortCode(self.state['to']),
            'from' : self.sf.getShortCode(self.state['from']),
            'date' : self.state['date'],
            'time' : self.state['time']
        }
        
        ticketInfo = self.scraper.scrape(new_state)
        
        return ticketInfo


