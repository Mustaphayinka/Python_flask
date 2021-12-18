from flask import Flask, request, jsonify, redirect, url_for
from flask_mysqldb import MySQL
import os



app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password1234'
app.config['MYSQL_DB'] = 'User'

mysql = MySQL(app)


# Fetch all data
@app.route('/', methods=['GET'])
def fetchall():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM userdetails")
    data = cur.fetchall()
    print(data)
    cur.close()
    return jsonify({"data": data})


# Fetch all with similarity
@app.route('/fetchOne', methods=['GET'])
def fetchOne():
    firstName = request.json['firstName']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM userdetails WHERE firstName=%s",(firstName,))
    data = cur.fetchall()
    cur.close()
    if data == ():
        return jsonify('No user by that name')
    else:
        return jsonify({"data": data})
    
    


# Post data
@app.route('/postData', methods=['POST'])
def postData():
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO userdetails(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
    mysql.connection.commit()
    cur.close()
    return jsonify("Result", {'firstName': firstName, 'lastName' : lastName})



# Update data
@app.route("/update", methods=["PUT"])
def update():
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE userdetails SET firstName='{}', lastName='{}' WHERE firstName='{}'".format(firstName, lastName, firstName))
    mysql.connection.commit()
    return 'done'




# Delete one
@app.route('/deleteOne', methods=['POST'])
def deleteOne():
    firstName = request.json['firstName']
    cur = mysql.connection.cursor()
    data = cur.execute("SELECT * FROM userdetails WHERE firstName=%s",(firstName,))
    if data == 0:
        return jsonify('No user by that name')
    cur.execute("DELETE FROM userdetails  WHERE firstName=%s",(firstName,))
    mysql.connection.commit()
    cur.close()
    return jsonify('User deleted successfully')



# Delete all
@app.route('/deleteAll', methods=['POST'])
def deleteAll():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM userdetails")
    mysql.connection.commit()
    cur.close()
    return jsonify('All users deleted successfully')


# Run server
if __name__ == "__main__":
    app.run(debug = True)