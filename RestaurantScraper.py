import requests
import time
import csv
import sys
from bs4 import BeautifulSoup

hygiene = []

def deletelist():
    hygiene.clear()


def savefile():
    filename = input("Please input name of file to be saved")        
    with open (filename + '.csv','w') as file:
       writer=csv.writer(file)
       writer.writerow(['Address','Town', 'Rating'])
       for row in hygiene:
          writer.writerow(row)
    print("File Saved Successfully")


def appendhygiene(scrape):
    hygiene.append(scrape)

def makesoup(url):
    page=requests.get(url)
    print(url + "  scraped successfully")
    return BeautifulSoup(page.text,"lxml")

def hygienescrape(g_data):
    for item in g_data:
        try:
            name = (item.find_all("a", {"class": "name"})[0].text)
        except:
            pass
        try:
            address = (item.find_all("span", {"class": "address"})[0].text)
        except:
            pass
        try:
            bleh = item.find_all('img', {'alt': True})[0]['alt']
            appendhygiene(scrape=[name,address,bleh])
        except:
            pass


def hygieneratingsbyrating():
    
    search = input("Please enter postcode")
    rating = input("Please enter hygiene rating")
    soup=makesoup(url = "https://www.scoresonthedoors.org.uk/search.php?name=&address=" + search + "&postcode=&distance=1&search.x=16&search.y=21&gbt_id=0&award_score=fhrs" + rating)
    hygienescrape(g_data = soup.findAll("div", {"class": "search-result"}))
    
    button_next = soup.find("a", {"rel": "next"}, href=True)
    while button_next:
        time.sleep(2)#delay time requests are sent so we don't get kicked by server
        soup=makesoup(url = "https://www.scoresonthedoors.org.uk/search.php{0}".format(button_next["href"]))
        hygienescrape(g_data = soup.findAll("div", {"class": "search-result"}))

        button_next = soup.find("a", {"rel" : "next"}, href=True)
        
        
        
def hygieneratings():
    
    search = input("Please enter postcode")
    soup=makesoup(url = "https://www.scoresonthedoors.org.uk/search.php?name=&address=&postcode=" + search + "&distance=1&search.x=16&search.y=21&gbt_id=0")
    hygienescrape(g_data = soup.findAll("div", {"class": "search-result"}))
    
    button_next = soup.find("a", {"rel": "next"}, href=True)
    while button_next:
        time.sleep(2)#delay time requests are sent so we don't get kicked by server
        soup=makesoup(url = "https://www.scoresonthedoors.org.uk/search.php{0}".format(button_next["href"]))
        hygienescrape(g_data = soup.findAll("div", {"class": "search-result"}))

        button_next = soup.find("a", {"rel" : "next"}, href=True)


def menu():
        strs = ('Enter 1 to search Food Hygiene ratings by Postcode \n'
                'Enter 2 to search by Post Code and Hygiene Rating Score\n'
                'Enter 3 to Exit\n' )
        choice = input(strs)
        return int(choice) 

while True:          #use while True
    choice = menu()
    if choice == 1:
        hygieneratings()
        savefile()
        deletelist()
    elif choice == 2:
        hygieneratingsbyrating()
        savefile()
        deletelist()
    elif choice == 3:
        break

