from flask import Flask, render_template, request, redirect, url_for#, session,logging
from flaskext.mysql import MySQL
#from flask_mysqldb import MySQL

import random, string
import os, sys

app = Flask(__name__)

mysql = MySQL()
#connect=create_db_connection("localhost","root","1234","+games")

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = '+games'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
   return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
   return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
   # if request.method=='POST':
   #    memdata= request.form
   #    mem_username=memdata['username']
   #    mem_email= memdata['email']
   #    mem_password= memdata['password']
   #    cur= mysql.connection.cursor()
   #    unique_id=random.randint(1,100000)
   #    user_query ="insert into `Users` (`unique_id`) values ({});".format(unique_id)
   #    member_query= "insert into `Members` (`unique_id`, `mem_username`, `mem_email`, `mem_password`) values ({},'{}','{}', sha1('{}'));".format(unique_id,mem_username,mem_email,mem_password)
   #    try:
   #       cur.execute(user_query)
   #       cur.execute(member_query)
   #    except:
   #       exit
   return render_template('signup.html')

@app.route('/request', methods=['GET', 'POST'])
def request():
   return render_template('request.html')

@app.route('/example', methods=['GET', 'POST'])
def example():
   result = (request.form['result'])
   cursor = connection.cursor()
   cursor.execute("get database testing result", result)
   return render_template('example.html', result = result)

@app.route('/game_page', methods=['GET', 'POST'])
def game_page():
   return render_template('game_page.html')

@app.route('/game_list', methods=['GET', 'POST'])
def game_list():
   return render_template('game_list.html')

if __name__ == '__main__':
   app.run()