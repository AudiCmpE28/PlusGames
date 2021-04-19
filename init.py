from flask import Flask, render_template
import os

app = Flask(__name__)

picFolder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = picFolder

@app.route('/')
def home():
   pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'gamesLOGO.png')
   return render_template('home.html', user_image = pic1)

if __name__ == '__main__':
   app.run()

