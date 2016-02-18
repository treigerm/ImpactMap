#!/usr/bin/python

import json, urllib

# MySQL database imports

import mysql.connector
from mysql.connector import errorcode

# import country info file (local)
import country_info
import distance_calculator as dc

import MapFetcher as mf


#geoJson = json.dumps(geoJson,separators=(',', ':'))

# import math to compute area searched
import math

# Flask imports

from flask import Flask
# renders HTML file in /templates
from flask import render_template
# requests form data, redirects browser after validation
from flask import request, redirect

app = Flask(__name__)

# get country list
countries = country_info.getCountryList()

# setup DB connection, cursor

db_connection = mysql.connector.connect(host='localhost', port='8889', database='HelloWorld',user='root',password='root')

# db insertion template

add_search = ("INSERT INTO search"
			"(region, start_date, end_date, pop_density, area, mobile_subs, water_access)"
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
    return render_template('index.html',countries=countries)

@app.route('/search', methods = ['POST'])
def search():
	# assigning field data to variables
	region = request.form['region']
	start_date = request.form['start_date']
	end_date = request.form['end_date']

	# getting lat, lon from OSM API call

	# USING JAZON'S PSEUDOCODE

	# getting and manipulating data from XML
	country = filter(lambda x: x.name == region, countries)[0]
	pop_density = float(country.populationDensity)
	area = 30
	mobile_subs = 100 - float(country.mobileOwners)

	if mobile_subs <= 0:
		mobile_access = 0
	else:
		mobile_access = pop_density * area * ((mobile_subs)/100)

	water_access = pop_density * area * (1 - (float(country.waterAccess))/100)

	# start date string split
	mm, dd, yyyy = start_date.split('/')
	start_date = dd + mm + yyyy

	# end date string split
	mm, dd, yyyy = end_date.split('/')
	end_date = dd + mm + yyyy

	# non OSM data grab

	# COMPLETE THIS

	# creating db instance with form date
	data_search = (region, start_date, end_date, pop_density, 0, mobile_access, water_access)
	# opening cursor
	cursor = db_connection.cursor()
	#write to DB
	cursor.execute(add_search, data_search)
	db_connection.commit()
	# closing cursor
	cursor.close()

	# Command line checker

	# Redirect after successful input
	return redirect('/')

# tester for Leaflet numbers retrieval
@app.route('/test')
def test():
	return render_template('test.html')

# page returns clean GEOJSON. JavaScript GETs and parses this.
@app.route("/geojson.json")
def hello():
	geojson = mf.get_map_by_name('Chitambo')	
	return json.dumps(geojson)

# about page. Project explanations and Credits.
@app.route('/about')
def about():
	return 'this is us'

# Error handling

@app.errorhandler(404)
def page_not_found(error):
	return 'You\'re trying to access a page that doesn\'t exist.'

if __name__ == '__main__':
    app.run(debug=True)

