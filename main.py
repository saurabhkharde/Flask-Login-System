#!/usr/bin/python3
# latin-1
from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import re

conn = pymysql.connect(host="localhost", user="root", passwd="", db="login")
cursor = conn.cursor()

app = Flask(__name__)

app.secret_key = "123456789"

#@app.route('/')
#def index():
#    return render_template('index.html')


@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
      
        cursor.execute('SELECT * FROM accounts WHERE email = %s OR phone = %s AND password = %s', (username, username, password))

        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['fname'] = account[1]
            session['lname'] = account[2]
            session['email'] = account[3]
            session['phone'] = account[4]
            session['password'] = account[5]
            return redirect(url_for('home'))
        else:
            msg = 'Please Try Again...'
    return render_template('index.html', msg='')


@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():

    msg = ''
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'email' in request.form and 'password' in request.form and 'phone' in request.form:
        fname = request.form['fname']
        lname = request.form['lname']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']

        cursor.execute('SELECT * FROM accounts WHERE email = %s', (email))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not fname or not lname or not email or not phone or not password:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s)', (fname, lname, email, phone, password))
            conn.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


@app.route('/pythonlogin/forget_password', methods = ['GET','POST'])
def forget_password():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'new_password' in request.form:
        email = request.form['email']
        password = request.form['password']
        new_password = request.form['new_password']
       
        cursor.execute('SELECT * FROM accounts WHERE email = %s', (email))
        account = cursor.fetchone()

        if account:
            if password == new_password:
                cursor.execute('UPADTE accounts SET password = %s WHERE email = %s', (password , email))
                conn.commit()
                msg = 'Password Successfully Changed..!!'
            else:
                msg = "Password Doesn't Match"
        else:
            msg = "Email Not Found....!!"

    return render_template('forget_password.html', msg='')



@app.route('/pythonlogin/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', fname=session['fname'])
    return redirect(url_for('login'))    

@app.route('/pythonlogin/profile')
def profile():
    return render_template('profile.html', fname=session['fname'], email=session['email'], password=session['password'], phone=session['phone'])

@app.route('/pythonlogin/logout')
def logout():
    session ['loggedin'] = False
    return render_template('index.html')


if __name__ =='__main__':
	app.run(debug=True)
