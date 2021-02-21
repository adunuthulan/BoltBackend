#set this in the shell session or the server
#export GOOGLE_APPLICATION_CREDENTIALS="/Users/niravadunuthula/Downloads/bolt-hacksc-firebase-adminsdk-rwia8-34ac113da0.json"
import firebase_admin
from firebase_admin import firestore, credentials

from os import environ

import threading
import datetime

from matching import matchAPI

# ENV_KEYS = {
#     "type": "service_account",
#     "private_key_id": environ["FIREBASE_PRIVATE_KEY_ID"],
#     "private_key": environ["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
#     "client_email": environ["FIREBASE_CLIENT_EMAIL"],
#     "client_id": environ["FIREBASE_CLIENT_ID"],
#     "token_uri": environ["FIREBASE_TOKEN_URI"],
#     "project_id": environ["FIREBASE_PROJECT_ID"],
# }


# credentials = credentials.Certificate(ENV_KEYS)

# default_app = firebase_admin.initialize_app(credentials)
default_app = firebase_admin.initialize_app()
client = firestore.client()

def makeMatch(uuid1, uuid2, dist):
    #Create a Match Event for with the two specified users and update the currentMatch for each user
    activity_ref = client.collection('matchActivities').document()
    time_ref = client.collection('time').document('time')

    #get the date in format YYYY-MM-DD HH:MM:SS
    time_ref.set({'time':firestore.SERVER_TIMESTAMP})

    d = time_ref.get().to_dict()['time']
    mindelay = 5 #The matchmaker will send a start time at least 60 seconds after the match is created, aligning with the nearest minute
    delayed = d.second+mindelay
    #startTimestamp = datetime.datetime(d.year, d.month, d.day, d.hour, d.minute + 1 + delayed//60, delayed%60)
    demoTimestamp = datetime.datetime(d.year, d.month, d.day, d.hour, d.minute + delayed//60, delayed%60)

    activity_ref.set({
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
        u'distance': dist, #miles
        u'startTimestamp': demoTimestamp, #startTimestamp #format YYYY-MM-DD HH:MM:SS
        u'aid': activity_ref.id
    })

    user1_ref = client.collection('users').document(uuid1)
    user2_ref = client.collection('users').document(uuid2)

    user1_ref.update({
        u'currentMatch': activity_ref.id
    })
    user2_ref.update({
        u'currentMatch': activity_ref.id
    })

def listen_available():
    # Create an Event for notifying main thread.
    callback_done = threading.Event()

    doc_ref = client.collection(u'matchwaiting').document(u'matchwaiting')
    
    # Create a callback on_snapshot function to capture changes
    def on_snapshot(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            print(f'Received document snapshot: {doc.id}')

            #get the users in the avaliable list
            available_users = doc.to_dict()[u'users']

            #remove the users uuids from the available list and make a matchEvent with both users
            if len(available_users) > 1:
                matches = matchAPI(available_users)
                for (uuid1, uuid2, dist) in matches:
                    print(matches, ":", uuid1)
                    available_users.remove(uuid1)
                    available_users.remove(uuid2)
                    print(available_users)
                    makeMatch(uuid1, uuid2, dist)
                doc_ref.set({
                    u'users': available_users
                })

        callback_done.set()

    # Watch the document
    doc_watch = doc_ref.on_snapshot(on_snapshot)

    # Wait for the callback.
    callback_done.wait(timeout=60)

    # Terminate watch on a document
    doc_watch.unsubscribe()

def listen_terminate():
    
    return