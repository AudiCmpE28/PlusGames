from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
   return render_template('home.html')
   
   
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('home'))

    # show the form, it wasn't submitted
    return render_template('login.html')


if __name__ == '__main__':
   app.run()