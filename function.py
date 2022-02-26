
from datetime import datetime
import json
import urllib.request as urllib2
from dataclasses import dataclass, field
from typing import List

# Set up ISS Data class to store default values in case of failure


@dataclass
class ISSData:
    message: str = "success"
    timestamp: datetime = 123456789
    iss_position: List = field(default_factory=lambda:
                               {"longitude": "-10.1234", "latitude": "31.41592"})

# Set up Person in Space data class to store default values in case of failure


@dataclass
class PersonData:
    message: str = "success"
    people: List = field(default_factory=lambda: [{"name": "James Tiberius Kirk", "craft": "NCC-1701"}, {
                         "name": "Chris Hadfield", "craft": "ISS"}, {"craft": "NCC-1701", "name": "S’chn T’gai Spock"}, {"name": "Hikaru Kato Sulu"}])

# Setting up api call to be reused for both the person and location endpoints


def getReq(endpoint):
    req = urllib2.Request("http://api.open-notify.org/" + endpoint + ".json")
    response = urllib2.urlopen(req)
    obj = json.loads(response.read())
    return obj

# Function to get the current lat and long of the ISS


def locateiss():
    data = getReq("iss-now")
    if data['message'] == "success":
        data = ISSData(data['message'], data['timestamp'],
                       data['iss_position'])
    else:
        data = ISSData()
    print("The ISS current location at ",
          data.timestamp, " is {", data.iss_position['latitude'], " , ", data.iss_position['longitude'], "}")

# function to get the count of people in space, the craft, and the astronauts aboard


def GetSpacePeople():
    data = getReq("astros")
    if data['message'] == 'success':
        data = PersonData(data['message'], data['people'])
    else:
        data = PersonData()
    craft = data.people[0]['craft']
    astros = []
    # need to loop through the people field and append astronauts to a list for simplified retrieval
    for astronaut in data.people:
        astros.append([astronaut][0]['name'])
    print("There are ", len(astros), " people aboard the ",
          craft, ". They are ", ', '.join(astros), ".")
