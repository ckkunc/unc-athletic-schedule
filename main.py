from types import NoneType
import requests
import re
from bs4 import BeautifulSoup, ResultSet
from typing import List


def main() -> None: 
    print("\n" + "List of UNC sports: " + "\n")
    list_of_sports()
    sport = input("\n" + "Enter the name of the sport you want to search for: ")
    address = input_data(sport)
    print("")
    event_data(address)
        

def event_data(sport: str) -> None: #Prints data for all events 
    events = data("https://goheels.com/sports/" + sport +  "/schedule", "sidearm-schedule-games-container", 
    "li", "sidearm-schedule-game ")
    #Finds specific classes corresponding to the event name, time, etc for each event
    #Prints all the data
    for event in events:
        home_or_away = event.find("div", class_ = "sidearm-schedule-game-location-indicator home")
        title = event.find("span", class_ = "sidearm-schedule-game-opponent-name")
        date = event.find("div", class_ = "sidearm-schedule-game-opponent-date flex-item-1")
        end_date = event.find("span", class_ = "enddate")
        location = event.find("div", class_ = "sidearm-schedule-game-location")
        time = event.find("div", class_ = "sidearm-schedule-game-time")
        result = event.find("div", class_ = "sidearm-schedule-game-result")
        promotion = event.find("div", class_ = "sidearm-schedule-game-opponent-promotion")

        #Determine if it is home or away game
        if home_or_away == None:
            home_or_away = "AT "
        else:
            home_or_away = "VS "

        print("\n" + "* " + home_or_away + title.text.strip())

        #Checks if entry is a tournament and has multiple dates
        if end_date != None:
            end = end_date.text.strip()
            print(end)
        else:
            print(date.text.strip())

        #Separate location and promotion info and store them as separate variables (if promotion exists)
        #For some reason promotion is a child element of location in the original html
        for x in promotion: 
            x.extract()
            x = x.strip()
        if x == "":
            print(location.text.strip())
        else:
            print(location.text.strip() + "\n" + "Promotion: " + x.strip())

        if time == None:
            print("Result: " + result.text.strip())
        else:
            print(time.text.strip())


def data(link: str, element: str, class_id: str, class_name: str) -> ResultSet:
    #Get html code through BeautifulSoup
    #Takes in arguments to find specific elements
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(class_ = element)
    data = results.find_all(class_id, class_= re.compile(class_name))
    return data


def list_of_sports() -> None:
    html = """
    <select class="c-scoreboard__filter-select" aria-label="Filter games by sport" data-bind="options: sports, 
    value: selectedSport, optionsText: 'title', optionsAfterRender: function(item, value){
    if (item.innerHTML == 'Choose Sport') { item.innerHTML = 'Select Sport' }
    }"><option value="">Select Sport</option><option value="">Baseball</option><option value=""
    >Cross Country</option><option value="">Fencing</option><option value="">Field Hockey</option><option value=""
    >Football</option><option value="">JV Men's Basketball</option><option value=""
    >Men's Basketball</option><option value="">Men's Golf</option><option value=""
    >Men's Lacrosse</option><option value="">Men's Soccer</option><option value=""
    >Men's Tennis</option><option value="">Softball</option><option value=""
    >Swimming &amp; Diving</option><option value="">Track &amp; Field</option><option value=""
    >Volleyball</option><option value="">Women's Basketball</option><option value=""
    >Women's Golf</option><option value="">Women's Gymnastics</option><option value=""
    >Women's Lacrosse</option><option value="">Women's Rowing</option><option value=""
    >Women's Soccer</option><option value="">Women's Tennis</option><option value="">Wrestling</option></select>
    """

    soup = BeautifulSoup(html,"lxml")
    items = soup.select('option[value]')
    sports = [item.text for item in items]
    del sports[0]
    output_list = []
    i = 1
    for sport in sports:
        output_list.append(sport)
        print(str(i) + ": " + output_list[i-1])
        i += 1


def input_data(input: str) -> str:
    output = input
    for char in input:
        if char == "'":
            output = input[:input.index(char)] + input[input.index(char) + 1:]
        elif char == " ":
            output = output[:input.index(char) - 1] + "-" + output[input.index(char):]
    return(output.lower()) 


if __name__ == "__main__":
    main()
