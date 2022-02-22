import firebase_admin
from firebase_admin import credentials, firestore, db
import os
import json
from datetime import datetime

# Fetch the service account key JSON file contents
cred=credentials.Certificate('./fbase/serviceAccountKey.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://workiot-3acb1-default-rtdb.europe-west1.firebasedatabase.app/'
})

#*****For testing purposes
#Read fbase/users.json
#Writes user to Firebase realtime database
def createUser():
    with open('./fbase/users.json', 'r') as jsonfile:
       userdata = jsonfile.read()
    data = json.loads(userdata)
    now = datetime.now()
    dateTime = now.strftime("%d/%m/%y %H:%M:%S")
    print (dateTime)
    ref = db.reference('/users')
    home_ref = ref.child(data['userId'])
    home_ref.push({
        'username' : data['username'],
        'userId' : data['userId'],
        'timestamp': dateTime,
        'goal': data['goal'],
        '1rm': data['1rm']
        }
    )


#Retrieves user from Firebase
def getUser(testId):
   #test user
   testId = '1225025456122'
   ref = db.reference('users/'+testId)
   results = ref.get()
   print (type(results))
   print (results)

#Read fbase/exercise.json
#Writes exercise to firebase realtime database
def pushDb():
   with open('./fbase/exercise.json', 'r') as jsonfile:
      workoutdata = jsonfile.read()
   data = json.loads(workoutdata)
   ref = db.reference('/workouts')
   now = datetime.now()
   dateTime = now.strftime("%d/%m/%y %H:%M:%S")
   print (dateTime)
   ref = db.reference('/workouts')
   home_ref = ref.child(data['userId'])
   home_ref.push({
      'userId' : data['userId'],
      'timestamp': dateTime,
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
#   pushDb()
#   createUser()
#   getUser(1)
