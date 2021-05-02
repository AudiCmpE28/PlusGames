import mysql.connector
import os
from mysql.connector import Error
import pandas as pd
import random
import string
from IPython.display import display
from pyconnector import *
from flask import Flask, request,render_template

#put in the actual database credentials you have on your end. 
connection = create_db_connection("localhost","root","1234","+games")


companyinsert = """
INSERT Company VALUES
('Microsoft'),('Bethesda'),('Arkane'),('Epic'),('Steam'),('Frontier'),('Ubisoft'),('Mojang');
"""
#Since we can only have unique companies, run only once
#execute_query(connection, companyinsert)

#-----------------------------------------------------
#Retrieving data and tabulating it in python
#-----------------------------------------------------

selectquery = """select * from company;"""
#reads and returns a list of companies
qresult = read_query(connection, selectquery)
for result in qresult:
    print(result)

print('\nLets put all that data into a row(array) instead')

resultlist1 = []
for result in qresult:
    result=result
    resultlist1.append(result)
    print(result)

print('\nLets instead put all that data into a column(2Darray).\nSee example at Line70 how we can use these columns to make proper tables')

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

# userquery = """insert into `Users` (`unique_id`) values (0);"""
# for x in range(0, 10):
#     execute_query(connection,userquery)

## suppose these random strings are user inputs from the website
for i in range(0,1):
    uniqueid= random.randint(1,100000)
    username= randomstring(16)
    email=randomstring(5)+'@'+randomstring(5)+'.com'
    password= randomstring(25)
    print('\nUnique_id:'+str(uniqueid)+'\nUsername:'+username+'\nEmail:'+email+'\nPassword:'+password)
    addmembers(connection, uniqueid,username,email,password)


# Tabulate the query results!
mem_db = []
sel_mem="select Members.unique_id, Members.mem_username, Members.mem_email,  Members.mem_password from Members;"
member_read = read_query(connection, sel_mem)
for result in member_read:
    result = list(result)
    mem_db.append(result)



columns = ["unique_id", "mem_username", "mem_email","mem_password"]
#df = pd.DataFrame(mem_db, columns=columns)
##Display dataframe/table
#display(df)

#----------------------------------------#
#dumps whole 2darray
#print(returncolumns(connection,sel_mem),end='\n')
#vs
#read a row for each column, dataframe is nicer
#for x in returncolumns(connection,sel_mem):
#    print(x)

displaytable(columns,returncolumns(connection,sel_mem))