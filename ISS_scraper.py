#The code will create a csv file containing the date and time of the flyover, duration of time the ISS is visible, maximum height in the sky,
#direction of appearance and disappearance in the sky and weather forecast.

import requests
from bs4 import BeautifulSoup
import csv

###################################
URL_ISS = "https://spotthestation.nasa.gov/URL" ##EXAMPLE: https://spotthestation.nasa.gov/sightings/view.cfm?country=Croatia&region=None&city=Zagreb
URL_WEATHER = "https://www.yr.no/en/forecast/daily-table/URL" ##EXAMPLE: https://www.yr.no/en/forecast/daily-table/2-3186886/Croatia/City%20of%20Zagreb/Zagreb
####################################

r = requests.get(URL_ISS)
soup = BeautifulSoup(r.content, 'html5lib')

table = soup.find('table', attrs={'class':'table table-striped table-condensed table-hover table-bordered'})

rows = table.find_all('tr')

sightings = []

headers =['Date', 'Visible for', 'Max_Height', 'Appears', 'Disappears', 'Weather']

for data in rows:
    counter = 0
    row = {}
    for td in data.find_all('td'):
        if counter < 5:
            row[headers[counter]] = td.text
            counter += 1
    if len(row) !=0 :
        height = int(row['Max_Height'].replace('°',''))
        if height > 40:
            sightings.append(row)

time_of_day = [[1,2,3,4,5,6],
              [6,7,8,9,10,11],
              [12,13,14,15,16,17],
              [18,19,20,21,22,23]]


r_weather = requests.get(URL_WEATHER)
soup_weather = BeautifulSoup(r_weather.content, 'html5lib')
weather = soup_weather.find_all('li', attrs={'class':'daily-weather-list-item'})

for sight in sightings:
    date_time = sight['Date'].split(', ')
    date = date_time[0].split()[2]
    time_hour = date_time[1].split()[0].split(':')[0]
    time_am_pm = date_time[1].split()[1]
    
    if time_am_pm == 'PM':
        if time_hour == '12':
            time_24 = int(time_hour)
        else:
            time_24 = int(time_hour)+12
    else:
        if time_hour == '12':
            time_24 = int(time_hour)-12
            
    if time_24 in time_of_day[0]:
        search = '0'
    elif time_24 in time_of_day[1]:
        search = '1'
    elif time_24 in time_of_day[2]:
        search = '2'
    else:
        search = '3'
            
    for row in weather:
        if int(row.div.a.h3.text.split()[1]) == int(date):
                forecast_row = row.find('li', attrs={'class':f'daily-weather-list-item__symbol daily-weather-list-item__symbol-{search}'})
                forecast=forecast_row.div.img['alt'].split()[1]
                sight['Weather']=forecast



filename = r'C:\PATH TO FILE\ISS.csv' ##EXAMPLE: r'C:\Users\User\Desktop\ISS.csv'

with open (filename, 'a', newline='',) as f:
    w = csv.DictWriter(f, headers, delimiter=';')
    w.writeheader()
    for sight in sightings:
        w.writerow(sight)

