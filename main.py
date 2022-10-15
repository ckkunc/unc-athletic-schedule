import requests
import re
from bs4 import BeautifulSoup

URL = "https://move.unc.edu/calendar/category/athletics/list/?tribe_paged=1"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="tribe-events-content")
events = results.find_all("div", class_= re.compile("type-tribe_events"))

for event in events:
    title = event.find("h3", class_ = "tribe-events-list-event-title")
    start_time = event.find("span", class_ = "tribe-event-date-start")
    end_time = event.find("span", class_ = "tribe-event-time")
    address = event.find("span", class_ = "tribe-address")
    
    print(title.text)
    print(start_time.text)
    if end_time != None:
        print(end_time.text)
    else:
        print("No scheduled time as of yet")
    print(address.text)

#Loop while "next" button exists in html to get all the pages
#Main function takes input
