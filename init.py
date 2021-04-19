from flask import Flask
from flask import render_template, url_for, redirect, request

app = Flask(__name__)

@app.route('home')
@app.route('/')
def home():
   return render_template('home.html')

if __name__ == '__main__':
<<<<<<< HEAD
   app.run(debug=true)
=======
   app.run()

def signup():
   return render_template('signup_login.html')
>>>>>>> 5b082e6b55794da2e1d17919729d9bc9607468ef
