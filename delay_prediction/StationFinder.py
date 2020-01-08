import csv
from pathlib import Path
from difflib import SequenceMatcher

# string comparison function
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

class StationFinder:

    # returns code
    def getCode(self, station):
        # set filepath
        filepath = Path(__file__).parent / "../delay_prediction/reference_data/stations_processed.csv"
        
        # open file into csv
        with open(filepath) as f:
            d = dict(filter(None, csv.reader(f)))

        # set up comparison stuff
        best_key_score = 0
        best_key = None

        # iterate through dictionary
        for key in d:
            # calculate similar score
            curr_score = similar(station, key)
            
            # if better, keep track of it
            if curr_score > best_key_score:
                best_key_score = curr_score
                best_key = key

        return d[best_key]

# TEST CODE
sf = StationFinder()

while(True):
    # get user input
    userInput = input("Input for Station Finder > ")

    print(sf.getCode(userInput))



    