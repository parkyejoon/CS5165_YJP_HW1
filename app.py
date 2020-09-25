from flask import Flask, url_for, render_template
from flask import request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from info import openinfo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
        ## Create a Database Table ##
        id = db.Column(db.Integer, primary_key = True)
        username = db.Column(db.String(80), unique = True)
        password = db.Column(db.String(80))
        email = db.Column(db.String(80), unique = True)
        firstname = db.Column(db.String(80))
        lastname = db.Column(db.String(80))

        def __init__(self, username, password, email, firstname, lastname):
                self.username = username
                self.password = password
                self.email = email
                self.firstname = firstname
                self.lastname = lastname

@app.route('/', methods = ['GET', 'POST'])
def home():
        ## Search user information. The correct username and password are required. ##
        if not session.get('logged_in'):
                return render_template('index.html')
        else:
                if request.method == 'POST':
                        username = request.form['username']
                        password = request.form['password']
                        return render_template('index.html', data = openinfo(username, password))
                return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
        ## Login format, need to write down the correct username and password ##
        if request.method == 'GET':
                return render_template('login.html')
        else:
                name = request.form['username']
                passw = request.form['password']
                try:
                        data = User.query.filter_by(username = name, password = passw).first()
                        if data is not None:
                                session['logged_in'] = True
                                return redirect(url_for('home'))
                        else:
                                return 'Username or Password is wrong. Please try again.'
                except:
                        return "Username or Password is wrong. Please try again."

@app.route('/register/', methods = ['GET', 'POST'])
def register():
        ## Registeration, there are username, password, email, first name, and last name. ##
        if request.method == 'POST':
                new_user = User(username = request.form['username'], password = request.form['password'], 
                        email = request.form['email'], firstname = request.form['firstname'], lastname = request.form['lastname'])

                db.session.add(new_user)
                db.session.commit()
                return render_template('login.html')
        return render_template('register.html')

@app.route("/logout")
def logout():
        ## Logout ##
        session['logged_in'] = False
        return redirect(url_for('home'))

if __name__ == '__main__':
        ## Database security, 159515951 is password. ##
        db.create_all()
        app.secret_key = "159515951"
        app.run(host = '0.0.0.0', debug = True)
