# XML Parser import

import xml.etree.ElementTree as ET
# this is a local xml file. Could be called from the Java parser?
tree = ET.parse('countries.xml')
root = tree.getroot()

# command line checker
"""for child in root:
	for baby in child:
		print baby.text"""

# class to access

class Country(object):
	def __init__(self, name, populationDensity, mobileOwners, waterAccess):
		self.name = name
		self.populationDensity = populationDensity
		self.mobileOwners = mobileOwners
		self.waterAccess = waterAccess

# init empty array

def getCountryList():
	# init array of 'empty' countries in XML file
	countriesCounter = 0

	for country in root.findall('Country'):
		countriesCounter = countriesCounter + 1

	countries = [Country('','','','') for x in range(countriesCounter)]
	i = 0

	# fill array with fetched countries
	for country in root:
		countries[i] = Country(country.find('Name').text,country.find('PopulationDensity').text,country.find('MobileOwners').text,country.find('WaterAccess').text)	
		i = i + 1

	return countries