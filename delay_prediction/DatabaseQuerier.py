import psycopg2
import pprint
import pandas.io.sql as sqlio

# Test Variables
past_journeys = 'nrch_livst_a51'
stations = 'stations'
test_rid = 201810247681166

# Globals
pp = pprint.PrettyPrinter(indent=4)

# Print without python container syntax (rows)
def printAsRows(list):
    for item in list:
        print(item)

# Print each item's attribute on a new line
def prettyPrint(list):
    pp.pprint(list)


###############################################
############  Fields Reference  ############

# rid   yyyymmdd + index

# tpl   Location TIPLOC (TIPLOCs are used by train planners to identify what time trains should arrive at, depart or pass a particular point)

##### Initial planned times
# pta   Planned Time of Arrival
# ptd   Planned Time of Departure

##### Working Times
# wta   Working (staff) Time of Arrival
# wtp   Working Time of Passing
# wtd   Working Time of Departure

##### Arrival Times
# arr_et          Estimated Arrival Time
# arr_wet         Working Estimated Time
# arr_atRemoved   true if actual replaced by estimated

##### Passing Times
# pass_et         Estimated Passing Time
# pass_wet        Working Estimated Time
# pass_atRemoved  true if actual replaced by estimated


##### Departure Times
# dep_et          Estimated Departure
# dep_wet         Working Estimated Time
# dep_atRemoved   true if actual replaced by estimated

# arr_at    Recorded Actual Time of Arrival
# pass_at   Actual Passing Time
# dep_at    Actual Departure Time
 
##### Reasons/Explanations
# cr_code   Cancellation Reason Code
# lr_code   Late Running Reason


###########################################
###############################################



class DatabaseQuerier:
    
    def __init__(self):
        self.connection = None
        self.cursor = None

    ###########################################################
    ################# Database Connection ##################

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

    ########################################################
    ############################################################

    ############################################################
    ########### Query Functions ############################

    def getTrainJourneyGivenRID(self,rid):
        # Open Connection
        self.openConnection()

        query = """
            SELECT * FROM {0} 
            WHERE rid = '{1}'
            """.format(past_journeys,test_rid)
        
        # Execute query and get results
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        # Close connection
        self.closeConnection()
        return records

    def testReturnDataframe(self,f,t):

        # Open Connection
        self.openConnection()

        query = """
            SELECT rid,tpl,arr_at,tpl_to,dep_at FROM
                (SELECT rid,tpl,dep_at FROM nrch_livst_a51 
                WHERE tpl = 'NRCH'
                AND dep_at IS NOT NULL
                ) AS x
                JOIN
                (SELECT rid AS rid_to,tpl AS tpl_to,arr_at FROM nrch_livst_a51 
                WHERE tpl = 'LIVST'
                AND arr_at IS NOT NULL
                ) AS y on x.rid = y.rid_to
                ORDER BY rid#
                
            """.format(past_journeys,f,t)
        
        # Execute query and get results
        return sqlio.read_sql_query(query, self.connection)

    def getSelectedTrains(self, f, t):

        # Open Connection
        self.openConnection()

        query = """
            SELECT rid,tpl,ptd,dep_at,tpl_to,pta,arr_at FROM
                (SELECT rid,tpl,ptd,dep_at FROM nrch_livst_a51 
                WHERE tpl = '{1}'
                AND dep_at IS NOT NULL
                ) AS x
                JOIN
                (SELECT rid AS rid_to,tpl AS tpl_to,pta,arr_at FROM nrch_livst_a51 
                WHERE tpl = '{2}'
                AND arr_at IS NOT NULL
                ) AS y on x.rid = y.rid_to
            ORDER BY rid
            """.format(past_journeys, f, t)

        # Execute query and get results
        return sqlio.read_sql_query(query, self.connection)

    def getDelayedTrains(self, f, t):
 
        # Open Connection
        self.openConnection()

        query = """
            SELECT rid,tpl,ptd,dep_at,tpl_to,pta,arr_at FROM
                (SELECT rid,tpl,ptd,dep_at FROM nrch_livst_a51 
                WHERE tpl = '{1}'
                AND dep_at IS NOT NULL
                ) AS x
                JOIN
                (SELECT rid AS rid_to,tpl AS tpl_to,pta,arr_at FROM nrch_livst_a51 
                WHERE tpl = '{2}'
                AND arr_at IS NOT NULL
                ) AS y on x.rid = y.rid_to
            WHERE ptd < dep_at
            ORDER BY rid
            """.format(past_journeys, f, t)

        # Execute query and get results
        return sqlio.read_sql_query(query, self.connection)

    def getAllTrains(self, f, t):
       
        # Open Connection
        self.openConnection()

        query = """
            SELECT rid,tpl,ptd,dep_at,tpl_to,pta,arr_at FROM
                (SELECT rid,tpl,ptd,dep_at FROM nrch_livst_a51 
                WHERE tpl = '{1}'
                AND dep_at IS NOT NULL
                AND ptd IS NOT NULL
                ) AS x
                JOIN
                (SELECT rid AS rid_to,tpl AS tpl_to,pta,arr_at FROM nrch_livst_a51 
                WHERE tpl = '{2}'
                AND arr_at IS NOT NULL
                AND pta IS NOT NULL
                ) AS y on x.rid = y.rid_to
            ORDER BY rid
            """.format(past_journeys, f, t)

        # Execute query and get results
        return sqlio.read_sql_query(query, self.connection)

    def getAllPreviousJourneyRIDs(self):
        # Open Connection
        self.openConnection()

        query = """
            SELECT DISTINCT rid FROM {0}
            LIMIT 20
            """.format(past_journeys)
      
          # Execute query and get results
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        # Close connection
        self.closeConnection()
        return records

    def getAllStations(self):
        # Open Connection
        self.openConnection()

        query = """
            SELECT * FROM {0}
            """.format(stations)
        
        # Execute query and get results
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        # Close connection
        self.closeConnection()
        return records

    def getAllData(self, limit):
            # Open Connection
        self.openConnection()

        query = """
            SELECT * FROM {0} LIMIT {1}
            """.format(past_journeys,limit)
        
        # Execute query and get results
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        # Close connection
        self.closeConnection()
        return records

    #######################################################
    ############################################################
    
# TEST HARNESS
if __name__ == '__main__':
    dl = DatabaseQuerier()
    prettyPrint(dl.getTrainJourneyGivenRID(test_rid))

