from flask import Flask, render_template, jsonify, request, redirect, url_for
from bson.objectid import ObjectId
import pymongo

# Initializing flask application
app = Flask(__name__)

# Connecting to local mongodb database
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')

# Creating a database
mydatabase = client['collection']

# Creating a collection in the database already created
collection = mydatabase['user']

# # # Routes for each functionality


# Get all data from the database
@app.route('/', methods = ['GET'])
def retriveAll():
    holder = []
    currentCollection = collection
    for i in currentCollection.find():
        holder.append({'firstname':i['firstname'],'email':i['email']})
    return jsonify('Users',holder)




# Get details with respect to objectId
@app.route('/get_details/<id>', methods = ['GET'])
def check(id):
    currentCollection = collection
    data = currentCollection.find_one({'_id': ObjectId(str(id))})
    if data == None:
        result = {'firstname':'No such record in the database', 'email' :'No such record in the database'}
    else:
        result = {'details' : {'firstname':data['firstname'], 'email' : data['email']}}
    return jsonify(result)


# retriving information with respect to firstname
@app.route('/<firstname>', methods = ['GET'])
def retriveFromName(firstname):
    currentCollection = collection
    data = currentCollection.find_one({'firstname': firstname})
    if data == None:
        result = {'firstname':'No such record in the database', 'email' :'No such record in the database'}
    else:
        result =  {'details' : {'firstname':data['firstname'], 'email' : data['email']}}
    return jsonify(result)



# Posting to the database
@app.route('/postData', methods = ['POST'])
def postData():
    currentCollection = collection
    firstName = request.json['firstname']
    surName = request.json['surname']
    email = request.json['email']
    currentCollection.insert_one({'firstname':firstName, 'Surname':surName, 'email':email})
    return jsonify({'firstname':firstName, 'Surname':surName, 'email':email})



# Update data in the database with respect to firstname
@app.route('/updateData/<firstname>', methods = ['PUT'])
def updateData(firstname):
    currentCollection = collection
    updatedFirstName = request.json['firstname']
    updatedSurName = request.json['surname']
    updatedEmail = request.json['email']
    currentCollection.update_one({'firstname': firstname}, {'$set' : {'firstname': updatedFirstName, 'Surname': updatedSurName, 'email': updatedEmail}})
    return jsonify("Updated result in the database", {'firstname': updatedFirstName, 'Surname': updatedSurName, 'email': updatedEmail})




# Delete data in the database with respect to firstname
@app.route('/deleteData/<firstname>', methods = ['DELETE'])
def deleteData(firstname):
    currentCollection = collection
    data = currentCollection.find_one({'firstname': firstname})
    print(data)
    if data == None:
        raise Exception("No such record in the database named {}".format(firstname))
    currentCollection.delete_one({'firstname': firstname})
    return '{} has been deleted'.format(firstname)


# Delete all data in the database
@app.route('/deleteAll', methods = ['DELETE'])
def deleteAll():
    currentCollection = collection
    currentCollection.delete_many({})
    return 'All records has been deleted'



if __name__ == '__main__' :
    app.secret_key = "123456789"
    app.run(debug = True)