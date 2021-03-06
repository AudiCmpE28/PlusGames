# SJSU CMPE 138 Spring 2021 TEAM1
# $env:FLASK_APP = "init.py"    
# $env:FLASK_ENV = "development"
# python -m flask run    
import logging
logger = logging.getLogger('AppLog')
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
import random
from flask import (Flask, g, redirect, render_template, request, session, url_for, Blueprint, escape, flash)
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
### DO NOT TOUCH THESE          
offset=0                      
page_track=0         
type_sort_db=0       
Game_identification_number=0
admin_check=''
### DO NOT TOUCH THESE
semaphore=0
admin=0
requestbox=0
deleteWarn=0
selectName=''
usernameGlobal=''
### DO NOT TOUCH THESE
#-------------------------------------------------------------------------------


# # # # # # # # # #
# Load user Home #
# # # # # # # # #
@login_manager.user_loader
def load_user(user_id):
   logger.debug('At user_loader')
   return User.get(user_id)


#*************************************************************************************************
#**************************************************************************************************
#    <<<<<<<<<<<<<<<<<<<<< #### Homepage HTML #### >>>>>>>>>>>>>>>>>>>>>>>>
#*************************************************************************************************
#*************************************************************************************************
# reroute to homepage to load homepage data
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
   global Game_identification_number
   global requestbox
   global selectName
   global deleteWarn
   # addadmins(mysql.connection, 69420, 'simonAlta', 'danish_query@sjsu.edu', 'simonAlta108!')

   if request.method == 'POST':
      if request.form['sort'] == 'Popular':   ## Popular ##
         type_sort_db='Popular'
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'A to Z':     ## Alphabetical ##
         type_sort_db='A to Z'
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Z to A':
         type_sort_db='Z to A'
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Console':   ## Platform ##
         type_sort_db='Console'
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'PC':
         type_sort_db='PC'
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Action':    ## Genres ##
         type_sort_db='Action'
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Adventure':
         type_sort_db='Adventure'
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Strategy':
         type_sort_db='Strategy'
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'RPG':
         type_sort_db='RPG'
         return redirect(url_for('game_list'))         
      elif request.form['sort'] == 'Casual':
         type_sort_db='Casual'
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Indie':
         type_sort_db='Indie'
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Simulation':
         type_sort_db='Simulation'
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Violent':
         type_sort_db='Violent'
         return redirect(url_for('game_list')) 
      elif request.form['sort'] == 'Racing':
         type_sort_db='Racing'
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Sports':
         type_sort_db='Sports'
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Education':
         type_sort_db='Education'
         return redirect(url_for('game_list'))
      elif request.form['sort'] == 'Massively Multiplayer':
         type_sort_db='Massively Multiplayer'
         return redirect(url_for('game_list')) 
      else:
         Game_identification_number=request.form.get('sort')
         return redirect(url_for('game_page'))

   ################################
   dbreinit(logger,mysql.connection,resetflag)
   parse_steam_game_csv(logger,mysql.connection, resetflagcsv)
   ################################
   offset=0
   resetflag=0
   page_track=1
   resetflagcsv=0
   type_sort_db='CLR'
   requestbox=0
   deleteWarn=0
   selectName='Admin Select Menu'
   
   return render_template('home.html', loggedIn=semaphore)
   

#**************************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Admin || Member Login HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#*************************************************************************************************
@app.route('/login', methods=['GET', 'POST'])
def login():
   error = None
   global admin_check
   global semaphore
   global selectName
   selectName='Admin Select Menu'

   if request.method == "POST": 
   
      if request.form.get('username'):
         mem_username=request.form.get('username')
         mem_password= request.form.get('password')
         if semaphore == 0:
            admin_check='' #clears if needed
            admin_check = request.form.get('admin_or_mem') #if check box clicked its true

         try:
            if admin_check: #if slider was set to admin will enter first if
               data = admin_password_retrieve(mysql.connection, mem_username)
            else:
               data = member_password_retrieve(mysql.connection, mem_username)

            truncated=data[0][0]
            unhexlifypw= binascii.unhexlify(truncated)
            verify(truncated,mem_password)
            session['mem_username'] = mem_username
            return redirect(url_for('profile'))

         except:
            logger.debug("Login failed by %s",mem_username)
            return render_template("login.html")
      else:
         flash("You're logged in!")
         return render_template("profile.html")
   else:
      return render_template("login.html", error= error)






