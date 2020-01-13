from delay_prediction.StationBasedForestClassifier import StationBasedForestRegressor
from delay_prediction.delays import secondsToTime
from joblib import dump, load

class DelayController:

    def __init__(self):
        # Initialise best classifier
        self.classifier = load('classifier.joblib')
        self.classifierb = load('classifier_updated.joblib')

    def get_delay(self, user_information):
        delay = self.classifier.classifyInstance(user_information)
        delayb = self.classifierb.classifyInstance(user_information)
        return delay,delayb

if __name__ == "__main__":
    dc = DelayController()
    print("done")
    a,b = dc.get_delay({"to":"LIVST", "from":"IPSWICH", "planned_dep_time":"2000", "delay_mins":0})
    print(secondsToTime(a), secondsToTime(b))
    a, b = dc.get_delay({"to": "LIVST", "from": "IPSWICH", "planned_dep_time": "2000", "delay_mins": 5})
    print(secondsToTime(a),secondsToTime(b))