import psycopg2
from sklearn.neighbors import NearestNeighbors
import datetime
### FOR TESTING
import sys
sys.path.insert(1, 'C:\\Users\\jezba\\Documents\\AI_chatbot\\delay_prediction')
from DatabaseQuerier import DatabaseQuerier
from sklearn.model_selection import train_test_split
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

def dayIndexToString(index):
    switcher = {
        0: "mon",
        1: "tues",
        2: "weds",
        3: "thurs",
        4: "fri",
        5: "sat",
        6: "sun",
    }
    return switcher.get(index, "Invalid day")

def testing():
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas.io.sql as sqlio
    import pandas

    #get today as weekday index
    day = datetime.datetime.today().weekday()
    #get time now as HHMMSS
    time = datetime.datetime.now().time().strftime("%H:%M:%S")

    dataframe = DatabaseQuerier().testReturnDataframe('NRCH','LIVST')

    #Initialize final dataset
    reduced_df = pandas.DataFrame(columns = ["rid","day","delay_s"])

    count = 0
    for row in dataframe.iterrows():

        # Get data in correct formats
        dep_date = row[1]['rid'][0:8]
        dep_date = datetime.datetime.strptime(dep_date,"%Y%m%d")
        #dep_date_f = datetime.datetime.strftime(dep_date,"%Y%m%d")

        # Get day of week as index
        day = dep_date.weekday()
        #day = dayIndexToString(day)

        # Calculate journey delay
        a = datetime.datetime.strptime(row[1]['dep_at'],"%H:%M")
        b = datetime.datetime.strptime(row[1]['arr_at'],"%H:%M")
        delay = b - a

        #If negative, passed midnight, make positive
        if delay.total_seconds() < 0:
            delay = delay + datetime.timedelta(days=1)
        
        reduced_df.loc[count] = [row[1]['rid'],day,delay.total_seconds()]
        count = count + 1
    print("DONE")
    # X = reduced_df.drop(['delay_s'], axis=1)
    # #separate target values
    # y = reduced_df['delay_s'].values
    # print(y[0:5])

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)
    # # ## Import the Classifier.
    # from sklearn.neighbors import KNeighborsClassifier
    # ## Instantiate the model with 5 neighbors. 
    # knn = KNeighborsClassifier(n_neighbors=5)
    # ## Fit the model on the training data.
    # knn.fit(X_train, y_train)
    # ## See how the model performs on the test data.
    # print(knn.score(X_test, y_test))

    # print(reduced_df)


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
    
    testing()
    


    


