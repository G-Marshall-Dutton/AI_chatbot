import csv
import datetime
import pandas
from joblib import dump, load

from sklearn.model_selection import train_test_split

from delay_prediction.DatabaseQuerier import DatabaseQuerier
from delay_prediction.delays import secondsToTime,monthIndexToString,dayIndexToString,peakIndexToString,isPeak

from sklearn.ensemble import RandomForestRegressor


from delay_prediction.delays import secondsToTime
from delay_prediction.delays import isAccurate


class StationBasedVersion3:

    def __init__(self):
        self.route = ["NRCH",
                      "DISS",
                      "STWMRKT",
                      #"NEEDHAM",
                      "IPSWICH",
                      "MANNGTR",
                      "CLCHSTR",
                      #"WITHAME",
                      "CHLMSFD",
                      #"SHENFLD",
                      "STFD",
                      "LIVST"]
        self.stationList= ["DISS","STWMRKT","IPSWICH","MANNGTR","CLCHSTR","CHLMSFD","STFD","LIVST"]
        self.stations = {}
        for station in self.stationList:
            self.stations.update({station:RandomForestRegressor(n_estimators= 1600,
                                                                min_samples_split= 5,
                                                                min_samples_leaf= 1,
                                                                max_features= 'auto',
                                                                max_depth= 10,
                                                                bootstrap= True)})


    def buildClassifier(self, datapoints):
        # Build classifier from training data
        # Initialize final dataset to be used in classifier

        for station in self.stationList:

            print("Building classifier for passing through ",station," ",end='')


            #Get data for station
            inputData = DatabaseQuerier().getDataOnStation(station, datapoints)

            # Initialise dataframe
            classification_data = pandas.DataFrame(
                columns=["prev_station_delay", "month", "day", "hour", "peak", "previous_journey_length","time_spent_at_station",
                         "dep_delay"])

            inputData.ptd.fillna(value=pandas.np.nan, inplace=True)
            inputData.dep_at.fillna(value=pandas.np.nan, inplace=True)
            inputData = inputData.fillna("00:00:00")
            count = 0
            for row in inputData.iterrows():

                # 0:rid 1:tpl 2:prev_station_ptd 3:prev_station_dep_at 4:pta 5:arr_at 6:ptd 7:dep_at 8:monthnum 9:dayofweek 10:peak

                data = row[1]
                prev_station_dep = datetime.datetime.strptime(data[0][0:8], "%Y%m%d")
                prev_station_dep = datetime.datetime.combine(prev_station_dep, data[3])
                prev_station_ptd = datetime.datetime.strptime(data[0][0:8], "%Y%m%d")
                prev_station_ptd = datetime.datetime.combine(prev_station_ptd, data[2])
                prev_station_delay = prev_station_dep - prev_station_ptd

                month = data[8]
                day = data[9]
                peak = data[10]

                arrival_time = datetime.datetime.strptime(data[0][0:8], "%Y%m%d")
                arrival_time = datetime.datetime.combine(arrival_time, data[5])
                hour = arrival_time.hour

                previous_journey_length = arrival_time - prev_station_dep



                if station != "LIVST":
                    dep_at = datetime.datetime.strptime(row[1][0][0:8], "%Y%m%d")
                    dep_at = datetime.datetime.combine(dep_at, data[7])

                    ptd = datetime.datetime.strptime(row[1][0][0:8], "%Y%m%d")
                    ptd = datetime.datetime.combine(ptd, data[6])

                    dep_delay = dep_at - ptd

                    previous_journey_length = arrival_time - prev_station_dep
                    time_spent_here = dep_at - arrival_time
                else:
                    dep_at = datetime.datetime.now() - datetime.datetime.now()
                    dep_delay = dep_at
                    #ptd = datetime.datetime.now()
                    time_spent_here = dep_at

                # prev_station_planned_dep = prev_station_ptd - prev_station_ptd.replace(hour=0, minute=0, second=0,
                #                                                                microsecond=0)
                #arrival_time = arrival_time - arrival_time.replace(hour=0, minute=0, second=0, microsecond=0)
                #ptd = ptd - ptd.replace(hour=0, minute=0, second=0, microsecond=0)

                # print("prev_station_dep: ",prev_station_dep)
                # print("prev_station_delay: ", prev_station_delay)
                # print("month: ", month)
                # print("day: ", day)
                # print("peak: ", peak)
                # print("- arrival_time: ", arrival_time)
                # print("- dep_at: ", dep_at)
                # print("- dep_delay: ", dep_delay)

                newRow = [prev_station_delay.total_seconds(), month, day, hour, peak,previous_journey_length.total_seconds(),
                                                       time_spent_here.total_seconds(), dep_delay.total_seconds()]
                classification_data.loc[count] = newRow
                count = count + 1

            classification_data.fillna(0)

            X = classification_data.drop(['previous_journey_length', 'time_spent_at_station', 'dep_delay'],
                                              axis=1)  # Remove predicting value for X dataframe
            y = classification_data[
                ['previous_journey_length', 'time_spent_at_station', 'dep_delay']].values  # Seperate target predicting values into own dataframe

            self.stations[station].fit(X, y)
            print(" (found ",classification_data.month.count()," instances in the data)")
            print("COMPLETE ")

        print(" DONE")

    def testIndividulStationModels(self):
        for station in self.stationList:
            with open(station+'.csv', mode='a') as results:
                results_writer = csv.writer(results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                # Get data for station
                inputData = DatabaseQuerier().getDataOnStation(station, None)

                # Initialise dataframe
                classification_data = pandas.DataFrame(
                    columns=["prev_station_dep", "prev_station_delay", "month ", "day", "peak", "arrival_time", "dep_at",
                             "dep_delay"])

                inputData.ptd.fillna(value=pandas.np.nan, inplace=True)
                inputData.dep_at.fillna(value=pandas.np.nan, inplace=True)
                inputData = inputData.fillna("00:00:00")
                count = 0
                for row in inputData.iterrows():

                    # 0:rid 1:tpl 2:prev_station_ptd 3:prev_station_dep_at 4:pta 5:arr_at 6:ptd 7:dep_at 8:monthnum 9:dayofweek 10:peak

                    data = row[1]
                    prev_station_dep = datetime.datetime.strptime(data[0][0:8], "%Y%m%d")
                    prev_station_dep = datetime.datetime.combine(prev_station_dep, data[3])

                    prev_station_ptd = datetime.datetime.strptime(data[0][0:8], "%Y%m%d")
                    prev_station_ptd = datetime.datetime.combine(prev_station_ptd, data[2])

                    prev_station_delay = prev_station_dep - prev_station_ptd

                    month = data[8]
                    day = data[9]
                    peak = data[10]

                    arrival_time = datetime.datetime.strptime(data[0][0:8], "%Y%m%d")
                    arrival_time = datetime.datetime.combine(arrival_time, data[5])

                    if station != "LIVST":
                        dep_at = datetime.datetime.strptime(row[1][0][0:8], "%Y%m%d")
                        dep_at = datetime.datetime.combine(dep_at, data[7])

                        ptd = datetime.datetime.strptime(row[1][0][0:8], "%Y%m%d")
                        ptd = datetime.datetime.combine(ptd, data[6])

                        dep_delay = dep_at - ptd

                        dep_at = dep_at - dep_at.replace(hour=0, minute=0, second=0, microsecond=0)
                    else:
                        dep_at = datetime.datetime.now() - datetime.datetime.now()
                        dep_delay = dep_at

                    prev_station_dep = prev_station_dep - prev_station_dep.replace(hour=0, minute=0, second=0,
                                                                                   microsecond=0)
                    arrival_time = arrival_time - arrival_time.replace(hour=0, minute=0, second=0, microsecond=0)

                    # print("prev_station_dep: ",prev_station_dep)
                    # print("prev_station_delay: ", prev_station_delay)
                    # print("month: ", month)
                    # print("day: ", day)
                    # print("peak: ", peak)
                    # print("- arrival_time: ", arrival_time)
                    # print("- dep_at: ", dep_at)
                    # print("- dep_delay: ", dep_delay)

                    classification_data.loc[count] = [prev_station_dep.total_seconds(), prev_station_delay.total_seconds(),
                                                      month, day, peak,
                                                      arrival_time.total_seconds(), dep_at.total_seconds(),
                                                      dep_delay.total_seconds()]
                    count = count + 1

                classification_data.fillna(0)

                X = classification_data.drop(['arrival_time', 'dep_at', 'dep_delay'],
                                             axis=1)  # Remove predicting value for X dataframe
                y = classification_data[
                    ['arrival_time', 'dep_at', 'dep_delay']].values  # Seperate target predicting values into own dataframe

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

                self.stations[station].fit(X_train, y_train)

                print("TESTING MODEL FOR ", station)
                count = 0
                numberAccurate = 0
                for row in X_test.iterrows():
                    prediction = round(self.stations[station].predict([[
                        row[1][0],row[1][1],row[1][2],row[1][3],row[1][4]
                    ]])[0][0])
                    actual = y_test[count][0]
                    #print("---->",secondsToTime(actual)," predicted as ",secondsToTime(prediction),"  ", end='')
                    if isAccurate(actual,prediction,60):
                        numberAccurate = numberAccurate + 1
                        #print("ACCURATE")
                    # else:
                    #     print("NOT ACCURATE")

                    count = count + 1
                    accuracy = (numberAccurate / count) * 100
                print(station, " arrival accuracy within 1 minute: ",numberAccurate,"/",count," ->",accuracy)
                results_writer.writerow([count,accuracy])

    def testClassifier(self,filename): # To work, change classify to return arrival_t
        with open(filename + '.csv', mode='a') as results:
            results_writer = csv.writer(results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            ## test on some journeys
            journeys_a = DatabaseQuerier().testClassificationData("NRCH","DISS", 5)
            journeys_b = DatabaseQuerier().testClassificationData("NRCH","STWMRKT", 5)
            journeys_c = DatabaseQuerier().testClassificationData("NRCH","IPSWICH", 5)
            journeys_d = DatabaseQuerier().testClassificationData("NRCH","MANNGTR", 5)
            journeys_e = DatabaseQuerier().testClassificationData("NRCH","CLCHSTR", 5)
            journeys_f = DatabaseQuerier().testClassificationData("NRCH", "CHLMSFD", 5)
            journeys_g = DatabaseQuerier().testClassificationData("NRCH","STFD", 5)
            journeys_h = DatabaseQuerier().testClassificationData("NRCH","LIVST", 5)

            frames = [journeys_a, journeys_b, journeys_c,journeys_d,journeys_e,journeys_f,journeys_g, journeys_h]

            testing_journeys = pandas.concat(frames)

            count = 0
            numberAccurateDISS = 0
            numberAccurateSTWMRKT = 0
            numberAccurateIPSWICH = 0
            numberAccurateMANNGTR = 0
            numberAccurateCLCHSTR = 0
            numberAccurateCHLMSFD = 0
            numberAccurateSTFD = 0
            numberAccurateLIVST = 0
            numberAccurate_TOTAL = 0



            for row in testing_journeys.iterrows():
                if count % 100 == 0:
                    print(count,"/",)

                dep_at = datetime.datetime.strptime(row[1][0][0:8], "%Y%m%d")
                dep_at = datetime.datetime.combine(dep_at, row[1][3])
                dep_HHMM = dep_at.strftime("%H%M%S")[0:4]

                ptd = datetime.datetime.strptime(row[1][0][0:8], "%Y%m%d")
                ptd = datetime.datetime.combine(ptd,row[1][2])

                dep_delay_s = (dep_at - ptd).total_seconds()
                dep_delay_m = round(dep_delay_s/60) # to minutes

                prediction, msg = self.classifyInstance({"to":row[1][4], "from":row[1][1], "planned_dep_time":dep_HHMM, "delay_mins":dep_delay_m})

                actual = testing_journeys.iloc[count][5]
                actual_s = (actual.hour * 60 + actual.minute) * 60 + actual.second

                print("To", row[1][4], secondsToTime(actual_s))
                print("       ", secondsToTime(prediction))

                if isAccurate(actual_s, prediction, 60):
                    print("   ACCURATE")
                    numberAccurate_TOTAL = numberAccurate_TOTAL + 1
                    _to = row[1][4]
                    if _to == "DISS":
                        numberAccurateDISS = numberAccurateDISS + 1
                    elif _to == "STWMRKT":
                        numberAccurateSTWMRKT = numberAccurateSTWMRKT + 1
                    elif _to == "IPSWICH":
                        numberAccurateIPSWICH = numberAccurateIPSWICH + 1
                    elif _to == "MANNGTR":
                        numberAccurateMANNGTR = numberAccurateMANNGTR + 1
                    elif _to == "CLCHSTR ":
                        numberAccurateCLCHSTR  = numberAccurateCLCHSTR + 1
                    elif _to == "CHLMSFD ":
                        numberAccurateCHLMSFD = numberAccurateCHLMSFD + 1
                    elif _to == "STFD":
                        numberAccurateSTFD = numberAccurateSTFD + 1
                    elif _to == "LIVST":
                        numberAccurateLIVST = numberAccurateLIVST + 1
                else:
                    print("   NOT")
                count = count + 1

            accuracyDISS = (numberAccurateDISS / 100) * 100
            accuracySTWMRKT = (numberAccurateSTWMRKT / 100) * 100
            accuracyIPSWICH = (numberAccurateIPSWICH / 100) * 100
            accuracyMANNGTR = (numberAccurateMANNGTR / 100) * 100
            accuracyCLCHSTR = (numberAccurateCLCHSTR / 100) * 100
            accuracyCHLMSFD = (numberAccurateCHLMSFD / 100) * 100
            accuracySTFD = (numberAccurateSTFD / 100) * 100
            accuracyLIVST = (numberAccurateLIVST / 100) * 100

            overallAccuracy = (numberAccurateDISS / count) * 100

            print(accuracyDISS,accuracySTWMRKT,accuracyIPSWICH,accuracyMANNGTR,accuracyCLCHSTR,accuracyCHLMSFD,accuracySTFD,accuracyLIVST," ",overallAccuracy)

            results_writer.writerow(["Diss", "Stowmarket", "Ipswich", "Manning", "Colchester", "Stratford","LiverpoolStreet", " ", "Overall"])
            results_writer.writerow([accuracyDISS,accuracySTWMRKT,accuracyIPSWICH,accuracyMANNGTR,accuracyCLCHSTR,accuracySTFD,accuracyLIVST," ",overallAccuracy])


    def classifyInstance(self, features):
        # Classify an set of features return the predicted output
        # from, to, planned_dep_time, delay_mins

        user_travelling_from = features['from']
        user_travelling_to = features['to']

        return_message = ""

        # check for valid route, stations
        to_index = None
        from_index = None
        i = 0
        for st in self.route:
            if st == user_travelling_to:
                to_index = i
            elif st == user_travelling_from:
                from_index = i
            i = i + 1

        if (to_index is None):
            return None, "Sorry! I cannot predict delays to " + user_travelling_to + " :("
        elif from_index is None:
            return None, "Sorry! I cannot predict delays from " + user_travelling_from + " :("

        if from_index > to_index:
            return None, "Sorry! I don't know enough about that journey :("

        user_planned_depature_time = datetime.datetime.strptime(features['planned_dep_time'], "%H%M")
        user_planned_depature_time_s = (user_planned_depature_time - user_planned_depature_time.replace(hour=0, minute=0, second=0,
                                                                                         microsecond=0)).total_seconds()
        #print("User planned departure at: ", secondsToTime(user_planned_depature_time_s), "(", user_planned_depature_time_s, ") FROM",user_travelling_from)

        delay = int(features['delay_mins']) * 60
        user_left_at = user_planned_depature_time_s + delay
        #print("User delayed by: ", delay)
        #print("Travelling to: ", user_travelling_to)

        now = datetime.datetime.now()
        month = now.month
        day = now.weekday()
        hour = int(user_left_at / 3600)
        hour = datetime.datetime.strptime(str(hour)+"0000", "%H%M%S")
        hour = hour.hour
        peak = isPeak(user_planned_depature_time_s)


        journey_length_since_dep = 0
        time_spent_at_station = 0
        started = False
        for stop in self.route:

            if not started and stop != user_travelling_from:
                continue
            elif stop == "NRCH":
                started = True
                continue

            started = True

            # Predict values for stop
            #print("Predicting values for passing through ", stop)
            predictions = self.stations[stop].predict([[delay, month, day, hour, peak]])

            columns = ["prev_station_delay", "month", "day", "hour", "peak", "previous_journey_length",
                       "time_spent_at_station",
                       "dep_delay"]


            previous_journey_length = predictions[0][0]
            time_spent_at_station = predictions[0][1]
            delay = predictions[0][2]

            journey_length_since_dep = journey_length_since_dep + previous_journey_length
            arrival_time = user_left_at + journey_length_since_dep
            hour = int(arrival_time / 3600)
            #print("         This train should arrive to ",stop," at ",secondsToTime(predicted_arrival_time), " and will likely be delayed by ", secondsToTime(delay),"\n")

            if stop == user_travelling_to:
                return_message = return_message + "You should arrive at your destination (" +user_travelling_to+") at: " + secondsToTime(arrival_time) + "\\n"
                #arrival_time = user_left_at + journey_length_since_dep
                #print("Predicing Final Values at ",stop," as ",secondsToTime(arrival_time))
                return arrival_time, return_message
            else:
                return_message = return_message + "You should reach " + stop + " at " + secondsToTime(arrival_time)
                journey_length_since_dep + time_spent_at_station

        return None, "ERROR FINDING DELAY"


if __name__ == "__main__":
    print("Hello")
    #dq = DatabaseQuerier()
    # classifier_sm = StationBasedForestRegressor()
    # classifier_sm.buildClassifier(1000)
    # dump(classifier_sm, 'classifier_sm.joblib')
    #
    # classifier_md = StationBasedForestRegressor()
    # classifier_md.buildClassifier(5000)
    # dump(classifier_md, 'classifier_md.joblib')
    #
    # classifier_lg = StationBasedForestRegressor()
    # classifier_lg.buildClassifier(None)
    # dump(classifier_lg, 'BIGBOY.joblib')

    # sm = load("latest_classifier.joblib")
    test = StationBasedVersion3()
    test.buildClassifier(5000)
    dump(test, 'final_classifier.joblib')
    #test.testClassifier("test1957")
    # print("Loaded sm")
    # md = load("classifier_md.joblib")
    # print("Loaded md")
    # lg = load("classifier_lg.joblib")
    # print("Loaded lg")
    # BIGBOY = load("BIGBOY.joblib")
    # print("Loaded BIGBOY")
    # new = load("no_times_lg.joblib")
    # print("Loaded new")

    # sm.testClassifier("sm")
    # md.testClassifier("md")
    # lg.testClassifier("lg")


    # while(True):
    #     t = input("to")
    #     f = input("from")
    #     ptd = input("ptd")
    #     delay = input("delay")

    #     arr,msg = test.classifyInstance({"to": t, "from": f, "planned_dep_time": ptd, "delay_mins": delay})

    #     print(secondsToTime(arr),msg)




    #dump(classifier, 'classifier.joblib')
    # print("LOADING CLASSIFIER")
    # test_load = load('classifier.joblib')
    # print("TESTING")
    # test_load.testClassifier("TESTING_BUILT_CLASSIFIER")

    # new_test = StationBasedVersion3()
    # new_test.buildClassifier(1000)
    # dump(new_test, 'test_extra_info.joblib')
    # time,message = test.classifyInstance({"to": "LIVST", "from": "NRCH", "planned_dep_time": "1300", "delay_mins": 0})
    # print(message)
    #sm.testClassifier("Testing_new_sm")
    # dump(new_test, 'classifier_updated.joblib')
    # a = load('classifier_updated.joblib')
    # a.testClassifier("NEW")
    # print("BUILDING NEW CLASSIFIER")


    # new_test.buildClassifier()
    # print("TESTING")
    # new_test.testClassifier("PLANNED_NOT_ACTUAL")
