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
