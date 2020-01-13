from delay_prediction.StationBasedForestClassifier import StationBasedForestRegressor
from delay_prediction.delays import secondsToTime
from joblib import dump, load

class DelayController:

    def __init__(self):
        # Initialise best classifier
        self.classifier = load('classifier.joblib')

    def get_delay(self, user_information):
        delay = self.classifier.classifyInstance(user_information)
        if delay is None:
            return "Error finding valid information on route"
            # delayb = self.classifierb.classifyInstance(user_information)
        return "You should arrive at close to: " + secondsToTime(delay)

if __name__ == "__main__":
    dc = DelayController()
    print("done")
    a = dc.get_delay({"to":"LIVST", "from":"NRCH", "planned_dep_time":"0500", "delay_mins":0})
    print(secondsToTime(a))