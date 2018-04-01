# import libraries
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
sheet = client.open("Scrap event website").sheet1

#Specify url
url_to_scrap = 'https://' # Specify website
page = requests.get(url_to_scrap)
# print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')

# evts=[]
table = soup.find_all('tbody')[0]
rows = table.find_all('tr', {'class': ''})[1::]

for tr in rows:
    if( tr.p or tr.a ):
        date = tr.p.text        # Specify content
        evt = tr.a.text
        location = tr.find_all('p')[-1].text
        url = tr.a.get('href')
        evtDetails = 'Date: {0}, Event: {1}, Location: {2}, URL: {3}'.format(date, evt, location, url)
        sheet.append_row([date, evt, location, url])

        # evts.append(evtDetails)
# print(evts)
