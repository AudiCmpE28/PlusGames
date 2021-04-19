from flask import Flask, render_template
import os

#fetches the image
LOGO_PICTURE = os.path.join('static', 'images')


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = LOGO_PICTURE #obtains the folder where image is

@app.route('/')
@app.route('/home')
def home():
   logo_image = os.path.join(app.config['UPLOAD_FOLDER'], 'gamesLOGO.jpg') #pick image
   return render_template('home.html', user_image = logo_image)



if __name__ == '__main__':
   app.run()