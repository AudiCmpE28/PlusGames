# SJSU CMPE 138 Spring 2021 TEAM1

import mysql.connector
from mysql.connector import Error
import pandas as pd
import random, string
from IPython.display import display
import logging
import csv
import MySQLdb

logger = logging.getLogger('TLog')
logger.setLevel(logging.DEBUG)
logger.debug('Logger config message')
fhandler = logging.FileHandler(filename='logfile2.log', mode='a')
fhandler.setLevel(logging.DEBUG)
hformatter=logging.Formatter('%(asctime)s %(name)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fhandler.setFormatter(hformatter)
logger.addHandler(fhandler)
from cryptography.fernet import Fernet

def encryptpw(password:str):
   f = Fernet("yMCknhRM5NJiN5flBsigJEavBdeVXal4UI08P7qfngc=")
   password=password.encode("utf-8")
   token = f.encrypt(password)
   print(token)
   return token

def decryptpw(encrypted_password):
   f = Fernet("yMCknhRM5NJiN5flBsigJEavBdeVXal4UI08P7qfngc=")
   decrypted=f.decrypt(encrypted_password)
   print(decrypted.decode("utf-8"))
   return decrypted.decode("utf-8")

kms="kms"
en=encryptpw(kms)
decryptpw(en)

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
        logger.debug('Db connection err')
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
        logger.debug('Commit: '+query)

    except Error as err:
        print(f"Error: '{err}'")
        #Rollback changes due to errors
        connection.rollback()
        cursor.close()
        logger.debug('Rollback: '+query)
        raise err


#Pass in a connection and a string query, returns result
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        logger.debug('Fetching: '+query)
        return result
    except Error as err:
        print(f"Error: '{err}'")
        cursor.close()
        logger.debug('Badfetch: '+query)

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
        raise err
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



def sortbygenre(connection,genre):
    gamegenre = "SELECT * FROM Game ORDER BY '{}';".format(genre)
    return returncolumns(connection,gamegenre)


def sortbypopularity_rating(connection, offset, per_page):
    gamequery="SELECT rating FROM Game ORDER BY rating DESC LIMIT {}, {};".format((offset*10), per_page) 
    return read_query(connection,gamequery)

def sortbypopularity(connection, offset, per_page):
    gamequery="SELECT game_n FROM Game ORDER BY rating DESC LIMIT {}, {};".format((offset*10), per_page) 
    return read_query(connection,gamequery)
    

def sortbyalphabetical(connection, offset, per_page):
	gamealpha = "SELECT game_n FROM Game ORDER BY game_n ASC LIMIT {}, {};".format((offset*10), per_page) 
	return read_query(connection,gamealpha)
	
	
def sordbyalphabeticaldesc(connection, offset, per_page):
	gamealphadesc = "SELECT game_n FROM Game ORDER BY game_n DESC LIMIT {}, {};".format((offset*10), per_page)
	return read_query(connection,gamealphadesc)

def sortbyplatform(connection,platform):
    chooseplatform = "SELECT * FROM Game join Released_on WHERE Game.game_id = Released_on.game_id and platform_name= '{}';".format(platform)
    return read_query(connection,chooseplatform)

# /** get url to display**/
def get_url_from_cvs(game_id):
    with open('static/csv/game_id_image.csv', encoding="utf8") as csv_file:
        csvfile=csv.reader(csv_file,delimiter=',') 
        for row in csvfile:
            if str(game_id)==row[0]:
                return row[1]  



def game_ids_with_name(connection, games_name):
	gamealpha = "SELECT game_id FROM Game WHERE Game.game_n = '{}';".format(games_name) 
	return read_query(connection,gamealpha)


def addcomment(connection, mem_username,game_id,text):
    insertq="insert into comment_on (mem_username, game_id,c_date,c_time,comment_text) values ('{}', {},NOW(),NOW(), '{}');".format(mem_username,game_id,text)
    execute_query(connection, insertq)

def addreview(connection, mem_username,game_id,text):
    insertq="insert into comment_on (mem_username, game_id,c_date,c_time,comment_text) values ('{}', {},NOW(),NOW(), '{}');".format(mem_username,game_id,text)
    execute_query(connection, insertq)

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
def parse_steam_game_csv(connection,reset):
    if reset==0:
        logger.info("CSV to db deferred")
        return 0
    with open('static/csv/steam_game.csv',encoding="utf8")as csv_file:
        csvfile = csv.reader(csv_file,delimiter =',')
        #store all the values in dynamic array
        #use loop to iterate through csvfile
        for row in csvfile:
            #inserting each row into value
            addcompany(connection,row[2])
            addplatform(connection,row[1])
            addgame(connection, row[0],row[2],row[3],row[4], row[5],row[6],row[7])
            addreleasedon(connection,row[0],row[1])
########################################################################

def getgamecomments(connection, game_id):
    game_comments = "select mem_username, c_date, c_time, comment_text from comment_on join Game on comment_on.game_id = Game.game_id where game_id={} order by c_time desc".format(game_id)
    return returncolumns(connection,game_comments)

def addbookmark(connection, mem_username, game_id):
        insertq="insert into bookmarked (mem_username, game_id) values ('{}', {});".format(mem_username, game_id)
        execute_query(connection, insertq)

# import pandas as pd
# df1 = pd.read_csv('static/csv/steam_game.csv',  delimiter=',')
# df2 = pd.read_csv('static/csv/game_id_image.csv', delimiter=',')

# with open('filtered.csv', 'w',encoding="utf8") as output:
#     pd.merge(df1, df2, on='game_id').to_csv(output, sep=',', index=False)
