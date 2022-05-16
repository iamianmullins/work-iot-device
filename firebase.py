# Facilitates firebase connectivity for work-iot
# Retrieves user settings for a logged in user using an nfc id
# Once the workout has been complete, workout data is pushed to firebase realtime db
# Ian Mullins

import firebase_admin
from firebase_admin import credentials, db
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
    try:
        ref = db.reference('user-settings/')
        results = ref.get()
        print("---------")
        userData = getSessionUserSettings(results, nfcScan)
        return userData
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")

# Get GUUID for workout push db
# Get workout settings for user session


def getSessionUserSettings(data, nfcId):
    try:
        for i in data:
            for j in data[i].values():
                if str(j['nfc']) == str(nfcId):
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
                    goodNfc = ('User found: ' + userDict['email'])
                    print(goodNfc)
                    sense.show_message(
                        str(goodNfc), scroll_speed=0.05, text_colour=blue)
                    return userDict
                else:
                    badNfc = (
                        "NFC ID unknown: " + str(nfcId))
                    print(badNfc)
        sense.show_message(
        str(badNfc), scroll_speed=0.05, text_colour=blue)
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


# Save workout data to firebase /workouts and user-workouts
def pushDb(data):
    try:
        with open('locationData.json') as file:
            locData = json.load(file)
        print(locData)
        print(type(locData))
        print(locData['lat'])
        lat = round(locData['lat'], 6)
        long = round(locData['long'], 6)
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
            'repsSet1': data['repsSet1'],
            'repsSet2': data['repsSet2'],
            'repsSet3': data['repsSet3'],
            'repsSet4': data['repsSet4'],
            'repsSet5': data['repsSet5'],
            'totalReps': data['totalReps'],
            'uid': newUid,
            'latitude': lat,
            'longitude': long,
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
            'repsSet1': data['repsSet1'],
            'repsSet2': data['repsSet2'],
            'repsSet3': data['repsSet3'],
            'repsSet4': data['repsSet4'],
            'repsSet5': data['repsSet5'],
            'totalReps': data['totalReps'],
            'latitude': lat,
            'longitude': long,
            'uid': newUid,
            'email': data['email'],
        })
        saveWorkout = ("Saving " + str(data['exerciseType']) + " workout!")
        print(saveWorkout)
        sense.show_message(
            str(saveWorkout), scroll_speed=0.05, text_colour=grn)
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


if __name__ == '__main__':
    string = "123456"
    getUser(string)
