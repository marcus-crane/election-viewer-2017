from bs4 import BeautifulSoup
from terminaltables import AsciiTable
import requests
import datetime
import time
import sys

def fetchPage():
  r = requests.get("http://www.electionresults.govt.nz/index.html")
  return r.text

def scrapeStats():
  data = []

  page = fetchPage()
  soup = BeautifulSoup(page, 'html.parser')

  table_body = soup.find('tbody')
  rows = table_body.find_all('tr')

  for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    
    data.append(cols)

  return data

def displayStats():
  data = scrapeStats()

  table_data = [
    ["Party", "Party Votes", "Vote %", "Electorate Seats", "List Seats", "Total Seats"],
  ]

  # Fixed a sizing bug
  for entry in data:
    if entry[0] == 'MÄori Party':
      entry[0] = 'Māori Party'

    table_data.append(entry)

  table = AsciiTable(table_data)

  sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=23, cols=106)) # Formats terminal size

  print(table.table)
  print(f"Last updated at {datetime.datetime.now().strftime('%I:%M:%S%p')}") # Display HH:MM:SS AM/PM

while True:
  displayStats()
  time.sleep(5)
