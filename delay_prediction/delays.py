import psycopg2
import pprint

past_journeys = 'nrch_livst_a51'
stations = 'stations'
test_rid = 201810247681166

pp = pprint.PrettyPrinter(indent=4)

# Print without python container syntax (rows)
def printAsRows(list):
    for item in list:
        print(item)

# Print each item's attribute on a new line
def prettyPrint(list):
    pp.pprint(list)

class Delays:
    
    def __init__(self):
        self.connection = None
        self.cursor = None

    def openConnection(self):
        try:
            self.connection = psycopg2.connect(
                user = "ppdb_admin",
                password = "f_6c1V3u",
                host = "mtay.dev",
                port = "5432",
                database = "papa_db")
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)

        if self.connection:
            return True
        else:
            return False

    def closeConnection(self):
        if(self.connection):
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed successfully")

    def getTrainJourneyGivenRID(self,rid):

        query = """
            SELECT * FROM {0} 
            WHERE rid = '{1}'
            """.format(past_journeys,test_rid)

        self.cursor.execute(query)
        records = self.cursor.fetchall()
        return records

# TEST HARNESS
if __name__ == '__main__':
    dl = Delays()
    dl.openConnection()
    prettyPrint(dl.getTrainJourneyGivenRID(test_rid))
    dl.closeConnection()

