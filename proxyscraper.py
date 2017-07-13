import csv
import requests
from bs4 import BeautifulSoup


url = 'https://www.sslproxies.org/'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, "lxml")
table = soup.find('table', attrs={'id': 'proxylisttable'})

list_of_rows = []
for row in table.findAll('tr'):
    list_of_cells = []
    for cell in row.findAll('td'):
        text = cell.text.replace('&nbsp;', '')
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)

filename = input("Please input name of file to be saved")        
with open (filename + '.csv','w') as file:
    writer=csv.writer(file)
    writer.writerow(['IP Address','Port', 'Code', 'Country', 'Anonymoity', 'Google', 'HTTPS', 'Last Checked'])
    for row in list_of_rows:
        writer.writerow(row)
print("File Saved Successfully")
