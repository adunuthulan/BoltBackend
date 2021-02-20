#app.py

#Import necessary packages
from database import listen_available
from flask import Flask
from flask_restful import Resource, reqparse, Api #Instantiate a flask object 

from database import client
import threading
import sys

app = Flask(__name__)

#Instantiate Api object
api = Api(app)

class Match(Resource):
    def get(self): 
        x = threading.Thread(target=listen_available)
        x.start()
        return []

class Activity(Resource):
    def get(self, name):
        return

api.add_resource(Match, '/match')

if __name__=='__main__':        
    #Run the applications
   
    app.run() 
    
    