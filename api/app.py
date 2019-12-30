import os
import time
import secrets
from flask import Flask
from flask import request
from flask_cors import CORS
from pymongo import MongoClient
import json
from bson import ObjectId
from bson.json_util import dumps

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)
cors = CORS(app)

client = MongoClient('mongodb://db:27017/')
db = client.frequences
userCollection = db.user
widgetCollection = db.widget

# Misc

@app.route('/')
def index():
    return 'Hello world!\n'

@app.route('/about.json')
def about():
    res = {
        'client' : {
            'host' : request.remote_addr
        },
        'server' : {
            'current_time' : int(time.time()),
            'services' : [{
                'name' : 'spotify',
                'widgets' : [{
                    'name' : 'spotifyLastSongs',
                    'description' : 'Display 4 last albums of an artist',
                    'params' : [{
                        'name' : 'id',
                        'type' : 'string'
                    }]
                }, {
                    'name' : 'spotifyTopTracks',
                    'description' : 'Display 4 top tracks of an artist',
                    'params' : [{
                        'name' : 'id',
                        'type' : 'string'
                    }]
                }, {
                    'name' : 'spotifyRelatedArtists',
                    'description' : 'Display 4 artists related to an artist',
                    'params' : [{
                        'name' : 'id',
                        'type' : 'string'
                    }]
                }]
            },{
                'name' : 'deezer',
                'widgets' : [{
                    'name' : 'deezerLastSongs',
                    'description' : 'Display 4 last albums of an artist',
                    'params' : [{
                        'name' : 'id',
                        'type' : 'string'
                    }]
                }, {
                    'name' : 'deezerTopTracks',
                    'description' : 'Display 4 top tracks of an artist',
                    'params' : [{
                        'name' : 'id',
                        'type' : 'string'
                    }]
                }, {
                    'name' : 'deezerRelatedArtists',
                    'description' : 'Display 4 artists related to an artist',
                    'params' : [{
                        'name' : 'id',
                        'type' : 'string'
                    }]
                }]
            }]
        }
    }
    return res

# User table functions

@app.route('/list/user', methods=["GET"])
def userList():
    count = 0
    users = {}
    cursor = userCollection.find({})
    for document in cursor:
        users[count] = JSONEncoder().encode(document)
        count += 1
    return users

# Register / login endpoints

@app.route('/register', methods=["POST"])
def register():
    if request.args.get('email') is None or request.args.get('password') is None:
        return "E-mail or password doesn't exist."
    userCollection.insert_one({
        'email' : request.args.get('email'),
        'password' : request.args.get('password'),
        'token' : secrets.token_hex()
        })
    return "Account created."

@app.route('/register/tpa', methods=["POST"])
def registerTPA():
    if request.args.get('id_tpa') is None:
        return "Token doesn't exist."
    cursor = userCollection.find_one({
        'id_tpa' : request.args.get('id_tpa')
    })
    if cursor is not None and cursor['token'] is not None:
        return cursor['token']
    token = secrets.token_hex()
    userCollection.insert_one({
        'id_tpa' : request.args.get('id_tpa'),
        'token' : token
    })
    return token

@app.route('/login', methods=["POST"])
def login():
    if request.args.get('email') is None or request.args.get('password') is None:
        return "E-mail or password doesn't exist."
    cursor = userCollection.find_one({
        'email' : request.args.get('email'),
        'password' : request.args.get('password')
        })
    if cursor is None or cursor['token'] is None:
        return "No user associated."
    else:
        return cursor['token']

@app.route('/login/spotify', methods=["POST"])
def loginSpotify():
    if request.args.get('auth_token') is None or request.args.get('spotify_token') is None:
        return "No token provided."
    userCollection.update_one({
        'token' : request.args.get('auth_token')
        }, { '$set' : {
        'spotify' : request.args.get('spotify_token')
        }
        })
    cursor = userCollection.find_one({
        'token' : request.args.get('auth_token')
    })
    if cursor is None:
        return "No user associated."
    return JSONEncoder().encode(cursor)

@app.route('/login/deezer', methods=["POST"])
def loginDeezer():
    if request.args.get('auth_token') is None or request.args.get('deezer_token') is None:
        return "No token provided."
    userCollection.update_one({
        'token' : request.args.get('auth_token')
        }, { '$set' : {
        'deezer' : request.args.get('deezer_token')
        }
        })
    cursor = userCollection.find_one({
        'token' : request.args.get('auth_token')
    })
    if cursor is None:
        return "No user associated."
    return JSONEncoder().encode(cursor)

# Widget handling

@app.route('/list/widget', methods=["POST"])
def listWidget():
    if request.args.get('auth_token') is None:
        return 'Error invalid args.'
    cursor = userCollection.find_one({
        'token' : request.args.get('auth_token')
    })
    if cursor is None:
        return "No user associated."
    widgets = widgetCollection.find({'token' : {'$in': [ request.args.get('auth_token') ]}})
    return dumps(widgets)

@app.route('/register/widget', methods=["POST"])
def registerWidget():
    if request.args.get('widget_id') is None or request.args.get('widget_type') is None or request.args.get('widget_data') is None or request.args.get('widget_name') is None or request.args.get('auth_token') is None:
        return "Error invalid args."
    cursor = userCollection.find_one({
        'token' : request.args.get('auth_token')
    })
    if cursor is None:
        return "No user associated."
    cursor = widgetCollection.find_one({
        'id' : request.args.get('widget_id')
    })
    if cursor is None:
        cursor = widgetCollection.insert_one({
            'id' : request.args.get('widget_id'),
            'token' : request.args.get('auth_token'),
            'type' : request.args.get('widget_type'),
            'name' : request.args.get('widget_name'),
            'data' : request.args.get('widget_data')
        })
        return 'Created.'
    widgetCollection.update_one({
        'id' : request.args.get('widget_id')
        }, { '$set' : {
        'type' : request.args.get('widget_type'),
        'name' : request.args.get('widget_name'),
        'data' : request.args.get('widget_data')
        }
        })
    return 'Updated.'

@app.route('/remove/widget', methods=["POST"])
def removeWidget():
    if request.args.get('widget_id') is None:
        return "Error invalid args."
    widgetCollection.delete_one({'id' : request.args.get('widget_id')})
    return "Deleted."