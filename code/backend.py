#!/usr/bin/python

import json, urllib

# MySQL database imports

import mysql.connector
from mysql.connector import errorcode

# Flask imports

from flask import Flask
# renders HTML file in /templates
from flask import render_template
# requests form data, redirects browser after validation
from flask import request, redirect

app = Flask(__name__)

# setup DB connection, cursor

db_connection = mysql.connector.connect(host='localhost', port='8889', database='HelloWorld',user='root',password='root')

# db insertion template

add_search = ("INSERT INTO search"
			"(region, start_date, end_date, pop_density, area, mobile_subs, water_access)"
			"VALUES (%s,%s,%s,%s,%s,%s,%s)")

# connection checker (terminal)

if (db_connection):
	print 'works'
else:
	print 'fucked'

# don't forget to close connection after POST/GET !!!

# URL Routing

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods = ['POST'])
def search():
	# assigning field data to variables
	region = request.form['region']
	start_date = request.form['start_date']
	end_date = request.form['end_date']

	# start date string split
	mm, dd, yyyy = start_date.split('/')
	start_date = dd + mm + yyyy

	# end date string split
	mm, dd, yyyy = end_date.split('/')
	end_date = dd + mm + yyyy

	# creating db instance with form date
	data_search = (region, start_date, end_date, 0, 0, 0, 0)
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

@app.route('/about')
def about():
	return 'this is us'

# Error handling

@app.errorhandler(404)
def page_not_found(error):
	return 'You\'re trying to access a page that doesn\'t exist.'

if __name__ == '__main__':
    app.run(debug=True)

# JSON getter example

j = json.loads('{"one" : "1", "two" : "2", "three" : "3"}')
print j['two']