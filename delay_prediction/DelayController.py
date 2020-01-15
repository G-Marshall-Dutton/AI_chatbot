from delay_prediction.StationBasedForestClassifier import StationBasedForestRegressor
from delay_prediction.StationBasedVersion3 import StationBasedVersion3
from delay_prediction.delays import secondsToTime
from joblib import dump, load

class DelayController:

    def __init__(self):
        # Initialise best classifier
        #self.classifier = load('/Users/georgemarshall-dutton/AI_chat_bot/delay_prediction/classifier.joblib')
        # test = StationBasedVersion3()
        # test.buildClassifier(5000)
        # dump(test, 'final_classifier.joblib')
        self.classifier = load('/Users/georgemarshall-dutton/AI_chat_bot/final_classifier.joblib')

    def get_delay(self, user_information):
        delay, message = self.classifier.classifyInstance(user_information)
        if delay is None:
            return message
            # delayb = self.classifierb.classifyInstance(user_information)
        return "You should arrive at close to: " + secondsToTime(delay)

if __name__ == "__main__":
    dc = DelayController()
    print("done")
    a = dc.get_delay({"to":"LIVST", "from":"NRCH", "planned_dep_time":"0500", "delay_mins":0})
    print(secondsToTime(a))