import logging
logger = logging.getLogger('TxLog')
logger.setLevel(logging.DEBUG)
logger.debug('Logger config message')
fhandler = logging.FileHandler(filename='logfile.log', mode='a')
fhandler.setLevel(logging.DEBUG)
hformatter=logging.Formatter('%(asctime)s %(name)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fhandler.setFormatter(hformatter)
logger.addHandler(fhandler)
#logger.debug('Debugging to file')

from flask import Flask, render_template, request, redirect, url_for, session #, g
from pyconnector import *
from mysql.connector import Error
from flask_mysql_connector import MySQL

import random, string
import os, sys 
import yaml



db=yaml.safe_load(open('db.yaml'))
#Create a db.yaml file in the base directory and put the following 4 lines in it. Add it to .gitignore so you keep your own independent config files.
#MYSQL_USER: 'root'
#MYSQL_HOST: 'localhost'
#MYSQL_PASSWORD: 'your_mysql_password'
#MYSQL_DATABASE: '+games'
#
app = Flask(__name__)
app.config['MYSQL_USER'] = db['MYSQL_USER']
app.config['MYSQL_HOST'] = db['MYSQL_HOST']
app.config['MYSQL_PASSWORD'] = db['MYSQL_PASSWORD']
app.config['MYSQL_DATABASE'] = db['MYSQL_DATABASE']
mysql = MySQL(app)

#### Homepage HTML ####
@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
   return render_template('home.html')


#### Login HTML ####
@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == "POST":
      mem_username=request.form.get('username')
      mem_password= request.form.get('password')
      
      cur= mysql.connection.cursor()
      cur.execute("SELECT * FROM members WHERE username=%s AND password=%s")
      # fetch all results and return
      members= cur.fetchall()
      
      # if len(members) > 0:
      #    if(bcyrpt.check_haspw(mem_password, members('password').encode('utf-8')) == members('password').encode('utf-8'):
      #       session('username') = mem_username('username')
      #       session('password') = user('password')
      #       msg = 'you logged in'
      #       return render_template('profile.html')
      #    else:
      #       msg = 'Invalid username or password'
      #       return render_template('login.html')
         # creating a session to be accessed in other routes
         # session('username') = members('username')
      cur.close()
      return render_template('profile.html')
   else:
      return render_template('login.html')

#### Logout ####
@app.route('/logout', methods=['GET', 'POST'])
def logout():
   session.clear()
   return render_template('home.html')



#### sign up HTML ####
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







#### request page HTML ####
@app.route('/request_page', methods=['GET', 'POST'])
def request_page():
   return render_template('request_page.html')

#### Game page HTML ####
@app.route('/game_page', methods=['GET', 'POST'])
def game_page():
   return render_template('game_page.html')

#### Game List HTML ####
@app.route('/game_list', methods=['GET', 'POST'])
def game_list():
   return render_template('game_list.html')

#### Profile HTML ####
# @app.route('/profile', methods=['GET', 'POST'])
# def profile():
#    return render_template('profile.html')


##############################
####       Database      ####
#############################
@app.route('/profile', methods=['GET','POST'])
def profile():
   if request.method=='POST':
      print(game_id)
      print(g_company)
      print(game_n)
      print(genre)
      print(rating)
      print(release_Date)
      print(price)
      ##
      try:
         sortbyalphabetical(mysql.connection)
         return render_template('profile.html')
      except:
         return -1

   return render_template('profile.html')




# class results(table):
#   game_id = columns('Game ID')      
#   g_company = columns('Company')		
#   game_n = columns('Game Name')		
#   genre = columns('Genre')			
#   rating = columns('Rate') 		
#   release_Date = columns('Release')
#   price	= columns('Price')




## Nasic Stuff ##
if __name__ == '__main__':
   app.run(debug=True)
