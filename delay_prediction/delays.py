import psycopg2
from sklearn.neighbors import NearestNeighbors
import datetime
### FOR TESTING
import sys
sys.path.insert(1, 'C:\\Users\\jezba\\Documents\\AI_chatbot\\delay_prediction')
from DatabaseQuerier import DatabaseQuerier
from sklearn.neighbors import NearestNeighbors
import pandas
from sklearn.model_selection import train_test_split
###
import csv

with open('InitialResults.csv', mode='w') as results:
    results_writer = csv.writer(results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

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

    # actual value, predicted value, largest difference allowed to be considered accurate
    def isAccurate(actual, prediction, maxError):
        if abs(actual - prediction) < maxError:
            return True
        else:
            return False

    def getDateFromRID(rid):
        date_string = rid[0:8]
        date = datetime.datetime.strptime(date_string, "%Y%m%d")
        return date


    def version1(neighbours): ## TESTING HERE

        queryDay = datetime.datetime.today().weekday() #get today as weekday index

        # Get 24hr time in seconds
        now = datetime.datetime.now()
        queryTimeInDayS = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

        # get all NRCH to LIVST journeys with dep and arr time
        dataframe = DatabaseQuerier().testReturnDataframe('NRCH','LIVST')

        # Initialize final dataset to be used in classifier
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


            reduced_df.loc[count] = [day*1000,timeInDayS,journeyTime.total_seconds()]
            #print(reduced_df.loc[count])
            count = count + 1
        print("DONE")


        # CLASSIFICATION HERE


        X = reduced_df.drop(['journeyTime'], axis=1) # Remove predicting value for X dataframe
        y = reduced_df['journeyTime'].values # Seperate target predicting values into own dataframe

        #Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

        neigh = NearestNeighbors(n_neighbors=neighbours)
        neigh.fit(X_train)

        displayLimit = 10;

        # Display train data
        # count = 0
        # for row in X_train.iterrows():
        #     day = row[1][0]
        #     time = row[1][1]
        #
        #     # Input (Test)
        #     print("Train(%d) %s %s -> %s" %(count,day,secondsToTime(time),y_train[count]))
        #     count = count + 1
        #
        #     if count > displayLimit:
        #         break;

        # Display test data
        # print()
        # count = 0
        # for row in X_test.iterrows():
        #     day = row[1][0]
        #     time = row[1][1]
        #
        #     # Input (Test)
        #     print("Test(%d) %s %s -> %s" %(count,day,secondsToTime(time),y_test[count]))
        #     count = count + 1
        #
        #     if count > displayLimit:
        #         break;

        # Classify
        #print()
        count = 0
        numberAccurate = 0

        for row in X_test.iterrows():

            day = row[1][0]
            time = row[1][1]

            # Input (Test)
            #print("%10s %s %s -> %s" %("Test:",day,secondsToTime(time),y_train[count]))

            predictions = neigh.kneighbors([[day, time]]) # 0:distance 1:position of neighbour

            final_delay = 0
            for prediction_distance, prediction_index in zip(predictions[0][0],predictions[1][0]):
                prediction_delay = y_train[prediction_index]
                final_delay = final_delay + prediction_delay

            final_delay = final_delay / predictions[0][0].size

            #print("Predicted: "+str(final_delay)+"   Actual: "+str(y_train[count]), end='')
            if isAccurate(y_test[count],final_delay,60):
                numberAccurate = numberAccurate + 1
               # print(" ACC")
            #else:
                #print(" NOT ACC")
            count = count + 1
        accuracy = (numberAccurate/X_test.size)*100
        print(neighbours,"Neighbours"," gives ACCURACY: ",accuracy)

        results_writer.writerow([neighbours, accuracy])

    def version2():
        # Look at current station, knowing how late they currently are to get the planned departure time, get actual arrival time at destination
        # lastStation planned dep, departureDelay (act dep - plan dep),      -> actual arrival time at destination
        #
        df = DatabaseQuerier().getVersion2Dataframe('DISS', 'LIVST')

        # Get time now as seconds since midnight
        now = datetime.datetime.now()
        query_time_s = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

        # Initialize final dataset to be used in classifier
        classification_df = pandas.DataFrame(columns=["time_at_station_s", "current_delay_s"])

        for row in df.iterrows():
            print(row)


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
        for i in range(1,500,20):
            version1(i)
    


    


