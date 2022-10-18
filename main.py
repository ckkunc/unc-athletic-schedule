import requests
import re
from bs4 import BeautifulSoup, ResultSet


def main() -> None:
    sport = input("What sport do you want to search for? ")
    event_data(sport)
        

def event_data(sport: str) -> None: #Prints data for all events 
    events = data("https://goheels.com/sports/" + sport +  "/schedule", "sidearm-schedule-games-container", 
    "li", "sidearm-schedule-game ")
    #Finds specific classes corresponding to the event name, time, etc for each event
    #Prints all the data
    for event in events:
        home_or_away = event.find("span", class_ = "sidearm-schedule-game-conference-vs flex flex-inline")
        title = event.find("div", class_ = "sidearm-schedule-game-opponent-name")
        time = event.find("div", class_ = "sidearm-schedule-game-opponent-date flex-item-1")

        print("* " + home_or_away.text.strip().upper() + " " + title.text.strip())
        print(time.text, end="\n"*2)


def data(link: str, element: str, class_id: str, class_name: str) -> ResultSet:
    #Get html code through BeautifulSoup
    #Takes in arguments to find specific elements
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(class_ = element)
    data = results.find_all(class_id, class_= re.compile(class_name))
    return data


if __name__ == "__main__":
    main()
