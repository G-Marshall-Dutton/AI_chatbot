import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#Set url
frm = 'NRW'
to = 'London'
date = "181219" #DDMMYY
time = "1645" #HHMM
typ = "dep" #dep/arr
my_url = "http://ojp.nationalrail.co.uk/service/timesandfares/"+frm+"/"+to+"/"+date+"/"+time+"/"+typ

#get page data
uClient = uReq(my_url)
#read data html
page_html = uClient.read()

page_soup = soup(page_html, "html.parser")
element= page_soup.find("td",{"class":"has-cheapest"}).find("script")

#print("from ", my_url, ", found ",len(elements))
print("-->",element)
# for index in range(len(elements)):
#     arrival = elements[index].findAll("tr",{"class":"arr"})
    
#     print(index," -> ",len(arrival))
    
#close 
uClient.close()


			# {"jsonJourneyBreakdown":
            #     {"departureStationName":"Norwich",
            #     "departureStationCRS":"NRW",
            #     "arrivalStationName":"London Bridge",
            #     "arrivalStationCRS":"LBG",
            #     "statusMessage":"bus service",
            #     "departureTime":"11:30",
            #     "arrivalTime":"14:26",
            #     "durationHours":2,
            #     "durationMinutes":56,
            #     "changes":3,
            #     "journeyId":1,
            #     "responseId":4,
            #     "statusIcon":"AMBER_TRIANGLE",
            #     "hoverInformation":"BUS"},
            # "singleJsonFareBreakdowns":[
            #     {"breakdownType":"SingleFare",
            #     "fareTicketType":"Advance (Standard Class)",
            #     "ticketRestriction":"OA",
            #     "fareRouteDescription":"Only valid on booked Greater Anglia services and suitable connecting services.",
            #     "fareRouteName":"AP GRT ANG ONLY",
            #     "passengerType":"Adult",
            #     "railcardName":"",
            #     "ticketType":"Advance (Standard Class)",
            #     "ticketTypeCode":"OS2","fareSetter":"LER",
            #     "fareProvider":"Greater Anglia",
            #     "tocName":"Greater Anglia",
            #     "tocProvider":"Greater Anglia",
            #     "fareId":26,
            #     "numberOfTickets":1,
            #     "fullFarePrice":17.0,
            #     "discount":0,
            #     "ticketPrice":17.0,
            #     "cheapestFirstClassFare":4.0,
            #     "nreFareCategory":"RESTRICTED",
            #     "redRoute":false}
            #     ],
            #     "returnJsonFareBreakdowns":[]
            #     }
		