from delay_prediction.KNN_Classifier import KNN_Classifier
from delay_prediction import DatabaseQuerier

class DelayController:

    def __init__(self):
        # Initialise best classifier
        self.classifier = KNN_Classifier()
        self.classifier.buildClassifier(DatabaseQuerier.DatabaseQuerier().getAllTrains("NRCH","DISS",100))

    def get_delay(self, user_information):
        delay = self.classifier.classifyInstance(user_information)
        return delay

if __name__ == "__main__":
    dc = DelayController()
    print(dc.get_delay({"to":"DISS", "from":"NRCH", "planned_dep_time":"1630", "delay_mins":0}))