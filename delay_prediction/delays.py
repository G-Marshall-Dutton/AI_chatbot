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
# wtd                   String              Working Time of Departure

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

def secondsToTime(seconds):
    return str(datetime.timedelta(seconds=seconds))

def testing(): ## TESTING HERE
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas.io.sql as sqlio
    import pandas

    queryDay = datetime.datetime.today().weekday() #get today as weekday index

    # Get 24hr time in seconds
    now = datetime.datetime.now()
    queryTimeInDayS = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

    # get all NRCH to LIVST journeys with dep and arr time
    dataframe = DatabaseQuerier().testReturnDataframe('NRCH','LIVST')

    #Initialize final dataset to be used in classifier
    reduced_df = pandas.DataFrame(columns = ["day","time_at_station","journeyTime"])

    count = 0
    for row in dataframe.iterrows():
        # Get data in correct formats
        dep_date = row[1]['rid'][0:8]
        dep_date = datetime.datetime.strptime(dep_date,"%Y%m%d")
        #dep_date_f = datetime.datetime.strftime(dep_date,"%Y%m%d")

        # Get day of week as index
        day = dep_date.weekday()
        tmp = dep_date.toordinal()
        #day = dayIndexToString(day)

        # Calculate journey delay
        a = datetime.datetime.strptime(row[1]['dep_at'],"%H:%M")
        b = datetime.datetime.strptime(row[1]['arr_at'],"%H:%M")
        journeyTime = b - a

        #If negative, passed midnight, make positive
        if journeyTime.total_seconds() < 0:
            journeyTime = journeyTime + datetime.timedelta(days=1)

        timeInDayS = (a - a.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

        
        reduced_df.loc[count] = [day,timeInDayS,journeyTime.total_seconds()]
        #print(reduced_df.loc[count])
        count = count + 1
    print("DONE")
    

    # CLASSIFICATION HERE
    from sklearn.neighbors import NearestNeighbors

    X = reduced_df.drop(['journeyTime'], axis=1) # Remove predicting value for X dataframe
    y = reduced_df['journeyTime'].values # Seperate target predicting values into own dataframe

    #Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
    
    neigh = NearestNeighbors(n_neighbors=1)
    neigh.fit(X_train)

    # Display train data
    count = 0
    for row in X_train.iterrows():
        day = row[1][0]
        time = row[1][1]

        # Input (Test)
        print("Train(%d) %s %s -> %s" %(count,day,secondsToTime(time),y_train[count]))
        count = count + 1

    # Display test data
    print()
    count = 0
    for row in X_test.iterrows():
        day = row[1][0]
        time = row[1][1]

        # Input (Test)
        print("Test(%d) %s %s -> %s" %(count,day,secondsToTime(time),y_test[count]))
        count = count + 1

    # Classify
    print()
    count = 0
    for row in X_test.iterrows():        

        if count > 100:
            break
        

        day = row[1][0]
        time = row[1][1]

        # Input (Test)
        print("%10s %s %s -> %s" %("Test:",day,secondsToTime(time),y_train[count]))

        prediction = neigh.kneighbors([[day, time]]) # 0:distance 1:position of neighbour
        neighbourIndex = prediction[1][0][0] #Index of neighbour in the training list
        pred_day = X_train.iloc(0)[neighbourIndex][0] #Day value of neighbour
        pred_time = X_train.iloc(0)[neighbourIndex][1] #Time of train of neighbour
        pred_delay = y_test[count] #Journey time of neighbour

        # Output (Neighbour/Train)
        print("%10s %s %s -> %s\n" %("Neighbour:",day,secondsToTime(pred_time),y_test[count]))
        count = count + 1
    


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
    


    


