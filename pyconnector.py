# SJSU CMPE 138 Spring 2021 TEAM1

import mysql.connector
from mysql.connector import Error
import pandas as pd
import random, string
from IPython.display import display
import logging
import csv
import MySQLdb
import os
logger2 = logging.getLogger('TLog')
logger2.setLevel(logging.DEBUG)
logger2.debug('logger2 config message')
fhandler = logging.FileHandler(filename='logfile2.log', mode='a', encoding='utf-8')
fhandler.setLevel(logging.DEBUG)
hformatter=logging.Formatter('%(asctime)s %(name)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fhandler.setFormatter(hformatter)
logger2.addHandler(fhandler)
import hashlib
import binascii

def encryptpw(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512',password.encode('utf-8'),salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    print("in encryptpw function encrypting ")
    print(password)
    print("as")
    print(pwdhash)
    return (salt + pwdhash).decode('ascii') #This is what you store in db

def verify(encrypted,password):
    password=password
    salt = encrypted[:64]
    encrypted = encrypted[64:]
    #print("in verify function encrypted pass got was ",end='')
    print(encrypted)
    #print("in verify function encr "+password+" as: ",end='')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),salt.encode('ascii'),100000)
    #print(pwdhash)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    #print('hexlified in verify is: '+pwdhash)
    if pwdhash == encrypted:
        return 1
    else:
        return 0


#-----------------
#Building blocks
#-----------------
#Connect to the database, necessary object for every query
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        #connect to the database
        connection = mysql.connector.connect(
            host=host_name, #use double quotes for all fields
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        connection.autocommit=False
        #autocommit disabled so we can rollback changes
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
        logger2.debug('Db connection err')
    return connection

# #csv file parser
# def parse_through_csv(connection):
#     with open('static/csv/steam_game.csv')as csv_file_game:
#         csvfile = csv.reader(csv_file_game,delimiter =',')
#         #store all the values in dynamic array
#         all_value = []
#         #use loop to iterate through csvfile
#         for row in csvfile:
#             #inserting each row into value
#             value = (row[0],row[1],row[2],row[3],row[4],row[5],row[6])
#             all_value.append(value)
#     mycursor = connection.cursor()
#     mycursor.executemany(query,all_value)
#     connection.commit()

def geturlfromcsv(game_id):
    file=csv.reader('static/csv/game_id_image.csv','r',encoding="utf8") 
    for row in file:
        if game_id==row[0]:
            return row[1]


# use triple quotes if using multiline strings (i.e queries w/linebreaks)
#Pass in connection and string query, commits or rollbacks changes depending on errors
def execute_query(connection, query):

    #instance of connection
    #cursor is an abstraction meant for
    #data set traversal.
    cursor = connection.cursor()
    
    try:
        cursor.execute(query)
        #print("Query successful")
        connection.commit()
        cursor.close()
        logger2.debug('Commit: '+query)

    except Error as err:
        print(f"Error: '{err}'")
        #Rollback changes due to errors
        connection.rollback()
        cursor.close()
        logger2.debug('Rollback: '+query)
        raise err


#Pass in a connection and a string query, returns result
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        logger2.debug('Fetching: '+query)
        return result
    except Error as err:
        print(f"Error: '{err}'")
        cursor.close()
        logger2.debug('Badfetch: '+query)


#for testing purposes, returns a string of size length 
def randomstring(length):
    l = string.ascii_lowercase
    return ''.join(random.choice(l)for i in range(length))





# use {}, '{}' for any raw arguments and string arguments,respectively.
# then at the end of the string use .format(parameter, ...)
def addmembers(connection, unique_id, mem_username, mem_email,mem_password):
    if(unique_id==0):
        unique_id=random.randint(6,999999)
    if mem_email == "" or mem_username =="" or mem_password == "":
        raise 'invalid'
    user_query ="insert into `Users` (`unique_id`) values ({});".format(unique_id)
    member_query= "insert into `Members` (`unique_id`, `mem_username`, `mem_email`, `mem_password`) values ({},'{}','{}','{}');".format(unique_id,mem_username,mem_email,mem_password)
    try: #This will fail the whole query and prevent a member being added to an already existing unique_id. Even though execute_query has a try/except, we need another try here to make sure we stop if the 1st exec fails
        execute_query(connection,user_query)
        execute_query(connection,member_query)
    except:
        exit

def getlogin(connection, mem_username):
    getuser="SELECT * FROM Members WHERE mem_username='{}'".format(mem_username)
    try:
        return read_query(connection,getuser)
    except:
        exit

def addadmins(connection, unique_id, admin_username, admin_email, admin_password): 
    user_query ="insert into `Users` (`unique_id`) values ({});".format(unique_id)
    adm_query="INSERT INTO administrator (unique_id, admin_username, admin_email, admin_password) VALUES({},'{}','{}','{}');".format(unique_id,admin_username,admin_email,admin_password)
    if(unique_id >6):
        logger2.info("Too many admins or UID taken")
        exit
    try:
        execute_query(connection,user_query)
        execute_query(connection,adm_query)
    except:
        exit

def addguest(connection,unique_id):
    user_query ="insert into `Users` (`unique_id`) values ({});".format(unique_id)
    try:
        execute_query(connection,unique_id)
    except:
        exit


#add add game, comment, add review, company, console etc.
#LOOK AT THE WEBSITE
#Anything that a person clicks on the website, think what should be returned to webpage. Write functions that the front end can use to format and display it.

def returncolumns(connection,query):#basically read_query but returns a 2darray/column
    qresult=read_query(connection,query)
    resultlist1 = []
    for result in qresult:
        result = list(result)
        resultlist1.append(result)
    return resultlist1

def displaytable(columns,twoDarray): #columns = ["unique_id", "mem_username", "mem_password"]
    df = pd.DataFrame(twoDarray, columns=columns)
    display(df)



def sortbygenre(connection, genre, offset, per_page):
    gamegenre = "SELECT game_n FROM Game WHERE Game.genre = '{}' ORDER BY genre LIMIT {}, {};".format(genre, offset, per_page)
    return read_query(connection,gamegenre)


def sortbypopularity_rating(connection, offset, per_page):
    gamequery="SELECT rating FROM Game ORDER BY rating DESC LIMIT {}, {};".format(offset, per_page) 
    return read_query(connection,gamequery)

def sortbypopularity(connection, offset, per_page):
    gamequery="SELECT game_n FROM Game ORDER BY rating DESC LIMIT {}, {};".format(offset, per_page) 
    return read_query(connection,gamequery)
    

def sortbyalphabetical(connection, offset, per_page):
	gamealpha = "SELECT game_n FROM Game ORDER BY game_n ASC LIMIT {}, {};".format(offset, per_page) 
	return read_query(connection,gamealpha)
	
	
def sordbyalphabeticaldesc(connection, offset, per_page):
	gamealphadesc = "SELECT game_n FROM Game ORDER BY game_n DESC LIMIT {}, {};".format(offset, per_page)
	return read_query(connection,gamealphadesc)

def sortbyplatform(connection, platform, offset, per_page):
    chooseplatform = "SELECT game_n FROM Game, Released_on WHERE Game.game_id = Released_on.game_id AND platform_name= '{}' ORDER BY platform_name LIMIT {}, {};".format(platform, offset, per_page)
    return read_query(connection,chooseplatform)

# /** get url to display**/
def get_url_from_csv(game_id):
    with open('static/csv/game_id_image.csv', encoding="utf8") as csv_file:
        csvfile=csv.reader(csv_file,delimiter=',') 
        for row in csvfile:
            if str(game_id)==row[0]:
                return row[1] 
        return '/static/images/game_page/default.jpg'


def game_ids_with_name(connection, games_name):
	gamealpha = "SELECT game_id FROM Game WHERE Game.game_n = '{}';".format(games_name) 
	return read_query(connection,gamealpha)

def game_information(connection, game_ID):
	gamealpha = "SELECT * FROM Game WHERE Game.game_id = {};".format(game_ID) 
	return read_query(connection,gamealpha)

def addcomment(connection, mem_username,game_id,text):
    insertq="INSERT IGNORE into comment_on (mem_username, game_id,c_date,c_time,comment_text) values ('{}', {},NOW(),NOW(), '{}');".format(mem_username,game_id,text)
    execute_query(connection, insertq)

def addreview(connection, mem_username,game_id,text):
    insertq="insert into review_on (mem_username, game_id,rv_date,rv_time,review_text) values ('{}', {},NOW(),NOW(), '{}');".format(mem_username,game_id,text)
    execute_query(connection, insertq)

def retrievereviews(connection,game_id):
    getreviews="SELECT * FROM review_on WHERE Game.game_id={};".format(game_id)
    execute_query(connection,getreviews)

def request_change_game(connection,mem_username,game_id,req_text):
    #if request is for existing game, else create a new game entry
    if read_query("SELECT game_id FROM game where game.game_id = {}".format(game_id)):
        req_text=req_text.replace('',r'\'')
        req_text=req_text.replace('--',r'/')
        execute_query("Insert into request_game (mem_username, game_id, req_text) values ('{}',{},'{}');".format(mem_username,game_id,req_text))
    else:
        q="insert into game (game_id) values ({});".format(game_id)
        req_text=req_text.replace('',r'\'')
        req_text=req_text.replace('--',r'/')
        execute_query("Insert into request_game (mem_username, game_id, req_text) values ('{}',{},'{}');".format(mem_username,game_id,req_text))




###############
#UPDATE FUNCTIONAS for ADMIN
#########
def does_game_ID_exist(connection, gameID):
    query_ID="SELECT game_id FROM Game WHERE Game.game_id = {};".format(gameID)
    return read_query(connection, query_ID)
    
def gameID_generator(connection):
    game_vertify=0
    game_ID=0
    while game_ID == game_vertify:
        game_ID=random.randint(0,999999)
        game_vertify=does_game_ID_exist(connection, game_ID)
    return game_ID

def retrieve_game_ID(connection, game_name):
    query_ID="SELECT game_id FROM Game WHERE Game.game_n = '{}';".format(game_name)
    return read_query(connection, query_ID)


 


#removal queries/admin funcs

def retrieve_member_requests(connection):
    get="Select game_id, mem_username, req_text FROM request_game;"
    read_query(connection, get)

def removerequest(connection, game_id):
    rem="Delete from reqest_game r where r.game_id={}".format(game_id)
    execute_query(connection,rem)

def removecomment(connection,mem_username,game_id,rv_date,rv_time,review_text):
    query="DELETE FROM `review_on` WHERE mem_username='{}' AND game_id={} AND rv_date='{}', rv_time='{}', review_text='{}';".format(mem_username,game_id,rv_date,rv_time,review_text)
    execute_query(connection,query)

def removegame(connection,game_id):
    query="DELETE FROM Game WHERE game_id ={};".format(game_id)
    execute_query(connection,query)

def removeuser(connection,unique_id):
    query="DELETE from `users` WHERE unique_id ={};".format(unique_id)
    execute_query(connection,query)



######################## Company, Game, Platform, Released on ##########

def addcompany(connection, company):
    companyq="Insert IGNORE company values ('{}')".format(company)
    execute_query(connection,companyq)

def addgame(connection,game_id,g_company,game_n,genre,rating,release_Date,price):
    gameq = "INSERT IGNORE INTO Game (game_id,g_company,game_n,genre,rating,release_Date,price) values ({},'{}','{}','{}',{},'{}',{});".format(game_id,g_company,game_n,genre,rating,release_Date,price)
    execute_query(connection, gameq)

def addplatform(connection,platform):
    gamep= "Insert IGNORE into platform (platform_name) values('{}');".format(platform)
    execute_query(connection, gamep)

def addreleasedon(connection,game_id,platform):
    gameidq = "insert IGNORE into released_on (game_id,platform_name) values ({},'{}');".format(game_id,platform)
    execute_query(connection,gameidq)

#csv file parser
def parse_steam_game_csv(logger,connection,reset):
    if reset==0:
        logger.debug("CSV to db deferred")
        return 0
    logger.debug('Importing CSV to db...')
    with open('static/csv/steam_game.csv',encoding="utf-8")as csv_file:
        csvfile = csv.reader(csv_file,delimiter =',')
        #store all the values in dynamic array
        #use loop to iterate through csvfile
        for row in csvfile:
            #inserting each row into value
            addcompany(connection,row[2])
            addplatform(connection,row[1])
            addgame(connection, row[0],row[2],row[3],row[4], row[5],row[6],row[7])
            addreleasedon(connection,row[0],row[1])
    logger.debug('...Importing Complete')
########################################################################

def getgamecomments(connection, game_id):
    # game_comments = "SELECT mem_username, c_date, c_time, comment_text FROM comment_on JOIN Game ON comment_on.game_id = Game.game_id WHERE game_id={} ORDER BY c_time DESC".format(game_id)
    game_comments = "SELECT mem_username, c_date, c_time, comment_text FROM comment_on WHERE comment_on.game_id={} ORDER BY c_time DESC".format(game_id)
    return read_query(connection,game_comments)

def addbookmark(connection, mem_username, game_id):
        insertq="insert into bookmarked (mem_username, game_id) values ('{}', {});".format(mem_username, game_id)
        execute_query(connection, insertq)

# import pandas as pd
# df1 = pd.read_csv('static/csv/steam_game.csv',  delimiter=',')
# df2 = pd.read_csv('static/csv/game_id_image.csv', delimiter=',')

# with open('filtered.csv', 'w',encoding="utf8") as output:
#     pd.merge(df1, df2, on='game_id').to_csv(output, sep=',', index=False)


########################################################################
# functions for password admin/member
########################################################################
def member_password_retrieve(connection, member_username):
	mem_passw = "SELECT mem_password FROM Members WHERE mem_username='{}';".format(member_username)
	return read_query(connection, mem_passw)

def admin_password_retrieve(connection, admin_username):
	admin_passw = "SELECT admin_password FROM Administrator WHERE admin_username='{}';".format(admin_username)
	return read_query(connection, admin_passw)   



########################################################################
# functions for UPDATE
########################################################################
def updategame_name(connection,game_id, game_n):
    q="UPDATE game set game_n=('{}') where game_id=({});".format(game_n,game_id)
    execute_query(connection,q)

def updategame_company(connection,game_id, g_company):
    addcompany(connection,g_company)
    q="UPDATE game set g_company=('{}') where game_id=({});".format(g_company,game_id)
    execute_query(connection,q)


def updategame_genre(connection,game_id, genre):
    q="UPDATE game set genre=('{}') where game_id=({});".format(genre,game_id)
    execute_query(connection,q)
    
def updategame_rating(connection,game_id, rating):
    q="UPDATE game set rating=({}) where game_id=({});".format(rating,game_id)
    execute_query(connection,q)        

def updategame_date(connection,game_id, release_Date):
    q="UPDATE game set release_Date=('{}') where game_id=({});".format(release_Date,game_id)
    execute_query(connection,q)
    
def updategame_price(connection,game_id, price):
    q="UPDATE game set price=({}) where game_id=({});".format(price,game_id)
    execute_query(connection,q)      

def updategame_releasedon(connection,game_id,platform):
    addplatform(connection, platform)
    addreleasedon(connection,game_id,platform)
    q="UPDATE IGNORE released_on SET platform_name=('{}') WHERE game_id=({});".format(platform,game_id)
    execute_query(connection,q) 



########################################################################
# functions for Member Profile
########################################################################
def update_username(connection,ID, username):
    q="UPDATE members set mem_username=('{}') where unique_id=({});".format(username,ID)
    execute_query(connection,q)
    
def retrieve_member_ID(connection, member_name):
    query_ID="SELECT unique_id FROM members WHERE mem_username=('{}');".format(member_name)
    return read_query(connection, query_ID)