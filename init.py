from flask import Flask
from flask import render_template, url_for, redirect, request

app = Flask(__name__)

@app.route('home')
@app.route('/')
def home():
   return render_template('home.html')

if __name__ == '__main__':
   app.run(debug=true)