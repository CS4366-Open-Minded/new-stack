import requests
import datetime

API_Key = "AIzaSyDgpcJhAGqk9TUOdIqwfUBTQu91pJMc4rI"

def get_user_location():
    query = 'http://freegeoip.net/json'
    response = requests.get(query).json()

    current_state = response["region_code"].lower()
    current_state_name = response["region_name"]
    current_country = response["country_code"].lower()
    
    return {"country_code": current_country, 
            "state_code": current_state,
            "state_name": current_state_name}


def get_upcoming_election():
    query = "https://www.googleapis.com/civicinfo/v2/elections?key="+ API_Key 
    response = requests.get(query).json()
    
    user_location = get_user_location()
    
    country_code = user_location["country_code"]
    state_code = user_location["state_code"]
    state_name = user_location["state_name"]
    
    elections = []
    
    for election in response["elections"]:
        if(country_code in election["ocdDivisionId"]):
            if(state_code in election["ocdDivisionId"]):
                elections.append(election)
                
    if len(elections) == 0:
        message = "There are no upcoming elections in " + state_name + "."
    
    else:
        string_date = elections[0]["electionDay"]
        day = int(string_date[8:])
        month = int(string_date[5:7])
        year = int(string_date[:4])
        
        string_date = datetime.date(day=day,month=month,year=year).strftime('%A %d, %B %Y')
        
        message = "Upcoming election in " + state_name + " is the "
        message = message + elections[0]["name"] + " "
        message = message + "on " +  string_date + "."
       
    return message   