#**************************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Profile HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#*************************************************************************************************
@app.route('/profile', methods=['GET', 'POST'])
def profile():
   logger.debug('Entered /profile')
   global admin_check
   global semaphore
   global admin
   global requestbox
   global selectName
   global deleteWarn
   adminMSG=''
   gameID=''
   game_vertify=''
   game_ID=''
   company=''
   game_n=''
   genres=''
   rate=''
   date=''
   price=''
   platform=''
   updateButton=0
   mem_username = session['mem_username']
   requests_games=[]


   if request.method == "POST": 
      if request.form['request'] == 'New Game':
         selectName='Selection -> New Game'
         requestbox=1           
      elif request.form['request'] == 'Edit Game':
         selectName='Selection -> Edit Game'
         requestbox=2
      elif request.form['request'] == 'Remove Game': 
         selectName='Selection -> Edit Game' 
         requestbox=3
      elif request.form['request'] == 'Remove Members':
         selectName='Selection -> Member Removal'
         requestbox=4       
      elif request.form['request'] == 'Retreive ID':
         gameID=request.form.get('game_name_back')  
         gameID=retrieve_game_ID(mysql.connection, gameID)
         gameID=[i[0] for i in gameID]

      elif request.form['request'] == 'INSERT':  
         game_ID=gameID_generator(mysql.connection)
         company=request.form.get('company')
         game_n=request.form.get('game_name')
         genres=request.form.get('genre')
         rate=request.form.get('rating')
         date=request.form.get('date')
         price=request.form.get('price')
         platform=request.form.get('platform')

         addcompany(mysql.connection, company)
         addgame(mysql.connection,game_ID,company,game_n,genres,rate,date,price)
         addreleasedon(mysql.connection,game_ID,platform)
         addreleasedon(mysql.connection,game_ID,platform)
      
      elif request.form['request'] == 'EDIT':  
         gameID=request.form.get('game_id_edit') 
         game_vertify=does_game_ID_exist(mysql.connection, gameID)
         if game_vertify != gameID:
            game_n=request.form.get('game_name')
            company=request.form.get('company')
            genres=request.form.get('genre')
            rate=request.form.get('rating')
            date=request.form.get('date')
            price=request.form.get('price')
            platform=request.form.get('platform2')

            if game_n != '':
               updategame_name(mysql.connection,gameID, str(game_n))
            if company != '':
               updategame_company(mysql.connection,gameID, str(company))
            if genres != '':
               updategame_genre(mysql.connection,gameID, str(genres))
            if rate != '':
               updategame_rating(mysql.connection,gameID, rate)
            if date != '':
               updategame_date(mysql.connection,gameID, str(date))
            if price != '':   
               updategame_price(mysql.connection,gameID, price)
            if platform != '':
               updategame_releasedon(mysql.connection,gameID, str(platform))
         else:
            gameID='Invalid ID'   

      elif request.form['request'] == 'REMOVE USER':
         userID=request.form.get('game_id_user')
         removeuser(mysql.connection, int(userID))
      
      elif request.form['request'] == 'REMOVE GAME':
         gameID=request.form.get('game_id_3') 
         removegame(mysql.connection, gameID)


      elif request.form['request'] == 'Remove Account':
         deleteWarn=deleteWarn+1
         if deleteWarn == 2:
            userID=retrieve_member_ID(mysql.connection, mem_username)
            userID=[i[0] for i in userID] 
            removeuser(mysql.connection, userID[0])
            return redirect(url_for('logout'))
      
      elif request.form['request'] == 'Update Username':
         updateButton=1

      elif request.form['request'] == 'Update':
         username=request.form.get('newUsr')
         userID=retrieve_member_ID(mysql.connection, mem_username) 
         userID=[i[0] for i in userID]
         update_username(mysql.connection, userID[0], username)
         mem_username=username
         session['mem_username'] = mem_username

      else:
         game_id=request.form.get('request')
         removerequest(mysql.connection, game_id)

         
   if "mem_username" in session:
      if semaphore == 0:
         semaphore=1
         if admin_check:
            admin=1
         else:
            admin=0
      
      if admin == 1:
         status=1   
         requests_games.append(retrieve_member_requests(mysql.connection))
         return render_template('profile.html', mem_username=mem_username, status=status, 
                                 selection=requestbox, gameID=gameID, ss=selectName, messages=requests_games)
      else: 
         status=0
         return render_template('profile.html', mem_username=mem_username, status=status, warning=deleteWarn, updates=updateButton)
   else: 
      return render_template('login.html')  #no account or logged in



