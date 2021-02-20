#app.py

#Import necessary packages
from database import listen_available
from flask import Flask
from flask_restful import Resource, reqparse, Api #Instantiate a flask object 

app = Flask(__name__)

#Instantiate Api object
api = Api(app)

class Match(Resource):
    def get(self): 
        listen_available()
        return

api.add_resource(Match, '/match')

from app import app as application 

if __name__=='__main__':        
    #Run the applications
    application.run() 
    