import mysql.connector
from mysql.connector import Error
import pandas as pd
import random
import string
import os
from pyconnector import *

#put in the actual database credentials you have on your end. 
connection = create_db_connection("localhost","root","1234","+games")


# samplequery="""
# insert into `Members`
# (`unique_id`, `mem_username`, `mem_password`)
# values
# (111, 'Anon', sha1('password123'));
# """
# ## above query does not work atm, below work. you can see it appear in the workbench table
# execute_query(connection, samplequery)

# companyinsert = """
# INSERT Company VALUES
# ('Microsoft'),('Bethesda'),('Arkane'),('Epic'),('Steam'),('Frontier'),('Ubisoft'),('Mojang');
# """

# execute_query(connection, companyinsert)
#-----------------------------------------------------
#Retrieving data and tabulating it in python
#-----------------------------------------------------

# selectquery = """
# select * from company;
# """
# qresult = read_query(connection, selectquery)
# for result in qresult:
#     print(result)

# print('\nLets put all that data into a row(array) instead')

# resultlist1 = []
# for result in qresult:
#     result=result
#     resultlist1.append(result)
#     print(result)

# print('\nLets put all that data into a column(2Darray) instead')

# resultlist2 = []
# for result in qresult:
#     result=list(result)
#     resultlist2.append(result)
#     print(result)

#now we can use those columns and display a table in python
#lets populate the tables first
# Safe Parameterized SQLquery method 
#("""SELECT count(*) FROM %(table_name)s """, {'table_name': table_name,})
#https://realpython.com/prevent-python-sql-injection/

# userquery = """insert into `Users` (`unique_id`) values (0);"""
# for x in range(0, 10):
#     execute_query(connection,userquery)

#suppose these are inputs from the html
for i in range(0,5):
    username= randomstring(16)
    password= randomstring(25)
    uniqueid= random.randint(1,100)
    print('\nUnique_id:'+str(uniqueid),'\nUsername:'+username,'\nPassword:'+password)
    
    addmembers(connection, uniqueid,username,password)


