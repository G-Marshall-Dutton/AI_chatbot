import datetime

###

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



# Get day as integer as string
def dayIndexToString(index):
    switcher = {
        0: "Mon",
        1: "Tues",
        2: "Weds",
        3: "Thurs",
        4: "Fri",
        5: "Sat",
        6: "Sun",
    }
    return switcher.get(index, "Invalid index")

# Get day as integer as string
def monthIndexToString(index):
    switcher = {
        0: "Jan",
        1: "Feb",
        2: "March",
        3: "April",
        4: "May",
        5: "June",
        6: "July",
        7: "Aug",
        8: "Sept",
        9: "Oct",
        10: "Nov",
        11: "Dec",
    }
    return switcher.get(index, "Invalid index")

# Get day as integer as string
def peakIndexToString(index):
    switcher = {
        0: "Off-Peak",
        1: "Peak",
    }
    return switcher.get(index, "Invalid index")

# Get datetime from seconds
def secondsToTime(seconds):
    return str(datetime.timedelta(seconds=seconds))

# actual value, predicted value, largest difference allowed to be considered accurate
def isAccurate(actual, prediction, maxError):
    if abs(actual - prediction) <= maxError:
        return True
    else:
        return False

# Get the date of journey from its rid
def getDateFromRID(rid):
    date_string = rid[0:8]
    date = datetime.datetime.strptime(date_string, "%Y%m%d")
    return date


    


    


