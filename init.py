import logging

logger = logging.getLogger('TxLog')
logger.setLevel(logging.DEBUG)
logger.info('Logger config message')
fhandler = logging.FileHandler(filename='logfile.log', mode='a')
fhandler.setLevel(logging.DEBUG)
hformatter=logging.Formatter('%(asctime)s %(name)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fhandler.setFormatter(hformatter)
logger.addHandler(fhandler)
#logger.debug('Debugging to file')

import os
import random
import string
import sys
import math

import yaml
from flask import (Flask, g, redirect, render_template, request, session,
                   url_for, Blueprint)
from flask_mysql_connector import MySQL
from mysql.connector import Error

from dbinit import *
from pyconnector import *
from flask_paginate import Pagination, get_page_parameter, get_page_args
from cryptography.fernet import Fernet

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
app.config['MYSQL_PASSWORD'] =db['MYSQL_PASSWORD']
app.config['MYSQL_DATABASE'] =db['MYSQL_DATABASE']
mysql = MySQL(app)

###################
global resetflag  #
resetflag=0       # Set to 1 if you want to reset the db
###################

###################
offset=0       # for pages
page_track=1
###################

#### Homepage HTML ####
@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
   global resetflag
   global offset
   ################################
   dbreinit(logger,mysql,resetflag)   
   ################################
   offset = 0
   resetflag=0

   return render_template('home.html')
   

#########################
#### Login HTML ####
#########################
@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == "POST": ##gets info from form
      mem_username=request.form.get('username')
      mem_password= request.form.get('password')
      getuser="SELECT * FROM Members WHERE mem_username='{}'".format(mem_username)
      cur.execute("SELECT * FROM members WHERE mem_password='{}'", (mem_password))
         
      try:
         getlogin(mysql.connection, mem_username)
         if mem_username != getlogin(mysql.connection, mem_username) or mem_password != decryptpw(mem_password):
            msg = 'Incorrect username or password'
         # cur= mysql.connection.cursor()
         # cur.execute("SELECT * FROM members WHERE mem_username='{}' AND mem_password='{}'", (mem_username, mem_password))
         # members= cur.fetchone()
         #if members[3]==mem_password #compare html hashed password against
            #
         # if (mem_password == __decryptpw(password) and mem_username == username): 
         #    return render_template('profile.html')
         # else:
         #    msg ='Incorrect username or password'
         #    return render_template('login.html')
         # cur.close()
         
      except:
         return -1
   else:
      return render_template('login.html')

#### Logout ####
@app.route('/logout', methods=['GET', 'POST'])
def logout():
   session.clear()
   return render_template('home.html')


#########################
#### sign up HTML ####
#########################
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


###########################
#### request page HTML ####
###########################
@app.route('/request_page', methods=['GET', 'POST'])
def request_page():
   return render_template('request_page.html')

#########################
#### Game page HTML ####
#########################
@app.route('/game_page', methods=['GET', 'POST'])
def game_page():
   return render_template('game_page.html')



#########################
#### Game List HTML ####
#########################
@app.route('/game_list', methods=['GET', 'POST'])
def game_list(page=1):
   global offset
   global page_track
   per_page = 10
   
   if request.method == 'POST':
      if request.form['submit_button'] == 'Forward':
         if(offset < (page_track-1)):
            offset+=1
      elif request.form['submit_button'] == 'Back':
         if(offset > 0):
            offset-=1
         else:
            offset=0   
      else:
            pass # unknown
   elif request.method == 'GET':
      offset = 0
      
   sql_query = "SELECT game_n FROM Game ORDER BY game_n ASC LIMIT {}, {}".format((offset*10), per_page) #offset*10

   gamesL=mysql.connection.cursor()
   gamesL.execute(sql_query)
   VideoGames=gamesL.fetchall()
   VideoGames=[i[0] for i in VideoGames] #removes () and , from each name
   gamesL.close()
   
   
   page_track = math.ceil(len(VideoGames)/10) 

   pagination = Pagination(page=page, 
                           per_page=per_page, 
                           format_number=True, 
                           total=len(VideoGames), 
                           record_name='Video Games' 
                           )
   return render_template('game_list.html', games_list = VideoGames, pagination=pagination)


#########################
#### Profile HTML ####
#########################
# @app.route('/profile', methods=['GET', 'POST'])
# def profile():
#    return render_template('profile.html')
@app.route('/profile', methods=['GET', 'POST'])
def profile():
   return render_template('profile.html')


## Nasic Stuff ##
if __name__ == '__main__':
   app.run(debug=True)
