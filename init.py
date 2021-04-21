from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
   return render_template('home.html')
   

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if(request.method == 'GET'):
#         return render_template('signup_login.html')

#     email = request.form['email']
#     passwd = request.form['passwd']
#     data = getUsersData()
#     for key in data:
#         if(email == data[key]['email'] and passwd == data[key]['pass']):
#             user = User()
#             user.id = email
#             flask_login.login_user(user, remember=True)
#             next = request.args.get('next')
#             if(next):
#                 return redirect(next)
#             else:
#                 return redirect(url_for('home'))

#     abort(401) # if inside the for, it can't find valid username and password  

@app.route('/login', methods=['GET', 'POST'])
def login():
   return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
   return render_template('signup.html')


if __name__ == '__main__':
   app.run()