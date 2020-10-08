import json
import bs4 as bs
import regex as re

#Not quite accurate, I made some manual edits to the csv

with open('neighborhooddata.csv', 'a') as dataFile:
    with open('Fixed_Neighborhood_Map.kml', 'r') as neighborhoodData:
        kml_soup = bs.BeautifulSoup(neighborhoodData, 'lxml-xml') # Parse as XML
        for place in kml_soup.findAll("Placemark"):
            neighborhoodName = place.find("name").text
            coordinatesFixed = place.find("coordinates").text

            #Regex to fix to desired format
            coordinatesFixed = re.sub(",0", " ", coordinatesFixed)
            coordinatesFixed = re.sub("\s+", " ", coordinatesFixed)[1:]
            #print(coordinatesFixed)

            #Made it so that only the numbers are added with no commas
            dataFile.write(f"{neighborhoodName};{coordinatesFixed}\n")
