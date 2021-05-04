# SJSU CMPE 138 Spring 2021 TEAM1
## Run on terminal

pip install Flask

pip install mysql-connector-python

pip install pandas

pip install IPython

pip install flask-mysql-connector

pip install pyyaml

pip install -U flask-paginate

pip install flask_table

pip install Flask-Images

pip install mysqlclient

pip install flask-login

pip install flask_table

pip install -U flask-paginate

 ----------------------------------------------------------------------------------------------------------------------------
## Create the database in sql.sql

## You can import my Python-sql connector library in pyconnector.py

from pyconnector import *

## Write more connecting scripts like in pyconnector.py
## Test them out in pytesting.py or your own folder/file

 ----------------------------------------------------------------------------------------------------------------------------
### Safe Parameterized SQLquery method 
aquery = "SELECT count(*) FROM '{}' ;".format(table_name)<br>
execute_query(connection, aquery) #etc<br>
https://realpython.com/prevent-python-sql-injection/<br>
<br>
{} for a numeric argument<br>
'{}' for an argument that is a string<br>
Price, rating, etc are numeric so use {}<br>
comment text, review text, genre, game_name are varchar/string so use '{}'<br>

 ----------------------------------------------------------------------------------------------------------------------------
#### Create a db.yaml file in the base directory and put the following 4 lines in it. Add it to .gitignore so 
## you keep your own independent config files.
MYSQL_USER: 'root'
MYSQL_HOST: 'localhost'
MYSQL_PASSWORD: 'your_mysql_password'
MYSQL_DATABASE: '+games'
