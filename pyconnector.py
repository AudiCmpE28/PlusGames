import mysql.connector
from mysql.connector import Error
import pandas as pd
import random, string
from flask import Flask, request,render_template
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
    return connection

# use triple quotes if using multiline strings (i.e queries w/linebreaks)
#Pass in connection and string query, commits or rollbacks changes depending on errors
def execute_query(connection, query):

    #instance of connection
    cursor = connection.cursor()
    
    try:
        cursor.execute(query)
        print("Query successful")
        connection.commit()
        cursor.close()
    except Error as err:
        print(f"Error: '{err}'")
        #Rollback changes due to errors
        connection.rollback()
        cursor.close()
        raise err


#Pass in a connection and a string query, returns result
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Error as err:
        print(f"Error: '{err}'")
        cursor.close()
        raise err


#for testing purposes, returns a string of size length 
def randomstring(length):
    l = string.ascii_lowercase
    return ''.join(random.choice(l)for i in range(length))


#---------------------------------
#connector funcs
#---------------------------------


# use {}, '{}' for any raw arguments and string arguments,respectively.
# then at the end of the string use .format(parameter, ...)
def addmembers(connection, unique_id, mem_username, mem_email,mem_password):
    user_query ="insert into `Users` (`unique_id`) values ({});".format(unique_id)
    member_query= "insert into `Members` (`unique_id`, `mem_username`, `mem_email`, `mem_password`) values ({},'{}','{}', sha1('{}'));".format(unique_id,mem_username,mem_email,mem_password)
    try: #This will fail the whole query and prevent a member being added to an already existing unique_id. Even though execute_query has a try/except, we need another try here to make sure we stop if the 1st exec fails
        execute_query(connection,user_query)
        execute_query(connection,member_query)
    except:
        exit

def addadmins(connection, unique_id, admin_username, admin_email, admin_password):
    user_query ="insert into `Users` (`unique_id`) values ({});".format(unique_id)
    adm_query="INSERT INTO administrator (unique_id, admin_username, admin_email, admin_password) VALUES({},'{}','{}',sha1('{}'));".format(unique_id,admin_username,admin_email,admin_password)
    try:
        execute_query(connection,user_query)
        execute_query(connection,adm_query)
    except:
        exit

def addguest(connection,unique_id):
    user_query ="insert into `Users` (`unique_id`) values ({});".format(unique_id)


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
gamegenre = "SELECT * FROM game ORDER BY genre;"
 print(returncolumns(connection,gamegenre))
    return
    
def sortbypopularity(connection):
    gamequery="select * from Game order by rating desc;" #uncertain, game not implemented yet so...
    print(returncolumns(connection,gamequery))
    return

def sortbyalphabetical(connection):

	gamealpha = "SELECT game_n FROM game ORDER BY game_n ASC;"
	print(returncolumns(connection,gamealpha))
	return
	
	
def sordbyalphabeticaldesc(connection):
	gamealphadesc = "SELECT game_n FROM game ORDER BY game_n DESC;"
	print(returncolumns(connection,gamealphadesc))
	return

def addcomment(connection, mem_username,game_id,text):
    insertq="insert into comment_on (mem_username, game_id,c_date,c_time,comment_text) values ('{}', {},NOW(),NOW(), '{}');".format(mem_username,game_id,text)
    execute_query(connection, insertq)

def addreview(connection, mem_username,game_id,text):
    insertq="insert into comment_on (mem_username, game_id,c_date,c_time,comment_text) values ('{}', {},NOW(),NOW(), '{}');".format(mem_username,game_id,text)
    execute_query(connection, insertq)

