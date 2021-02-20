#set this in the shell session or the server
#export GOOGLE_APPLICATION_CREDENTIALS="/home/niravadunuthula/Downloads/bolt-hacksc-firebase-adminsdk-rwia8-34ac113da0.json"
import firebase_admin
from firebase_admin import firestore

import threading
import datetime

from Matching import matchAPI

default_app = firebase_admin.initialize_app()
client = firestore.client()

snapshot = client.collection('users').document('alice').get()

def makeMatch(uuid1, uuid2, dist):
    #Create a Match Event for with the two specified users and update the currentMatch for each user
    activity_ref = client.collection('matchActivities').document()

    #get the date in format YYYY-MM-DD HH:MM:SS
    d = datetime.datetime.now()
    mindelay = 60 #The matchmaker will send a start time at least 60 seconds after the match is created, aligning with the nearest minute
    delayed = d.second+mindelay
    startTimestamp = datetime.datetime(d.year, d.month, d.day, d.hour, d.minute + 1 + delayed//60)

    activity_ref.set({
        u'startTimestamp': startTimestamp, #format YYYY-MM-DD HH:MM:SS
        u'distance': dist, #miles
        u'athlete1': {
            u'uuid': uuid1,
            u'distanceRun': 0,
            u'completionTime': 0
        },
        u'athlete2': {
            u'uuid': uuid2,
            u'distanceRun': 0,
            u'completionTime': 0
        },
        u'winner': None
    })
    
    user1_ref = client.collection('users').document(uuid1)
    user2_ref = client.collection('users').document(uuid2)

    user1_ref.update({
        u'currentMatch': activity_ref
    })
    user2_ref.update({
        u'currentMatch': activity_ref
    })

def listen_available():
    # Create an Event for notifying main thread.
    callback_done = threading.Event()
    
    # Create a callback on_snapshot function to capture changes
    def on_snapshot(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            print(f'Received document snapshot: {doc.id}')

            #get the users in the avaliable list
            available_users = doc.to_dict()['matches']

            #remove the users uuids from the available list and make a matchEvent with both users
            if len(available_users) > 1:
                matches = matchAPI(available_users)
                for (uuid1, uuid2, dist) in matches:
                    available_users.remove(uuid1)
                    available_users.remove(uuid2)
                    makeMatch(uuid1, uuid2, dist)

                doc.update({
                    u'uuid': available_users
                })

        callback_done.set()

    doc_ref = client.collection(u'matchwaiting').document(u'matchwaiting')

    # Watch the document
    doc_watch = doc_ref.on_snapshot(on_snapshot)

    # Wait for the callback.
    callback_done.wait(timeout=60)

    # Terminate watch on a document
    doc_watch.unsubscribe()