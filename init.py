from flask import Flask, render_template, request, redirect, url_for, session #,logging
#from flaskext.mysql import MySQL
from pyconnector import *
from mysql.connector import Error
import random, string
import os, sys
from flask_mysql_connector import MySQL
import yaml

db=yaml.safe_load(open('db.yaml'))

app = Flask(__name__)
app.config['MYSQL_USER'] = db['MYSQL_USER']
app.config['MYSQL_HOST'] = db['MYSQL_HOST']
app.config['MYSQL_PASSWORD'] = db['MYSQL_PASSWORD']
app.config['MYSQL_DATABASE'] = db['MYSQL_DATABASE']
mysql = MySQL(app)

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
   return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == "POST": ##gets info from form
      mem_username=request.form.get('username')
      mem_password= request.form.get('password')
      try:
         cur= mysql.connection.cursor()
         cur.execute("SELECT * FROM members WHERE username=%s", (mem_username))
         members= cur.fetchall()
         cur.close()
      except:
         return -1
   else:
      return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
   session.clear()
   return render_template('home.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
   if request.method=='POST':
      mem_username=request.form.get('username')
      mem_email= request.form.get('email')
      mem_password= request.form.get('password')
      unique_id=random.randint(1,100000)
      print(mem_username)
      print(mem_email)
      print(mem_password)
      user_query ="insert into `Users` (`unique_id`) values ({});".format(unique_id)
      member_query= "insert into `Members` (`unique_id`, `mem_username`, `mem_email`, `mem_password`) values ({},'{}','{}', sha1('{}'));".format(unique_id,mem_username,mem_email,mem_password)
      try:
         addmembers(mysql.connection,unique_id,mem_username,mem_email,mem_password)
         return render_template('signup.html')
      except:
         return -1
   return render_template('signup.html')

@app.route('/request_page', methods=['GET', 'POST'])
def request_page():
   return render_template('request_page.html')

@app.route('/game_page', methods=['GET', 'POST'])
def game_page():
   return render_template('game_page.html')

@app.route('/game_list', methods=['GET', 'POST'])
def game_list():
   return render_template('game_list.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
   return render_template('profile.html')



if __name__ == '__main__':
   app.run(debug=True)