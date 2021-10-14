from flask import Flask
from app import app
from app.models import User

@app.route('/user/signup', methods = ['GET'])
def signup():
    return User().signup()
