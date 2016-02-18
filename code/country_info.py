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
		# mobile subscription per 100 people
		self.mobileOwners = mobileOwners
		# % of people having access to clean water
		self.waterAccess = waterAccess

# init empty array

def getCountryList():
	# init array of 'empty' countries in XML file
	countriesCounter = 0

	for country in root.findall('Country'):
		countriesCounter = countriesCounter + 1

	countries = [Country('',0,0,0) for x in range(countriesCounter)]
	i = 0

	# fill array with fetched countries
	for country in root:

		name 			= country.find('Name').text
		pop_density 	= country.find('PopulationDensity').text
		mobile_subs 	= country.find('MobileOwners').text
		water_access 	= country.find('WaterAccess').text
		countries[i]	= Country(name,pop_density,mobile_subs,water_access)	
		i = i + 1

	return countries