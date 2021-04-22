from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
   return render_template('home.html')
   


@app.route('/login', methods=['GET', 'POST'])
def login():
   return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
   return render_template('signup.html')

@app.route('/example', methods=['GET', 'POST'])
def example():
   return render_template('example.html')


if __name__ == '__main__':
   app.run()