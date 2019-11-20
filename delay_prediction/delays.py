import psycopg2
from sklearn.neighbors import NearestNeighbors
import datetime
### FOR TESTING
import sys
sys.path.insert(1, 'C:\\Users\\jezba\\Documents\\AI_chatbot\\delay_prediction')
from DatabaseQuerier import DatabaseQuerier
###

###############################################
############  Fields Reference  ############

# rid                   string              yyyymmdd + index

# tpl                   string              Location TIPLOC (used by train planners to identify what time trains should arrive at, depart or pass a particular point)

##### Initial planned times
# pta                   string              Planned Time of Arrival
# ptd                   string              Planned Time of Departure

##### Working Times
# wta                   string              Working (staff) Time of Arrival
# wtp                   string              Working Time of Passing
# wtd                   boolean             Working Time of Departure

##### Estimated Arrival Times
# arr_et                string              Estimated Arrival Time
# arr_wet               string              Working Estimated Time
# arr_atRemoved         boolean             true if actual replaced by estimated

##### Estimated Passing Times
# pass_et               string              Estimated Passing Time
# pass_wet              string              Working Estimated Time
# pass_atRemoved        boolean             true if actual replaced by estimated

##### Estimated Departure Times
# dep_et                string              Estimated Departure
# dep_wet               string              Working Estimated Time
# dep_atRemoved         boolean             true if actual replaced by estimated

##### Actual Times
# arr_at                string              Recorded Actual Time of Arrival
# pass_at               string              Actual Passing Time
# dep_at                string              Actual Departure Time
 
##### Reasons/Explanations
# cr_code               int                 Cancellation Reason Code
# lr_code               int                 Late Running Reason


###########################################
###############################################

def createNearestNeighbours():
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas.io.sql as sqlio

    day = datetime.datetime.today().weekday()
    time = datetime.datetime.now().time().strftime("%H:%M:%S")

    dataframe = DatabaseQuerier().testReturnDataframe('NRCH','LIVST')

    for row in dataframe.iterrows():
        a = datetime.datetime.strptime(row[1]['dep_at'],"%H:%M")
        b = datetime.datetime.strptime(row[1]['arr_at'],"%H:%M")
        delay = b - a
        if delay.total_seconds() < 0:
            delay = delay + datetime.timedelta(days=1)
        delay = datetime.datetime.fromtimestamp(delay.seconds)
        print(a.time(),b.time(),delay.time()) 


####################################################
#
#   Provide api to classifier  
#
class DelayPredictor:
    def __init__(self):
        ## Setup way to connect to database
        self.db = DatabaseQuerier()

    def predictDelay(self, recent_station, dest_station, time, day_of_week):
        return "just walk mate"




###############################################################
###################### Test Harness  ######################
if __name__ == "__main__":
    # print("delays Test Environment")
    # db = DatabaseQuerier()
    # rids = db.getAllPreviousJourneyRIDs()
    # for i in range(len(rids)):
    #     rids[i] = rids[i][0]
    # print(rids)
    
    createNearestNeighbours()
    


    


