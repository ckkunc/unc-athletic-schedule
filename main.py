import requests
import re
from bs4 import BeautifulSoup, ResultSet
from typing import List


def main() -> None:
    num_of_pages: int = find_num_of_pages()
    data(num_of_pages)

# this is the feature-next branch
def find_num_of_pages() -> int:
    i = 1
    page_number: str = str(i)
    url: str = "https://move.unc.edu/calendar/category/athletics/list/?tribe_paged=" + page_number
    URL = url
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="tribe-events-header")
    header = results.find_all("li", class_= re.compile("tribe-events-nav-next tribe-events-nav-right"))

    while len(header) != 0:
        
        page_number: str = str(i)
        url: str = "https://move.unc.edu/calendar/category/athletics/list/?tribe_paged=" + page_number
        URL = url
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="tribe-events-header")
        header = results.find_all("li", class_= re.compile("tribe-events-nav-next tribe-events-nav-right"))
        print("data for " + str(i))
        if len(header) == 0:
            print("There are no more events")
        else:
            
            i += 1
        return i



def data(num_of_pages: int) -> None:
    while i <= num_of_pages:
        i = 1
        p = 1
        page_number: str = str(p)
        url: str = "https://move.unc.edu/calendar/category/athletics/list/?tribe_paged=" + page_number
        URL = url
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="tribe-events-content")
        events = results.find_all("div", class_= re.compile("type-tribe_events"))
        i += 1
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



if __name__ == "__main__":
    main()
