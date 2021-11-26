import mysql.connector
import json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
  return "Let's test workflow!"

@app.route('/widgets')
def get_widgets():
	mydb = mysql.connector.connect(
		host="mysqldb",
		user="root",
		password="secret",
		database="inventory"
	)
	cursor = mydb.cursor()

	cursor.execute("Select * from widgets")

	row_headers=[x[0] for x in cursor.description]

	results = cursor.fetchall()
	json_data=[]
	for result in results:
		json_data.append(dict(zip(row_headers,result)))

	cursor.close()

	return json.dumps(json_data)

@app.route('/initdb')
def db_init():
	mydb = mysql.connector.connect(
		host="mysqldb",
		user="root",
		password="secret"
	)

	cursor = mydb.cursor()
	cursor.execute("drop database if exists inventory")
	cursor.execute("create database inventory")
	cursor.close()
	
	mydb = mysql.connector.connect(
		host="mysqldb",
		user="root",
		password="secret",
		database="inventory"
	)
	
	cursor = mydb.cursor()

	cursor.execute("drop table if exists widgets")
	cursor.execute("create table widgets (name varchar(255), description varchar(255))")
	cursor.close()

	return 'init database'

if __name__ == "__main__":
	app.run(host ='0.0.0.0')
