#!/usr/bin/python -tt
# usr/bin/python -tt

import json, urllib

# MySQL database imports

import mysql.connector
from mysql.connector import errorcode

# import country info file (local)
import country_info
import distance_calculator as dc

import MapFetcher as mf

# import math to compute area searched
import math

# Flask imports

from flask import Flask
# renders HTML file in /templates
from flask import render_template
# requests form data, redirects browser after validation
from flask import request, redirect

app = Flask(__name__)

with open('world.json') as data_file:
    data = json.load(data_file)

# get country list
countries = country_info.getCountryList()

country_names = map(lambda x: x.name, countries)

final_cities = []

for country in country_names:
	try:
		cities = map(lambda x: x.decode('utf-8'),data[country])
		for city in cities:
			final_cities.append(city + " - " + country)
	except (KeyError, UnicodeEncodeError):
		continue

# setup DB connection, cursor
config = {
  'user': 'root',
  'password': 'root',
  'port':'8889',
  'host': 'localhost',
  'database': 'HelloWorld',
  'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock'
}

db_connection = mysql.connector.connect(**config)

# db insertion template

add_search = ("INSERT INTO search"
			"(region, start_date, end_date, population, area, mobile_subs, water_access)"
			"VALUES (%s,%s,%s,%s,%s,%s,%s)")

# connection checker (command line)

if (db_connection):
	print 'works'
else:
	print 'fucked'

# don't forget to close connection after POST/GET !!!

# URL Routing

@app.route('/')
def index():
    return render_template('index.html',cities=final_cities)

#  variables have global scope, are called in the map serving page
start_date_global = ""
end_date_global = ""
country_global = ""
city_global = ""
area_global = 0
population_global = 0
mobile_access_global = 0
water_access_global = 0

@app.route('/search', methods = ['POST','GET'])
def search():
	# in case browser points directly to /search, output error
	if request.method == 'GET':
		return "Sorry, you can't access this page"

	# assigning field data to variables
	region = request.form['region']
	region_city, region_country = region.split(" - ")
	start_date = request.form['start_date']
	end_date = request.form['end_date']

	# getting lat, lon from OSM API call

	# getting and manipulating data from XML
	country = filter(lambda x: x.name == region_country, countries)[0]
	global country_global
	country_global = country

	global city_global
	city_global = region_city

	pop_density = float(country.populationDensity)
	# area of nodes queried in OSM API. Can be set to getter function to MapFetcher
	area = math.pi
	global area_global
	area_global = area

	# population
	population = area * pop_density;
	global population_global
	population_global = population

	# mobile_access
	mobile_subs = 100 - float(country.mobileOwners)
	if mobile_subs <= 0:
		mobile_access = 0
	else:
		mobile_access = pop_density * area * ((mobile_subs)/100)
		global mobile_access_global
		mobile_access_global = mobile_access

	# water_access
	water_access = pop_density * area * (1 - (float(country.waterAccess))/100)
	global water_access_global
	water_access_global = water_access

	# start date string split
	mm, dd, yyyy = start_date.split('/')
	start_date = yyyy + mm + dd
	global start_date_global
	start_date_global = start_date

	# end date string split
	mm, dd, yyyy = end_date.split('/')
	end_date = yyyy	+ mm + dd
	global end_date_global
	end_date_global = end_date

	# creating db instance with form date
	data_search = (region, start_date, end_date, population, area, mobile_access, water_access)
	# opening cursor
	cursor = db_connection.cursor()
	#write to DB
	cursor.execute(add_search, data_search)
	db_connection.commit()
	# closing cursor
	cursor.close()

	# Redirect after successful input
	return redirect('/search_result')

# tester for Leaflet numbers retrieval
@app.route('/search_result')
def test():
	if start_date_global == "" or end_date_global == "" or area_global == 0 or city_global == "":
		return redirect('/')

	# converting global dates to str()
	global start_date_global
	start_date_global = str(start_date_global)
	global end_date_global
	end_date_global = str(end_date_global)

	population = str(int(round(population_global)))
	mobile = str(int(round(mobile_access_global)))
	water = str(int(round(water_access_global)))
	area = str(int(round(area_global)))
	country = country_global

	difference_isEmpty = False

	city = str(city_global)
	constant = 0.009

	try:
		start_coord = mf.get_start(city)
		c_lon, c_lat = start_coord
		min_lon = c_lon - constant
		min_lat = c_lat - constant
		max_lat = c_lat + constant
		max_lon = c_lon + constant

		hospitals, h_ids = mf.get_num_hospitals(city)
		schools, s_ids = mf.get_num_schools(city)
		difference_ways, old_ways = mf.get_difference(city,start_date_global, end_date_global)
	except ValueError:
		difference_isEmpty = True

	return render_template('test.html',ways_updated=difference_ways,ways_old=old_ways,area=area,population=population,mobile=mobile,water=water,country=country, start_coord=start_coord, hospitals=hospitals, schools=schools, min_lon=min_lon, min_lat=min_lat, max_lat=max_lat, max_lon=max_lon)

# page returns clean GEOJSON. JavaScript GETs and parses this. Currently not used.
@app.route("/datatoMap")
def hello():
	return render_template('yeezus.html')

# about page. Project explanations and Credits.
@app.route('/about')
def about():
	return render_template('about.html')

# Error handling

@app.errorhandler(404)
def page_not_found(error):
	return 'You\'re trying to access a page that doesn\'t exist.'

if __name__ == '__main__':
    app.run(debug=True)
