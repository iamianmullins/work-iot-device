import firebase_admin
from firebase_admin import credentials, firestore, db
import os
import json
from datetime import datetime
import uuid
from sense_hat import SenseHat


sense = SenseHat()
grn = [0, 255, 0]
blue = [0, 0, 255]

# Fetch the service account key JSON file contents
cred = credentials.Certificate('./fbase/serviceAccountKey.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://workiot-3acb1-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Returns session user-settings data retrieved from Firebase
def getUser(nfcScan):
    ref = db.reference('user-settings/')
    results = ref.get()
    print("---------")
    userData = getSessionUserSettings(results, nfcScan)
    return userData

# Get GUUID for workout push db
# Get workout settings for user session
def getSessionUserSettings(data, nfcId):
    for i in data:
        for j in data[i].values():
           if str(j['nfc']) ==nfcId:
              userDict = {
                  'guuid': i,
                  'uid': j['uid'],
                  'nfc': j['nfc'],
                  'exerciseGoal': j['exerciseGoal'],
                  'oneRmBp': j['oneRmBp'],
                  'oneRmDl': j['oneRmDl'],
                  'oneRmSq': j['oneRmSq'],
                  'email': j['email'],
              }
              goodNfc = ("Known NFC device found: " + str(nfcId))
              print (goodNfc)
              sense.show_message(str(goodNfc), scroll_speed=0.05, text_colour=blue)
              return userDict
           else:
              badNfc = ("NFC device unknown, please register in the WorkIOT app: " + str(nfcId))
              print (badNfc)
              sense.show_message(str(badNfc), scroll_speed=0.05, text_colour=blue)

# Save workout data to firebase /workouts and user-workouts
def pushDb(data):
    newUid = uuid.uuid4().hex
    now = datetime.now()
    dateTime = now.strftime("%d/%m/%y %H:%M:%S")
    db.reference('/workouts/').child(newUid).set({
       'timestamp': dateTime,
       'exerciseGoal': data['exerciseGoal'],
       'exerciseType': data['exerciseType'],
       'workingWeight': data['workingWeight'],
       'reasonSet1': data['reasonSet1'],
       'reasonSet2': data['reasonSet2'],
       'reasonSet3': data['reasonSet3'],
       'reasonSet4': data['reasonSet4'],
       'reasonSet5': data['reasonSet5'],
       'repsSet1': str(data['repsSet1']),
       'repsSet2': str(data['repsSet2']),
       'repsSet3': str(data['repsSet3']),
       'repsSet4': str(data['repsSet4']),
       'repsSet5': str(data['repsSet5']),
       'totalReps': str(data['totalReps']),
       'guuid': data['guuid'],
       'uid': newUid,
       'email': data['email'],
       })
    db.reference('/user-workouts/').child(data['guuid']).child(newUid).set({
       'timestamp': dateTime,
       'exerciseGoal': data['exerciseGoal'],
       'exerciseType': data['exerciseType'],
       'workingWeight': data['workingWeight'],
       'reasonSet1': data['reasonSet1'],
       'reasonSet2': data['reasonSet2'],
       'reasonSet3': data['reasonSet3'],
       'reasonSet4': data['reasonSet4'],
       'reasonSet5': data['reasonSet5'],
       'repsSet1': str(data['repsSet1']),
       'repsSet2': str(data['repsSet2']),
       'repsSet3': str(data['repsSet3']),
       'repsSet4': str(data['repsSet4']),
       'repsSet5': str(data['repsSet5']),
       'totalReps': str(data['totalReps']),
       'guuid': data['guuid'],
       'uid': newUid,
       'email': data['email'],
       })
    saveWorkout = ("Saving " + str(data['exerciseType']) + " workout!")
    print (saveWorkout)
    sense.show_message(str(saveWorkout), scroll_speed=0.05, text_colour=grn)
