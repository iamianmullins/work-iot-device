import firebase_admin
from firebase_admin import credentials, firestore, db
import os
import json

cred=credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://workiot-3acb1-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref = db.reference('/workouts')

def push_db(data):
    ref = db.reference('/workouts')
    home_ref = ref.child(data['userId'])
    home_ref.push({
        'userId' : data['userId'],
        'timestamp': data['timestamp'],
        'goal': data['goal'],
        'exercise' : data['exercise'],
        'weight' : data['weight'],
        'state1': data['state1'],
        'reason1': data['reason1'],
        'state2': data['state2'],
        'reason2': data['reason2'],
        'state3': data['state3'],
        'reason3': data['reason3'],
        'state4': data['state4'],
        'reason4': data['reason4'],
        'state5': data['state5'],
        'reason5': data['reason5']
        }
    )


if __name__ == "__main__":
   with open('exercise.json', 'r') as jsonfile:
      workoutdata = jsonfile.read()
   data = json.loads(workoutdata)
   print("Successful push")
   print("Timestamp: " + str(data['timestamp']))
   push_db(data)
