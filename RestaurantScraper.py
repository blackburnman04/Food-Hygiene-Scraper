import requests
import time
from prettytable import from_csv
import csv
import sys
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk, Image


path = "scoresondoors.jpg" # image file name for logo to be displayed in root window (must be in same directory as running script)

hygiene = []



def deletelist():
    hygiene.clear()


def gui_input(prompt):

    root = tk.Toplevel()
    # this will contain the entered string, and will
    # still exist after the window is destroyed
    var = tk.StringVar()

    # create the GUI
    label = tk.Label(root, text=prompt)
    entry = tk.Entry(root, textvariable=var)
    label.pack(side="left", padx=(20, 0), pady=20)
    entry.pack(side="right", fill="x", padx=(0, 20), pady=20, expand=True)

    # Let the user press the return key to destroy the gui
    entry.bind("<Return>", lambda event: root.destroy())

    # this will block until the window is destroyed
    root.wait_window()

    # after the window has been destroyed, we can't access
    # the entry widget, but we _can_ access the associated
    # variable
    value = var.get()
    return value


# Display a string in `out_label`
def print_to_gui(text_string):
    status_label.config(text=text_string)
    # Force the GUI to update
    root.update()


def savefile():
    filename = gui_input("Please input name of file to be saved")
    with open (filename + '.csv','w') as file:
       writer=csv.writer(file)
       writer.writerow(['Address','Town', 'Rating'])
       for row in hygiene:
          writer.writerow(row)
    print("File Saved Successfully")
    print_to_gui("CSV File Saved Successfully")


def appendhygiene(scrape):
    hygiene.append(scrape)

def makesoup(url):
    page=requests.get(url)
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

    search = gui_input("Please enter postcode")
    rating = gui_input("Please enter rating")
    soup=makesoup(url = "https://www.scoresonthedoors.org.uk/search.php?name=&address=" + search + "&postcode=&distance=1&search.x=16&search.y=21&gbt_id=0&award_score=fhrs" + rating)
    hygienescrape(g_data = soup.findAll("div", {"class": "search-result"}))

    button_next = soup.find("a", {"rel": "next"}, href=True)
    while button_next:
        time.sleep(2)#delay time requests are sent so we don't get kicked by server
        soup=makesoup(url = "https://www.scoresonthedoors.org.uk/search.php{0}".format(button_next["href"]))
        hygienescrape(g_data = soup.findAll("div", {"class": "search-result"}))

        button_next = soup.find("a", {"rel" : "next"}, href=True)

    savefile()
    deletelist()



def hygieneratings():
    search = gui_input("Please enter postcode")
    soup=makesoup(url = "https://www.scoresonthedoors.org.uk/search.php?name=&address=&postcode=" + search + "&distance=1&search.x=16&search.y=21&gbt_id=0")
    hygienescrape(g_data = soup.findAll("div", {"class": "search-result"}))

    button_next = soup.find("a", {"rel": "next"}, href=True)
    while button_next:
        time.sleep(2)#delay time requests are sent so we don't get kicked by server
        soup=makesoup(url = "https://www.scoresonthedoors.org.uk/search.php{0}".format(button_next["href"]))
        hygienescrape(g_data = soup.findAll("div", {"class": "search-result"}))

        button_next = soup.find("a", {"rel" : "next"}, href=True)
        print_to_gui("Scraping Ratings")

    print_to_gui("Ratings Scraped")
    savefile()
    deletelist()


def quit():
    root.quit()




# GUI Code Tkinter

root = tk.Tk()
root.resizable(False, False)
root.geometry("1000x450")
root.wm_title("Hygiene Check- Scores on the Doors Food Hygience Check")
Label = tk.Label(root, text='Food Hygiene Check\n Scores on the Doors Food Hygiene', font=('Comic Sans MS', 18))
button = tk.Button(root, text="Search by Postcode", command=hygieneratings)
button2 = tk.Button(root, text="Search by Postcode & Rating", command=hygieneratingsbyrating)
button3 = tk.Button(root, text="Quit Program", command=quit)
Label.pack()
button.pack()
button2.pack()
button3.pack()
status_label = tk.Label(text="")
status_label.pack()
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")
root.mainloop()
