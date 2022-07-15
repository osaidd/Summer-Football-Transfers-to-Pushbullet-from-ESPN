from bs4 import BeautifulSoup
from pushbullet import Pushbullet
import requests
import datetime as d

#get todays date
day = d.datetime.now().strftime("%b %d")


# to catch any errors
try:

    #pushbullet api key: to send notifs later
    file = open('api_key.txt' , 'r')
    api_key = file.read()

    #initialize pb object
    pb = Pushbullet(api_key)

    #load webpage
    webPage = requests.get('https://www.espn.com/soccer/transfers')
    webPage.raise_for_status()
    #parse
    soup = BeautifulSoup(webPage.text, 'html.parser')
    #Find the table containing all information about transfers
    table = soup.find('tbody').findAll('tr')
    #loop for every transfer in recent times
    
    #formattedstring = string to hold all final information about transfers
    formattedString = ""

    for entries in table:
        
        #Find the transfer date
        EntryDate = entries.find('span' , class_="w-100").text

        #Find all transfers that occured today
        if(EntryDate == day):
            playerName = entries.find('a' , class_ = "AnchorLink").text

            clubs = entries.findAll('span' , class_="hide-mobile")
            oldClub = clubs[0].text
            newClub = clubs[1].text

            price = entries.findAll('span' , class_="w-100")[1].text
            urlName = playerName.replace(" " , "+")
            googleURL = f"https://www.google.com/search?q={urlName}+Transfer"

            #format all the information into a readable message
            formattedString = formattedString + playerName + " confirmed move from " + oldClub + " to " + newClub + " for " + price + "\n " + googleURL + "\n" + "\n"
            

    
    #Send notification to phone      
    push = pb.push_note(day + ' Transfers', formattedString)

except Exception as e:
    print(e)





