from urllib.request import urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from datetime import datetime,date
import time
import pandas as pd
import json
import csv
import operator
import re

def parseDate(dateStr):
	"""Returns the date object using a Date string."""
	date_object = datetime.strptime(dateStr,'%b %d, %Y, %A')
	return date_object.date()

def GetLocation(place):
	"""Return the latitude and longitude of a particular place"""

	url = 'http://maps.googleapis.com/maps/api/geocode/json?'   #api url for google maps

	url = url + urlencode({'sensor':'false','address':place})   #encoding url

	fileData = urlopen(url).read().decode('utf-8')

	dObj = json.loads(fileData)
	if(len(dObj["results"])==0):								# incase no data is received, 
		matching = re.findall(", ([A-Za-z]+)",place)			# find the location for city of the ground
		if(len(matching)):
			latitude,longitude = GetLocation(matching[0])
		else:
			return 0,0											# if nothing is returned then return 0,0
	else:
		latitude = dObj["results"][0]["geometry"]["location"]["lat"]
		longitude = dObj["results"][0]["geometry"]["location"]["lng"]	

	return latitude,longitude


URL = "http://www.cricbuzz.com/cricket-schedule/upcoming-series" # url for list of matches

startDate = date(2016,7,1) 		#start date 1st July 2016
endDate = date(2017,1,31)		#end date   31st Jan 2017

page = urlopen(URL)
soup = BeautifulSoup(page)		#parsing html

numOfMatches = dict()			

# finding data for each date #
matcheDates = soup.find_all("div",{"class" :"cb-col-100 cb-col", "ng-show":"((filtered_category == 0 || filtered_category == 9))"})
for dat in matcheDates:
	date = dat.find("div",{"class":"cb-lv-gray-strip text-bold"})	# getting date in string format from the date block
	if(parseDate(date.string)>= startDate and parseDate(date.string)<=endDate): #checking the range of the date
		
		matches = dat.findAll("div",class_="cb-col-100 cb-col")			#getting all international matches
		
		for match in matches:
			matchTitle = match.find_all("a")				#match's title
			location = match.find_all("div", class_="cb-font-12 text-gray cb-ovr-flo") #match's ground
			time = match.find_all("span")	# match's unix time
			length = len(time)

			# storing the matches in a dictionary with key as locations and value as number of matches #
			for i in range(length):
				if(location[i].string not in numOfMatches):
					numOfMatches[location[i].string] = 1
				else:
					numOfMatches[location[i].string] = numOfMatches[location[i].string] + 1

# removing TBC 
numOfMatches.pop('TBC, TBC',None)

#sorting according to number of matches
numOfMatches = sorted(numOfMatches.items(), key=operator.itemgetter(1),reverse=True)

#storing the data into a csv file to be used by bubble maps
with open("./info.csv", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(["Location","Matches","Lon","Lat"])
    for item in numOfMatches:
    	lat,lon = GetLocation(item[0])
    	writer.writerow([item[0],item[1],lon,lat])




