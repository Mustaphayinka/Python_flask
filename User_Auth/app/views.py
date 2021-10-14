from flask import Flask, redirect, render_template, session, request, jsonify, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app import app
import bcrypt
import pymongo
from pymongo import MongoClient
import re


# Connecting to local mongodb database
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
# Creating a database
mydatabase = client['Students']
# Creating a collection in the database already created
collection = mydatabase['Students_Info']


@app.route("/", methods=['post', 'get'])
def home():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user_found = collection.find_one({"name": re.compile(user, re.IGNORECASE)})
        email_found = collection.find_one({"email": re.compile(user, re.IGNORECASE)})
        if user_found:
            message = "There's already a user by that name"
            return render_template('home.html', message=message)
        if email_found:
            message = 'This email already exists'
            return render_template('home.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('home.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            collection.insert_one(user_input)
            user_data = collection.find_one({"email": email})
            new_email = user_data['email']
   
            return render_template('logged_in.html', email=new_email, user = user_data)
    return render_template('home.html')




@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = collection.find_one({"email": re.compile(email, re.IGNORECASE)})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route('/logged_in/')
def logged_in():
    if "email" in session:
        email = session.get('email')
        user = collection.find_one({'email': re.compile(email, re.IGNORECASE)})
        session["log"] = True
        return render_template('logged_in.html', user=user, email = email)
    else:
        return redirect(url_for("login"))



@app.route('/signout', methods = ["GET","POST"])
def logout():
    message = 'Please login to your account'
    if "email" in session:
        session.clear()
        return redirect(url_for('login', message = message))
    else:
        return redirect(url_for("home"))
