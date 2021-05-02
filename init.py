# SJSU CMPE 138 Spring 2021 TEAM1
# $env:FLASK_APP = "init.py"    
# $env:FLASK_ENV = "development"
# python -m flask run    
import logging
logger = logging.getLogger('initLog')
logger.setLevel(logging.DEBUG)
logger.debug('Logger config message')
fhandler = logging.FileHandler(filename='logfile.log', mode='a',encoding='utf-8')
fhandler.setLevel(logging.DEBUG)
hformatter=logging.Formatter('%(asctime)s %(name)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fhandler.setFormatter(hformatter)
logger.addHandler(fhandler)
logger.debug('Debugging to file')

import os
import random
import string
import sys
import math
import base64
import yaml
from flask import (Flask, g, redirect, render_template, request, session,
                   url_for, Blueprint, escape, flash)
from flask_mysql_connector import MySQL
from mysql.connector import Error
from flask_login import (LoginManager, logout_user, logout_user, 
                         login_required, current_user)

import functools 

from dbinit import *
from pyconnector import *
from flask_paginate import Pagination, get_page_parameter, get_page_args
import hashlib
import binascii

db=yaml.safe_load(open('db.yaml'))
#Create a db.yaml file in the base directory and put the following 4 lines in it. Add it to .gitignore so you keep your own independent config files.
#MYSQL_USER: 'root'
#MYSQL_HOST: 'localhost'
#MYSQL_PASSWORD: 'your_mysql_password'
#MYSQL_DATABASE: '+games'
#


app = Flask(__name__)
app.secret_key = "12345"
app.config['MYSQL_USER'] = db['MYSQL_USER']
app.config['MYSQL_HOST'] = db['MYSQL_HOST']
app.config['MYSQL_PASSWORD'] =db['MYSQL_PASSWORD']
app.config['MYSQL_DATABASE'] =db['MYSQL_DATABASE']
mysql = MySQL(app)



login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# login = LoginManager()
# login.login_view = 'login'
# login.init_app(app)
#------------------------------------------------------------------------------
global resetflag     #
resetflag=0          # Set to 1 if you want to reset the db
global resetflagcsv  # 
resetflagcsv=0       # Set to 1 if you want to reimport the csv to database
##########################################################################
offset=0             # for pages
page_track=0         # page counter configuration
type_sort_db=0       # variable used in homepage to pick sort query
Game_identification_number=0
#-------------------------------------------------------------------------------


# #
# Load user 
# #
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

#**************************************************************************************
#***************************************************************************************
#    <<<<<<<<<<<<<<<<<<<<< #### Homepage HTML #### >>>>>>>>>>>>>>>>>>>>>>>>
#**************************************************************************************
#**************************************************************************************
@app.route('/')
def homepage():
   return redirect(url_for('home'))


@app.route('/home', methods=['GET', 'POST'])
def home():
   logger.info("Entered /home")
   global resetflag
   global resetflagcsv
   global offset
   global type_sort_db
   if request.method == 'POST':
      if request.form['sort'] == 'Popular':
         type_sort_db=0
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'A to Z':
         type_sort_db=1
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Z to A':
         type_sort_db=2
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Console':
         # type_sort_db=3
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'PC':
         type_sort_db=0
         return redirect(url_for('game_list'))


   ################################
   dbreinit(logger,mysql.connection,resetflag)
   parse_steam_game_csv(mysql.connection, resetflagcsv)
   ################################
   offset=0
   resetflag=0
   page_track=1
   resetflagcsv=0

   return render_template('home.html')
   

#***************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Login HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#**************************************************************************************
@app.route('/login', methods=['GET', 'POST'])
def login():
   error = None
   if request.method == "POST": 
      print(request.form.get('username'))
   
      if request.form.get('username'):
         mem_username=request.form.get('username')
         mem_password= request.form.get('password')
         print("this is the mem_password from form: ",end='')
         print(mem_password)
         try:
            print('searching db for '+mem_username)
            data= read_query(mysql.connection,"SELECT mem_password FROM Members WHERE mem_username='{}';".format(mem_username))
            truncated=data[0][0]
            print(truncated)
            unhexlifypw= binascii.unhexlify(truncated)
            print(truncated)
            verify(truncated,mem_password)
            logger.info("Login verification by %s",mem_username)
            session['mem_username'] = mem_username
            return redirect(url_for('profile'))

         except:
            logger.debug("Login failed by %s",mem_username)
            return render_template("login.html")
      #check for admin
      # elif (request.form.get('username') != 'admin') or request.form.get('password') != 'admin':
      #    error = 'Invalid Credentials'
      else:
         # session['logged_in'] = True
         flash("You're logged in!")
         return render_template("profile.html")
   else:
      return render_template("login.html", error= error)



#***************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Admin Login HTML (NOT DONE) ]]]]]]]]]]]]]]]]]]]]]]]]]
#**************************************************************************************
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
   error = None
   if request.method == "POST": 
      print(request.form.get('username'))
   
      if request.form.get('username'):
         mem_username=request.form.get('username')
         # session["mem_username"] = username
         mem_password= request.form.get('password')
         print("this is the mem_password from form: ",end='')
         print(mem_password)
         try:
            print('searching db for '+mem_username)
            data= read_query(mysql.connection,"SELECT mem_password FROM Members WHERE mem_username='{}';".format(mem_username))
            truncated=data[0][0]
            print(truncated)
            unhexlifypw= binascii.unhexlify(truncated)
            print(truncated)
            verify(truncated,mem_password)
            print('Success!')
            return render_template('profile.html')
         except:
            logger.debug("Login failed by %s",mem_username)
            return render_template("login.html")
      #check for admin
      # elif (request.form.get('username') != 'admin') or request.form.get('password') != 'admin':
      #    error = 'Invalid Credentials'
      else:
         # session['logged_in'] = True
         flash("You're logged in!")
         return render_template("profile.html")
   else:
      return render_template("login.html", error= error)



#***************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Logout HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#**************************************************************************************
@app.route('/logout')
def logout():
   # session.pop("user", None)
   # logout_user()
   session.clear()
   flash("You have been logged out!", "info")
   return redirect(url_for('home'))



#***************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ sign up HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#**************************************************************************************
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
      encryptedpw=encryptpw(mem_password)
      try:
         print('Adding to database password: '+mem_password)
         print('As :', end='')
         print(encryptedpw)
         addmembers(mysql.connection,unique_id,mem_username,mem_email,encryptedpw)
         #authenticate/create session here?

         flash("Thanks for registering!")
         session['logged_in'] = True
         
         return render_template('home.html')
      except Exception as e:
         return (str(e))
   return render_template('signup.html')



#***************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ request page HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#**************************************************************************************
@app.route('/request_page', methods=['GET', 'POST'])
def request_page():
   if "mem_username" in session:
      mem_username = session['mem_username']
      return render_template('request_page.html', mem_username=mem_username)
   else:
      return render_template('login.html')


#***************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Game page HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#**************************************************************************************
@app.route('/game_page', methods=['GET', 'POST'])
def game_page():
   global Game_identification_number
   game_i=[]
   game_info=game_information(mysql.connection, Game_identification_number)   
   game_i.append(get_url_from_cvs(Game_identification_number))
   return render_template('game_page.html', game_page=game_info, game_image=game_i)



#***************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Game List HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#**************************************************************************************
@app.route('/game_list', methods=['GET', 'POST'])
def game_list(page=1):
   global offset
   global page_track
   global type_sort_db
   global Game_identification_number
   per_page = 30

   # when front or back button pressed, activates POST
   # we use value and type thru here
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
         Game_identification_number=request.form.get('submit_button')
         return redirect(url_for('game_page'))
      
   if type_sort_db == 0: #POPULAR   
      VideoGames=sortbypopularity(mysql.connection, offset*30, per_page) # offset*10
   elif type_sort_db == 1: # A to Z (ASCE)
      VideoGames=sortbyalphabetical(mysql.connection, offset*30, per_page)
   elif type_sort_db == 2: # Z to A (DESC)
      VideoGames=sordbyalphabeticaldesc(mysql.connection, offset*30, per_page)
   elif type_sort_db == 3: # CONSOLE   
      VideoGames=sortbyplatform(mysql.connection,platform)
   elif type_sort_db == 4: # PC
      VideoGames=sortbyplatform(mysql.connection,'windows')
   elif type_sort_db == 5: # MOBILE
      VideoGames=sortbyplatform(mysql.connection,platform)
   elif type_sort_db == 6: # HANDHELD
      VideoGames=sortbyplatform(mysql.connection,platform)
   elif type_sort_db == 7: # ARCADE
      VideoGames=sortbyplatform(mysql.connection,platform)


   #### Fetching the data from query ####
   VideoGames=[i[0] for i in VideoGames] #removes () and , from each name
   
   # keep track of the pages t cap at min and max
   page_track = math.ceil(len(VideoGames)) 

   image_url = []
   gameID = []

   for games_na in VideoGames:
      games_num=game_ids_with_name(mysql.connection, games_na)
      gameID.append(str(games_num))
      print(games_na+':'+str(games_num))
   print('...')
   gameID=[x[2:-3] for x in gameID]
 
   for search in gameID:
      image_url.append(get_url_from_cvs(search))
      print(search)
     
   #pagination assists in orgaizing pages and contents per page
   pagination = Pagination(page=page, per_page=per_page, format_number=True, 
                           total=len(VideoGames), record_name='Video Games') 

   return render_template('game_list.html', games_list = zip(VideoGames, image_url, gameID), pagination=pagination)


#***************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Profile HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#**************************************************************************************
@app.route('/profile', methods=['GET', 'POST'])
def profile():
   if "mem_username" in session:
      mem_username = session['mem_username']
      return render_template('profile.html', mem_username=mem_username)
   else: 
      return render_template('login.html')   

## Basic Stuff ##
if __name__ == '__main__':
   app.run(debug=True)
