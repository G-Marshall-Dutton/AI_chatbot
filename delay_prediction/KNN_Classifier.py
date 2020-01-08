import csv
import datetime
import pandas
from delay_prediction.DatabaseQuerier import DatabaseQuerier

from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split

from delay_prediction.delays import secondsToTime
from delay_prediction.delays import isAccurate


class KNN_Classifier:

    def __init__(self):
        self.classification_data = None
        self.classifier = NearestNeighbors(n_neighbors=1)

    def buildClassifier(self, train):
        # Build classifier from training data

        # Initialize final dataset to be used in classifier
        self.classification_data = pandas.DataFrame(
            columns=["time_at_station_s", "current_delay_s", "rid", "arrival_time_s"])

        count = 0
        for row in train.iterrows():

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
            self.classification_data.loc[count] = [planned_departure.total_seconds(), departure_delay.total_seconds(),
                                                   row[1][0], actual_arrival.total_seconds()]
            count = count + 1

    def classifyInstance(self, features):
        # Classify an set of features return the predicted output
        # from, to, planned_dep_time, delay_mins

        # Get time now as seconds since midnight
        planned_depature_time = datetime.datetime.strptime(features['planned_dep_time'], "%H%M")
        planned_depature_time_s = (planned_depature_time - planned_depature_time.replace(hour=0, minute=0, second=0,
                                                                                         microsecond=0)).total_seconds()
        print("User planned departure at: ", secondsToTime(planned_depature_time_s), "(", planned_depature_time_s, ")")

        delay = int(features['delay_mins']) * 60
        print("User delayed by: ", delay)

        X = self.classification_data.drop(['arrival_time_s', 'rid'], axis=1)  # Remove predicting value for X dataframe
        y = self.classification_data[['arrival_time_s', 'rid']].values  # Seperate target predicting values into own dataframe

        self.classifier.fit(X)

        predictions = self.classifier.kneighbors([[planned_depature_time_s, delay]])  # 0:distance 1:position of neighbour
        predicted_arrival = y[predictions[1]][0][0][0]

        return "You should arrive at " + secondsToTime(predicted_arrival)

    def testClassifier(self):
        # Return the % accuracy given a train and test set (writes result to results file)
        with open('results.csv', mode='a') as results:
            results_writer = csv.writer(results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            results_writer.writerow(["TESTING NN_CLASSIFIER"])

            X = self.classification_data.drop(['arrival_time_s', 'rid'], axis=1)  # Remove predicting value for X dataframe
            y = self.classification_data[
                ['arrival_time_s', 'rid']].values  # Seperate target predicting values into own dataframe

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=9)

            testClassifier = NearestNeighbors(n_neighbors=1)
            testClassifier.fit(X_train)

            count = 0
            numberAccurate = 0
            for row in X_test.iterrows():

                time_at_station_s = row[1][0]
                current_delay_s = row[1][1]

                print("TEST %d    ( %s):      dep_at=%s, delay=%s   ->  arrival:%s" % (
                    count, y_test[count][1], secondsToTime(time_at_station_s), current_delay_s,
                    secondsToTime(y_test[count][0])))

                # Input (Test)
                predictions = testClassifier.kneighbors(
                    [[time_at_station_s, current_delay_s]])  # 0:distance 1:position of neighbour

                predicted_arrival = y_train[predictions[1]][0][0][0]


                # print(predictions[1])
                neighbour_dep_time_s = X_train.iloc[predictions[1][0][0]][0]
                neighbour_delay_s = X_train.iloc[predictions[1][0][0]][1]
                # print(neighbour_dep_time_s,neighbour_delay_s)

                print("   PREDICTED ( %s):      dep_at=%s, delay=%s   ->  arrival:%s" % (
                    y_train[predictions[1][0][0]][1], secondsToTime(neighbour_dep_time_s), neighbour_delay_s,
                    secondsToTime(predicted_arrival)))
                # print("    PREDICTED: dep_at=%s delay=%s   ->  arrival:%s" %(secondsToTime(neighbour_dep_time_s),neighbour_delay_s,secondsToTime(predicted_arrival)))
                # print(y_test[count][0])
                if isAccurate(y_test[count][0], predicted_arrival, 60):
                    numberAccurate = numberAccurate + 1
                    print('\033[92m' + " ACCURATE ")
                else:
                    print('\033[91m' + " NOT ACCURATE")
                count = count + 1
                print('\033[0m', end='')

            accuracy = (numberAccurate / X_test.size) * 100
            print("ACCURACY: ", "(", numberAccurate, "/", X_test.size, ")  ->", accuracy)
            results_writer.writerow([accuracy])

if __name__ == "__main__":

    dq = DatabaseQuerier()
    classifier = KNN_Classifier()

    classifier.buildClassifier(dq.getAllTrains("NRCH","DISS",100))
    print("BUILDING CLASSIFIER COMPLETE")

    classifier.testClassifier()
    print("TESTING CLASSIFIER COMPLETE")

    response = classifier.classifyInstance({"to":"DISS", "from":"NRCH", "planned_dep_time":"1630", "delay_mins":0})
    print(response)
    print("CLASSIFYING INSTANCE COMPLETE")

