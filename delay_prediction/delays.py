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

with open('tempResults.csv', mode='a') as results:
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
        if abs(actual - prediction) <= maxError:
            return True
        else:
            return False

    def getDateFromRID(rid):
        date_string = rid[0:8]
        date = datetime.datetime.strptime(date_string, "%Y%m%d")
        return date

    def version2(_to,_from, type):
        # Ask user what the current delay is, where they are travelling to, the last station they were/are at
        if type == "all":
            df = DatabaseQuerier().getAllTrains(_to,_from)
        else:
            df = DatabaseQuerier().getDelayedTrains(_to, _from)
        # Get time now as seconds since midnight
        #now = datetime.datetime.now()
        #query_time_s = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        # query_time = datetime.datetime.strptime("2019-07-01-20:30:00", "%Y-%m-%d-%H:%M:%S")
        # query_time_s = (query_time - query_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        # delay = 300 # 300s delay
        # start_station_dep_time_s = query_time_s - delay

        # Idea is to find trains that planned dep time was start_station_dep_time_s but actual dep time was
        # print("Local Time: ",query_time_s,"  DELAY: ",delay,"   dep_at: ",start_station_dep_time_s)

        # Initialize final dataset to be used in classifier
        classification_df = pandas.DataFrame(columns=["time_at_station_s", "current_delay_s","rid","arrival_time_s"])

        count = 0
        for row in df.iterrows():
            
            #print(row)
            # 1:2 planned dep, 1:3 actual dep, 1:5 planned arrival, 1:6 actual arrival

            # Planned departure datetime

            try:
                planned_departure = datetime.datetime.strptime(row[1][0][0:8]+row[1][2],"%Y%m%d%H:%M:%S")
            except ValueError:
                planned_departure = datetime.datetime.strptime(row[1][0][0:8] + row[1][2], "%Y%m%d%H:%M")
            planned_departure = planned_departure - planned_departure.replace(hour=0, minute=0, second=0, microsecond=0)
            #print(planned_departure)

            # Actual departure datetime
            try:
                actual_departure = datetime.datetime.strptime(row[1][0][0:8]+row[1][3],"%Y%m%d%H:%M:%S")
            except ValueError:
                actual_departure = datetime.datetime.strptime(row[1][0][0:8] + row[1][3], "%Y%m%d%H:%M")
            actual_departure = actual_departure - actual_departure.replace(hour=0, minute=0, second=0, microsecond=0)
            #print(actual_departure)

            # Delay at departure station
            departure_delay = actual_departure-planned_departure
            #print(departure_delay)

            # Actual arrival datetime
            try:
                actual_arrival = datetime.datetime.strptime(row[1][0][0:8] + row[1][6], "%Y%m%d%H:%M:%S")
            except ValueError:
                actual_arrival = datetime.datetime.strptime(row[1][0][0:8] + row[1][6], "%Y%m%d%H:%M")
            actual_arrival = actual_arrival - actual_arrival.replace(hour=0, minute=0, second=0, microsecond=0)
            #print(actual_arrival)


            #time_until_arrival = actual_arrival - actual_departure
            #print(time_until_arrival)

            #print("rid:",row[1][0],"ptd:",planned_departure,"delay:",departure_delay,"arrival:",actual_arrival)
            classification_df.loc[count] = [planned_departure.total_seconds(), departure_delay.total_seconds(),row[1][0], actual_arrival.total_seconds()]
            count = count + 1

        X = classification_df.drop(['arrival_time_s','rid'], axis=1)  # Remove predicting value for X dataframe
        y = classification_df[['arrival_time_s','rid']].values  # Seperate target predicting values into own dataframe

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=9)

        neigh = NearestNeighbors(n_neighbors=1)
        neigh.fit(X_train)

        count = 0
        numberAccurate = 0
        for row in X_test.iterrows():

            time_at_station_s = row[1][0]
            current_delay_s = row[1][1]

            print("TEST %d    ( %s):      dep_at=%s, delay=%s   ->  arrival:%s" %(count, y_test[count][1],secondsToTime(time_at_station_s),current_delay_s,secondsToTime(y_test[count][0])))

            # Input (Test)
            predictions = neigh.kneighbors([[time_at_station_s, current_delay_s]])  # 0:distance 1:position of neighbour

            arrival_time = 0
            #for prediction_distance, prediction_index in zip(predictions[0][0], predictions[1][0]):
            predicted_arrival = y_train[predictions[1]][0][0][0]
            #arrival_time = arrival_time + predicted_arrival

            #arrival_time = arrival_time / predictions[0][0].size

            #print(predictions[1])
            neighbour_dep_time_s = X_train.iloc[predictions[1][0][0]][0]
            neighbour_delay_s = X_train.iloc[predictions[1][0][0]][1]
            #print(neighbour_dep_time_s,neighbour_delay_s)

            print("   PREDICTED ( %s):      dep_at=%s, delay=%s   ->  arrival:%s" %(y_train[predictions[1][0][0]][1], secondsToTime(neighbour_dep_time_s),neighbour_delay_s,secondsToTime(predicted_arrival)))
            #print("    PREDICTED: dep_at=%s delay=%s   ->  arrival:%s" %(secondsToTime(neighbour_dep_time_s),neighbour_delay_s,secondsToTime(predicted_arrival)))
            #print(y_test[count][0])
            if isAccurate(y_test[count][0], predicted_arrival, 60):
                numberAccurate = numberAccurate + 1
                print('\033[92m' + " ACCURATE ")
            else:
                print('\033[91m'+ " NOT ACCURATE")
            count = count + 1
            print('\033[0m', end='')

        accuracy = (numberAccurate / X_test.size) * 100
        print("ACCURACY: ","(",numberAccurate,"/",X_test.size,")  ->", accuracy)
        results_writer.writerow([accuracy])


    def getData():
        df = DatabaseQuerier().getSelectedTrains('NRCH', 'LIVST')
        train, test = train_test_split(df, test_size=0.2, random_state=42)
        return train, test


    def getEstimatedArrivalTimeV1(travel_information):
        # from, to, planned_dep_time, delay_mins

        df = DatabaseQuerier().getAllTrains('NRCH', 'LIVST')


        # Get time now as seconds since midnight
        planned_depature_time = datetime.datetime.strptime(travel_information['planned_dep_time'],"%H:%M")
        planned_depature_time_s = (planned_depature_time - planned_depature_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        print("Planned Departure at: ",secondsToTime(planned_depature_time_s),"(",planned_depature_time_s,")")

        delay = travel_information['delay_mins']*60
        print("Delayed by: ",delay)

        # Initialize final dataset to be used in classifier
        classification_df = pandas.DataFrame(columns=["time_at_station_s", "current_delay_s", "rid", "arrival_time_s"])

        count = 0
        for row in df.iterrows():

            # print(row)
            # 1:2 planned dep, 1:3 actual dep, 1:5 planned arrival, 1:6 actual arrival

            # Planned departure datetime

            try:
                planned_departure = datetime.datetime.strptime(row[1][0][0:8] + row[1][2], "%Y%m%d%H:%M:%S")
            except ValueError:
                planned_departure = datetime.datetime.strptime(row[1][0][0:8] + row[1][2], "%Y%m%d%H:%M")
            planned_departure = planned_departure - planned_departure.replace(hour=0, minute=0, second=0, microsecond=0)
            # print(planned_departure)

            # Actual departure datetime
            try:
                actual_departure = datetime.datetime.strptime(row[1][0][0:8] + row[1][3], "%Y%m%d%H:%M:%S")
            except ValueError:
                actual_departure = datetime.datetime.strptime(row[1][0][0:8] + row[1][3], "%Y%m%d%H:%M")
            actual_departure = actual_departure - actual_departure.replace(hour=0, minute=0, second=0, microsecond=0)
            # print(actual_departure)

            # Delay at departure station
            departure_delay = actual_departure - planned_departure
            # print(departure_delay)

            # Actual arrival datetime
            try:
                actual_arrival = datetime.datetime.strptime(row[1][0][0:8] + row[1][6], "%Y%m%d%H:%M:%S")
            except ValueError:
                actual_arrival = datetime.datetime.strptime(row[1][0][0:8] + row[1][6], "%Y%m%d%H:%M")
            actual_arrival = actual_arrival - actual_arrival.replace(hour=0, minute=0, second=0, microsecond=0)
            # print(actual_arrival)

            # print("rid:",row[1][0],"ptd:",planned_departure,"delay:",departure_delay,"arrival:",actual_arrival)
            classification_df.loc[count] = [planned_departure.total_seconds(), departure_delay.total_seconds(),
                                            row[1][0], actual_arrival.total_seconds()]
            count = count + 1

        X = classification_df.drop(['arrival_time_s', 'rid'], axis=1)  # Remove predicting value for X dataframe
        y = classification_df[['arrival_time_s', 'rid']].values  # Seperate target predicting values into own dataframe

        # Split data
        #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=9)

        neigh = NearestNeighbors(n_neighbors=1)
        neigh.fit(X)

        count = 0
        predictions = neigh.kneighbors([[planned_depature_time_s, delay]])  # 0:distance 1:position of neighbour


        predicted_arrival = y[predictions[1]][0][0][0]
        return "You should arrive at "+secondsToTime(y[predictions[1]][0][0][0])


    def getEstimatedArrivalTimeV2(_from, _to, delayed_by):
        # Pass all stations/stops with departure and arrival times
        # create model for each station
        #   inputs: dep_at, delay, day, month, peak/off-peak      Y: arr_at (other observed data)

        df = DatabaseQuerier().getSelectedTrains('NRCH', 'LIVST')
        train, test = train_test_split(df, test_size=0.2, random_state=42)

        print("TODO")


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
        test = getEstimatedArrivalTimeV1({"planned_dep_time":"12:00","delay_mins":2})
        print(test)
        # results_writer.writerow(["14neighbours 1-10000multiplier"])
        # for i in range(1000, 20000, 1000):
        #     version1(14, i)
    


    


