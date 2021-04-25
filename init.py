from flask import Flask, render_template, request, redirect, url_for
import os, sys

app = Flask(__name__)

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
   return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
   
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


if __name__ == '__main__':
   app.run()