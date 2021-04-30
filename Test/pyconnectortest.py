# SJSU CMPE 138 Spring 2021 TEAM1
import mysql.connector
from mysql.connector import Error
import pandas as pd
import random, string

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
#for testing purposes, returns a string of size length
#use 
def randomstring(length):
    l = string.ascii_lowercase
    return ''.join(random.choice(l)for i in range(length))


#---------------------------------
#Table specific connectors-queries
#---------------------------------


# use {}, '{}' for any raw arguments and string arguments,respectively.
# then at the end of the string use .format(parameter, ...)
def addmembers(connection, memid, memname, password):
    user_query ="insert into `Users` (`unique_id`) values ({});".format(memid)
    member_query= "insert into `Members` (`unique_id`, `mem_username`, `mem_password`) values ({},'{}', sha1('{}'));".format(memid,memname,password)
    try: #This will fail the whole query and prevent a member being added to an already existing unique_id
        execute_query(connection,user_query)
        execute_query(connection,member_query)
    except:
        exit
