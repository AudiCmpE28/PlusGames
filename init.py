from flask import Flask, render_template, request, redirect, url_for
import os, sys
from flask_msqldb import MySQL
from pyconnector.py


app = Flask(__name__)

 mysql = MySQL(app)

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
   return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == "POST": ##gets info from form
      userDetails = request.form
      email= userDetails['email']
      password = userDetails['password']
      cur = mysql.connection.cursor() #open cursor
      cursor.execute("Insert INTO users(email, password) VALUES(%s, %s)", (username, email))
      cur.close()
   else:
      return render_template('login.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
   return render_template('signup.html')

@app.route('/request', methods=['GET', 'POST'])
def request():
   return render_template('request.html')


@app.route('/example', methods=['GET', 'POST'])
def example():
   result = (request.form['result'])
   cursor = connection.cursor()
   cursor.execute("get database testing result", result)
   return render_template('example.html', result = result)


@app.route('/game_page', methods=['GET', 'POST'])
def game_page():
   return render_template('game_page.html')

@app.route('/game_list', methods=['GET', 'POST'])
def game_list():
   return render_template('game_list.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
   return render_template('profile.html')



if __name__ == '__main__':
   app.run()