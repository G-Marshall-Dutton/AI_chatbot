import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json
import pprint
from flask import Flask, render_template,request,make_response,jsonify

class webScraper():


    def scrape(self, journeyDict):

        print("SCRAPING TICKET INFO... ")

        #Set url
        frm = journeyDict['from']
        to = journeyDict['to']
        date = journeyDict['date']
        time = journeyDict['time']
        typ = "dep" 
        my_url = "http://ojp.nationalrail.co.uk/service/timesandfares/"+frm+"/"+to+"/"+date+"/"+time+"/"+typ
    
        print("SCRAPING FROM:  ", my_url)

        #get page data
        uClient = uReq(my_url)

        #read data html
        page_html = uClient.read()

        # Get HTML
        page_soup = soup(page_html, "html.parser")

        # Scrape cheapest ticket info
        element= page_soup.find("td",{"class":"has-cheapest"}).find("script")

        # Remove script tags from 'element'
        text = element.get_text()

        # Find full price from page
        price = page_soup.find("td",{"class":"has-cheapest"}).find("label")
        price = price.get_text()

        # Convert to python Dict
        journeyInfo = json.loads(text)

   
        # Get relevant ticket info
        ticketInfo = {
            "fromStation" : journeyInfo['jsonJourneyBreakdown']['departureStationCRS'],
            "toStation": journeyInfo['jsonJourneyBreakdown']['arrivalStationCRS'],
            "changes": journeyInfo['jsonJourneyBreakdown']['changes'],
            "departureTime": journeyInfo['jsonJourneyBreakdown']['departureTime'],
            "arrivalTime": journeyInfo['jsonJourneyBreakdown']['arrivalTime'],
            "ticketType": journeyInfo['singleJsonFareBreakdowns'][0]['ticketType'],
            "passengerType": journeyInfo['singleJsonFareBreakdowns'][0]['passengerType'],
            "numberOfTickets": journeyInfo['singleJsonFareBreakdowns'][0]['numberOfTickets'],
            "fareRouteName": journeyInfo['singleJsonFareBreakdowns'][0]['fareRouteName'],
            "pageUrl" : my_url,
            "price": price 
        }

            
        #close 
        uClient.close()

        # Print ticket info to console
        pprint.pprint(ticketInfo)

        return ticketInfo





# TEST HARNESS -------------------------------------------------------
# Uncomment everything beneath to run


# #Set url
# frm = 'NRW'
# to = 'London'
# date = "181219" #DDMMYY
# time = "1645" #HHMM
# typ = "dep" #dep/arr
# my_url = "http://ojp.nationalrail.co.uk/service/timesandfares/"+frm+"/"+to+"/"+date+"/"+time+"/"+typ

# #get page data
# uClient = uReq(my_url)
# #read data html
# page_html = uClient.read()

# page_soup = soup(page_html, "html.parser")
# element= page_soup.find("td",{"class":"has-cheapest"}).find("script")

# #print("from ", my_url, ", found ",len(elements))
# print("-->",element)

# # remove script tags from 'element'
# text = element.get_text()

# # Convert to python Dict
# journeyInfo = json.loads(text)

# # Prints the nicely formatted dictionary
# pprint.pprint(journeyInfo)

# fromStation = journeyInfo['jsonJourneyBreakdown']['departureStationName']
# toStation = journeyInfo['jsonJourneyBreakdown']['arrivalStationName']
# changes =  journeyInfo['jsonJourneyBreakdown']['changes']
# ticketType = journeyInfo['singleJsonFareBreakdowns'][0]['ticketType']
# ticketPrice = journeyInfo['singleJsonFareBreakdowns'][0]['ticketPrice']
# passengerType = journeyInfo['singleJsonFareBreakdowns'][0]['passengerType']
# numberOfTickets = journeyInfo['singleJsonFareBreakdowns'][0]['numberOfTickets']
# fareRouteName = journeyInfo['singleJsonFareBreakdowns'][0]['fareRouteName']


# print("-!!!-", journeyInfo['jsonJourneyBreakdown']['departureStationName'])


# # for index in range(len(elements)):
# #     arrival = elements[index].findAll("tr",{"class":"arr"})
    
# #     print(index," -> ",len(arrival))
    
# #close 
# uClient.close()


# 			# {"jsonJourneyBreakdown":
#             #     {"departureStationName":"Norwich",
#             #     "departureStationCRS":"NRW",
#             #     "arrivalStationName":"London Bridge",
#             #     "arrivalStationCRS":"LBG",
#             #     "statusMessage":"bus service",
#             #     "departureTime":"11:30",
#             #     "arrivalTime":"14:26",
#             #     "durationHours":2,
#             #     "durationMinutes":56,
#             #     "changes":3,
#             #     "journeyId":1,
#             #     "responseId":4,
#             #     "statusIcon":"AMBER_TRIANGLE",
#             #     "hoverInformation":"BUS"},
#             # "singleJsonFareBreakdowns":[
#             #     {"breakdownType":"SingleFare",
#             #     "fareTicketType":"Advance (Standard Class)",
#             #     "ticketRestriction":"OA",
#             #     "fareRouteDescription":"Only valid on booked Greater Anglia services and suitable connecting services.",
#             #     "fareRouteName":"AP GRT ANG ONLY",
#             #     "passengerType":"Adult",
#             #     "railcardName":"",
#             #     "ticketType":"Advance (Standard Class)",
#             #     "ticketTypeCode":"OS2","fareSetter":"LER",
#             #     "fareProvider":"Greater Anglia",
#             #     "tocName":"Greater Anglia",
#             #     "tocProvider":"Greater Anglia",
#             #     "fareId":26,
#             #     "numberOfTickets":1,
#             #     "fullFarePrice":17.0,
#             #     "discount":0,
#             #     "ticketPrice":17.0,
#             #     "cheapestFirstClassFare":4.0,
#             #     "nreFareCategory":"RESTRICTED",
#             #     "redRoute":false}
#             #     ],
#             #     "returnJsonFareBreakdowns":[]
#             #     }
		