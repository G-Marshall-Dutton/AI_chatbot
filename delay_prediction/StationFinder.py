import csv
from pathlib import Path
from difflib import SequenceMatcher

# string comparison function
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class StationFinder:
    # class attributes - empty dictionaries
    stationToCodeDict = dict()
    codeToStationDict = dict()

    # constructor, load the dictionaries once
    def __init__(self):
        # set filepath
        filepath = Path(__file__).parent / "../delay_prediction/reference_data/stations_processed.csv"
        
        # create station to code dictionary
        with open(filepath) as f:
            self.stationToCodeDict = dict(filter(None, csv.reader(f)))

        # create code to station dictionary
        with open(filepath) as f:
             d = dict(filter(None, csv.reader(f)))

             # create dictionary in csv order, then swap keys and values
             self.codeToStationDict = dict((v,k) for k,v in d.items())

    # returns code
    def getCode(self, station):

        # set up comparison stuff
        best_key_score = 0
        best_key = None

        # iterate through dictionary
        for key in self.stationToCodeDict:
            # calculate similar score
            curr_score = similar(station, key)
            
            # if better, keep track of it
            if curr_score > best_key_score:
                best_key_score = curr_score
                best_key = key

        return self.stationToCodeDict[best_key]

    # returns station
    def getStation(self, code):

        # set up comparison stuff
        best_key_score = 0
        best_key = None

        # iterate through dictionary
        for key in self.codeToStationDict:
            # calculate similar score
            curr_score = similar(code, key)
            
            # if better, keep track of it
            if curr_score > best_key_score:
                best_key_score = curr_score
                best_key = key

        return self.codeToStationDict[best_key]

# TEST CODE
sf = StationFinder()

while(True):
    # get user input
    userInput = input("Input for Station Finder > ")

    # TEST FOR GET CODE
    #print(sf.getCode(userInput))

    # TEST FOR GET STATION
    print(sf.getStation(userInput))




    