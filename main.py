import requests
import re
from bs4 import BeautifulSoup, ResultSet
from typing import List


def main() -> None:
    num_of_pages = find_num_of_pages()
    event_data(num_of_pages)


def find_num_of_pages() -> int: #Loops the counter while the 'next page' button exists to count the number of pages
    #Sees if next button exists on 1st page
    header = data("https://move.unc.edu/calendar/category/athletics/list/?tribe_paged=","tribe-events-header", 
    "li", "tribe-events-nav-next tribe-events-nav-right", 1)
    i = 1
    #While next button exists, increment counter and go to next page
    while len(header) != 0:
        header = data("https://move.unc.edu/calendar/category/athletics/list/?tribe_paged=","tribe-events-header", 
        "li", "tribe-events-nav-next tribe-events-nav-right", i)
        if len(header) == 0:
            print("There are " + str(i) + " pages")
        else:
            i += 1
    return i


def event_data(num_of_pages: int) -> None: #Prints data for all events 
    i = 1
    p = 1
    while i <= num_of_pages:   
        events = data("https://move.unc.edu/calendar/category/athletics/list/?tribe_paged=", "tribe-events-content", 
        "type-tribe_events", p)
        #Finds specific classes corresponding to the event name, time, etc for each event
        #Prints all the data
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
        i += 1
        p += 1


def data(link: str, element: str, class_id: str, class_name: str, page_number: int) -> ResultSet:
    #Get html code through BeautifulSoup
    #Takes in arguments to find specific elements
    url: str = link + str(page_number)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id= element)
    data = results.find_all(class_id, class_= re.compile(class_name))
    return data


if __name__ == "__main__":
    main()
