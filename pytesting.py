import mysql.connector
from mysql.connector import Error
import pandas as pd
import random
import string
from IPython.display import display
from pyconnector import *

#put in the actual database credentials you have on your end. 
connection = create_db_connection("localhost","root","1234","+games")


companyinsert = """
INSERT Company VALUES
('Microsoft'),('Bethesda'),('Arkane'),('Epic'),('Steam'),('Frontier'),('Ubisoft'),('Mojang');
"""

execute_query(connection, companyinsert)
#-----------------------------------------------------
#Retrieving data and tabulating it in python
#-----------------------------------------------------

selectquery = """
select * from company;
"""
qresult = read_query(connection, selectquery)
for result in qresult:
    print(result)

print('\nLets put all that data into a row(array) instead')

resultlist1 = []
for result in qresult:
    result=result
    resultlist1.append(result)
    print(result)

print('\nLets put all that data into a column(2Darray) instead')

resultlist2 = []
for result in qresult:
    result=list(result)
    resultlist2.append(result)
    print(result)

#now we can use those columns and display a table in python
#lets populate the tables first

#-------------------------------------------------------------
# Safe Parameterized SQLquery method 
#aquery = "SELECT count(*) FROM '{}' ;".format(table_name)
#execute_query(connection, aquery) #etc
#https://realpython.com/prevent-python-sql-injection/
#-------------------------------------------------------------

userquery = """insert into `Users` (`unique_id`) values (0);"""
for x in range(0, 10):
    execute_query(connection,userquery)

#suppose these are inputs from the html
for i in range(0,5):
    username= randomstring(16)
    password= randomstring(25)
    uniqueid= random.randint(1,100000)
    print('\nUnique_id:'+str(uniqueid),'\nUsername:'+username,'\nPassword:'+password)    
    addmembers(connection, uniqueid,username,password)


#Tabulate the query results!
mem_db = []
member_read = read_query(connection, "select Members.unique_id, Members.mem_username, Members.mem_password from Members;")
for result in member_read:
    result = list(result)
    mem_db.append(result)

columns = ["unique_id", "mem_username", "mem_password"]
df = pd.DataFrame(mem_db, columns=columns)

display(df)
