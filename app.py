#app.py

#Import necessary packages
from flask import Flask
from flask_restful import Resource, reqparse, Api #Instantiate a flask object 
import threading
app = Flask(__name__)

#Instantiate Api object
api = Api(app)



class Match(Resource):
    def get(self, name):    
        matchAPI = matchAPI()  
        match = matchAPI.getMatch(name)

        return match

class Activity(Resource):
    def get(self, ):
        return


api.add_resource(Match, '/match')

if __name__=='__main__':        
    #Run the applications
    app.run() 

    