#**************************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Logout HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#*************************************************************************************************
@app.route('/logout')
def logout():
   logger.debug('Logging out...')
   global semaphore
   # session.pop("user", None)
   # logout_user()
   semaphore=0
   session.clear()
   flash("You have been logged out!", "info")
   return redirect(url_for('home'))




#**************************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ sign up HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#*************************************************************************************************
@app.route('/signup', methods=['GET','POST'])
def signup():
   global semaphore
   logger.debug('Entered /signup')
   if request.method=='POST':
      mem_username=request.form.get('username')
      mem_email= request.form.get('email')
      mem_password= request.form.get('password')
      unique_id=random.randint(1,100000)
      encryptedpw=encryptpw(mem_password)
      try:
         addmembers(mysql.connection,unique_id,mem_username,mem_email,encryptedpw)
         #authenticate/create session here?

         flash("Thanks for registering!")
         session['logged_in'] = True
         session['mem_username'] = mem_username
         return redirect(url_for('profile'))
      
      
      except Exception as e:
         return (str(e))
   return render_template('signup.html')





#**************************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ request page HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#*************************************************************************************************
@app.route('/request_page', methods=['GET', 'POST'])
def request_page():
   gameID=''
   mem_username = session['mem_username']

   if request.method == 'POST':
      if request.form['submit'] == 'Retrieve ID':
         gameID=request.form['game_name_back']
         gameID=retrieve_game_ID(mysql.connection, gameID)
         gameID=[i[0] for i in gameID]
         if gameID:
            gameID=gameID[0]
         else:
            gameID='INVALID GAME NAME'
         

      elif request.form['submit'] == 'Submit Form':
         request_comm=request.form["req_txt"]
         gameID=int(request.form['game_id'])
         gameID=gameID_generator(mysql.connection)
         request_change_game(mysql.connection, mem_username, gameID, request_comm)
         redirect(url_for('home'))
         # if gameID == 0:
         #    gameID=gameID_generator(mysql.connection)
         #    request_change_game(mysql.connection, mem_username, gameID, request_comm)
         #    redirect(url_for('home'))
         # else:
         #    game_vertify=does_game_ID_exist(mysql.connection, gameID)
         #    game_vertify=[x[0] for x in game_vertify]
         #    game_vertify=game_vertify[0]

         #    if game_vertify == gameID:
         #       gameID=gameID_generator(mysql.connection)
         #       does_game_ID_exist(mysql.connection, mem_username, gameID, request_comm)
         #       redirect(url_for('home'))


   if "mem_username" in session:
      mem_username = session['mem_username']
      return render_template('request_page.html', mem_username=mem_username, gameid=gameID)
   else:
      return render_template('login.html')





#**************************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Game page HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#*************************************************************************************************
@app.route('/game_page', methods=['GET', 'POST'])
def game_page():
   global semaphore
   global Game_identification_number
   global admin
   game_comments=[]
   comment=''

   if request.method == 'POST':
      if request.form['comments'] == 'Postit':
         comment=request.form['comment']

   if semaphore:  #if user is signed in
      mem_username = session['mem_username']
      if admin == 0:
         if comment:
            addcomment(mysql.connection, mem_username,int(Game_identification_number),comment)

   game_comments.append(getgamecomments(mysql.connection, Game_identification_number))


   game_i=[]
   game_info=game_information(mysql.connection, Game_identification_number)   
   game_i.append(get_url_from_csv(Game_identification_number))
   return render_template('game_page.html', game_page=game_info, game_image=game_i, comment=game_comments, status=semaphore)




