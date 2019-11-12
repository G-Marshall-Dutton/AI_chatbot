import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#Set url
frm = 'NRW'
to = 'London'
date = "181019" #DDMMYY
time = "1645" #HHMM
typ = "dep" #dep/arr
my_url = "http://ojp.nationalrail.co.uk/service/timesandfares/"+frm+"/"+to+"/"+date+"/"+time+"/"+typ

#get page data
uClient = uReq(my_url)
#read data html
page_html = uClient.read()

page_soup = soup(page_html, "html.parser")
elements = page_soup.select('tr[class*="mtx"]')
for index in range(len(elements)):

    element = elements[index]

    tst = element.find("tr", class_="arr").body


    print(index," -> ", tst)
    
#close 
uClient.close()

