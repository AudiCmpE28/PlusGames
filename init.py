# $env:FLASK_APP = "init.py"    
# $env:FLASK_ENV = "development"
# python -m flask run    
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
                   url_for, Blueprint, escape)
from flask_mysql_connector import MySQL
from mysql.connector import Error
# from flask_login import (LoginManager, logout_user, logout_user, 
#                          login_required, current_user)

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


# login_manager =LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.init_app(app)

#------------------------------------------------------------------------------
global resetflag     #
resetflag=0          # Set to 1 if you want to reset the db
global resetflagcsv  # 
resetflagcsv=0       # Set to 1 if you want to reimport the csv to database
##########################################################################
offset=0             # for pages
page_track=1         # page counter configuration
type_sort_db=0       # variable used in homepage to pick sort query
#-------------------------------------------------------------------------------


#**************************************************************************************
#***************************************************************************************
#    <<<<<<<<<<<<<<<<<<<<< #### Homepage HTML #### >>>>>>>>>>>>>>>>>>>>>>>>
#**************************************************************************************
#**************************************************************************************
@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
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
         # type_sort_db=4
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Mobile':
         # type_sort_db=5
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Handheld':
         # type_sort_db=6
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Arcade':
         # type_sort_db=7
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
   if request.method == "POST": ##gets info from form
      mem_username=request.form.get('username')
      mem_password= request.form.get('password')
      getuser="SELECT * FROM Members WHERE mem_username='{}'".format(mem_username)
      try:
         database_cred=getlogin(mysql.connection, getuser)
         if mem_username != database_cred[1] or mem_password != decryptpw[3]:
            msg = 'Incorrect username or password'

         
      except:
         logger.info("Login failed by %s",mem_username)
   else:
      return render_template('login.html')


#***************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Logout HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#**************************************************************************************
@app.route('/logout', methods=['GET', 'POST'])
# @login_required
def logout():
   session.clear()
   #logout_user()
   return render_template('home.html')



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
      user_query ="insert into `Users` (`unique_id`) values ({});".format(unique_id)
      member_query= "insert into `Members` (`unique_id`, `mem_username`, `mem_email`, `mem_password`) values ({},'{}','{}', sha1('{}'));".format(unique_id,mem_username,mem_email,mem_password)
      try:
         addmembers(mysql.connection,unique_id,mem_username,mem_email,mem_password)
         return render_template('signup.html')
      except:
         return -1
   return render_template('signup.html')



#***************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ request page HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#**************************************************************************************
@app.route('/request_page', methods=['GET', 'POST'])
def request_page():
   return render_template('request_page.html')


#***************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Game page HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#**************************************************************************************
@app.route('/game_page', methods=['GET', 'POST'])
def game_page():
   return render_template('game_page.html')



#***************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Game List HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#**************************************************************************************
@app.route('/game_list', methods=['GET', 'POST'])
def game_list(page=1):
   global offset
   global page_track
   global type_sort_db
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

   #establish connection with MySQL
   # gamesL=mysql.connection.cursor() 
   #We already have one, mysql @ line 48
   
   if type_sort_db == 0: #POPULAR   
      VideoGames=sortbypopularity(mysql.connection, offset, per_page) # offset*10
   elif type_sort_db == 1: # A to Z (ASCE)
      VideoGames=sortbyalphabetical(mysql.connection, offset, per_page)
   elif type_sort_db == 2: # Z to A (DESC)
      VideoGames=sordbyalphabeticaldesc(mysql.connection, offset, per_page)

   elif type_sort_db == 3: # CONSOLE   
      VideoGames=sortbyplatform(mysql.connection,platform)
   elif type_sort_db == 4: # PC
      VideoGames=sortbyplatform(mysql.connection,platform)
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
      
   gameID=[x[2:-3] for x in gameID]

   for search in gameID:
      image_url.append(get_url_from_cvs(search))
     

   #pagination assists in orgaizing pages and contents per page
   pagination = Pagination(page=page, per_page=per_page, format_number=True, 
                           total=len(VideoGames), record_name='Video Games') 

   return render_template('game_list.html', games_list = VideoGames, images_g = image_url, gameId=gameID, pagination=pagination)



# /** get url to display**/
def get_url_from_cvs(game_id):
    with open('static/csv/game_id_image.csv', encoding="utf8") as csv_file:
        csvfile=csv.reader(csv_file,delimiter=',') 
        for row in csvfile:
            if str(game_id)==row[0]:
                return row[1]  


#***************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Profile HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#**************************************************************************************
@app.route('/profile', methods=['GET', 'POST'])
# @login_required
def profile():
   return render_template('profile.html')


## Nasic Stuff ##
if __name__ == '__main__':
   app.run(debug=True)
