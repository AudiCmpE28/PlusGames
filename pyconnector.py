import mysql.connector
from mysql.connector import Error
import pandas as pd

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
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
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query successful")
        connection.commit()
    except Error as err:
        print(f"Error: '{err}'")
        #Rollback changes due to errors
        connection.rollback()


#Pass in a connection and a string query, returns result
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

#Table specific connectors-queries
def addmembers(memid, memname, password):
    execute_query(connection,"insert into `Members` (`unique_id`, `mem_username`, `mem_password`) values (%(memid)d, %(memname)s, sha1(%(password)s));",{'memid':memid, 'memname':memname, 'password':password})