#**************************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Game List HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#*************************************************************************************************
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
            logger.debug('Next page')
      elif request.form['submit_button'] == 'Back':
         if(offset > 0):
            offset-=1
            logger.debug('Prev page')
         else:
            offset=0
      else:
         Game_identification_number=request.form.get('submit_button')
         return redirect(url_for('game_page'))
         
   logger.debug('Sorting by: %s',type_sort_db)
   if type_sort_db == 'Popular': #POPULAR   
      VideoGames=sortbypopularity(mysql.connection, offset*30, per_page) # offset*10
   elif type_sort_db == 'A to Z': # A to Z (ASCE)
      VideoGames=sortbyalphabetical(mysql.connection, offset*30, per_page)
   elif type_sort_db == 'Z to A': # Z to A (DESC)
      VideoGames=sordbyalphabeticaldesc(mysql.connection, offset*30, per_page)
   elif type_sort_db == 'Console': # CONSOLE   
      VideoGames=sortbyplatform(mysql.connection,'console', offset*30, per_page) #placeholder
   elif type_sort_db == 'PC': # PC
      VideoGames=sortbyplatform(mysql.connection,'windows', offset*30, per_page) #placeholder

   elif type_sort_db == 'Action': # GENRES
      VideoGames=sortbygenre(mysql.connection, 'Action', offset*30, per_page)
   elif type_sort_db == 'Adventure': 
      VideoGames=sortbygenre(mysql.connection, 'Adventure', offset*30, per_page)
   elif type_sort_db == 'Strategy': 
      VideoGames=sortbygenre(mysql.connection, 'Strategy', offset*30, per_page)
   elif type_sort_db == 'RPG':
      VideoGames=sortbygenre(mysql.connection, 'RPG', offset*30, per_page)
   elif type_sort_db == 'Casual': 
      VideoGames=sortbygenre(mysql.connection, 'Casual', offset*30, per_page)
   elif type_sort_db == 'Indie': 
      VideoGames=sortbygenre(mysql.connection, 'Indie', offset*30, per_page)
   elif type_sort_db == 'Simulation': 
      VideoGames=sortbygenre(mysql.connection, 'Simulation', offset*30, per_page)
   elif type_sort_db == 'Violent':
      VideoGames=sortbygenre(mysql.connection, 'Violent', offset*30, per_page)
   elif type_sort_db == 'Racing': 
      VideoGames=sortbygenre(mysql.connection, 'Racing', offset*30, per_page)
   elif type_sort_db == 'Sports': 
      VideoGames=sortbygenre(mysql.connection, 'Sports', offset*30, per_page)
   elif type_sort_db == 'Education': 
      VideoGames=sortbygenre(mysql.connection, 'Education', offset*30, per_page)
   elif type_sort_db == 'Massively Multiplayer':
      VideoGames=sortbygenre(mysql.connection, 'Massively Multiplayer', offset*30, per_page)
#################################################################################################

   #### Fetching the data from query ####
   VideoGames=[i[0] for i in VideoGames] #removes () and , from each name
   
   # keep track of the pages t cap at min and max
   page_track = math.ceil(len(VideoGames)) 

   image_url = []
   gameID = []
   validID = []

   for games_na in VideoGames:
      games_num=game_ids_with_name(mysql.connection, games_na)
      gameID.append(str(games_num))
      
   gameID=[x[2:-3] for x in gameID]
 
   # cleans number ids from punctuation
   for num in gameID:
      num=num.replace(',', '')
      num=num.replace(')', '')
      num=num.replace('(', '')
      num=num.split(' ')
      for clean in num:
         if clean != '':
            validID.append(str(clean))

   for search in validID:
      image_url.append(get_url_from_csv(search))

     
   #pagination assists in orgaizing pages and contents per page
   pagination = Pagination(page=page, per_page=per_page, format_number=True, 
                           total=len(VideoGames), record_name='Video Games') 

   return render_template('game_list.html', games_list = zip(VideoGames, image_url, gameID), 
                           pagination=pagination, list_type=type_sort_db)



#***************************************************************************************
#    [[[[[[[[[[[[[[[[[[[[[[[[[ Python HTML ]]]]]]]]]]]]]]]]]]]]]]]]]
#**************************************************************************************



## Basic Stuff ##
if __name__ == '__main__':
   app.run(debug=True)
