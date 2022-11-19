from flask import Flask, Response, render_template
from camera import Video
import cv2
from keras.utils import load_img,img_to_array
import numpy as np
from skimage.transform import resize
from keras.models import load_model
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app.secret_key = 'your secret key'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'geeklogin'

app = Flask(__name__)
@app.route('/')
def index():
	return render_template('home.html')

@app.route('/asl')
def asl():
	return render_template('asl.html')

@app.route('/predict')
def predict():
	return render_template('predict.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

model=load_model('C:/Users/rohit/OneDrive/Desktop/VII/IBM-Project-19465-1659698319/Project Development Phase/Sprint 2/asl.h5')
def gen(video):
    while True:
        success, image = video.read()
        
        copy=image.copy()
        cv2.imwrite('img.jpg',copy)
        copy_img=load_img('img.jpg',target_size=(64,64,1))
        img=img_to_array(copy_img)
        img = resize(img,(64,64,1))
        img = np.expand_dims(img,axis=0)
        pred=np.argmax(model.predict(img))
        op=['A','B','C','D','E','F','G','H','I']
        print(op[pred])
        cv2.putText(image,op[pred],(100,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),3)

        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

video = cv2.VideoCapture(0)
@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run()
