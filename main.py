import json
import time
from firebase import getUser
from firebase import pushDb
from getWorkoutData import getWorkoutData
from timer import beginExercise
import getExercise
import nfcscanner
from sense_hat import SenseHat

sense = SenseHat()
red = [255, 0, 0]
green = [0, 255, 0]
white = [255, 255, 255]
black = [0, 0, 0]
blue = [0, 0, 255]
orange = [247, 177, 0]

if __name__ == "__main__":
    try:
        # get card id from NFC scanner
        while True:
            exercise = ""
            cardId = None
            cardId = nfcscanner.scan()
            if cardId is not None:
                fbData = getUser(cardId)
                if fbData is not None:
                    exercise = getExercise.getExercise()
                    repSetData = getWorkoutData(fbData["exerciseGoal"])
                    if exercise == "bench-press":
                       workingWeight = str(round(float(int(fbData["oneRmBp"])/100)*int(repSetData["pcntrm"]), 2))
                    elif exercise == "deadlift":
                       workingWeight = str(round(float(int(fbData["oneRmDl"])/100)*int(repSetData["pcntrm"]), 2))
                    elif exercise == "squat":
                       workingWeight = str(round(float(int(fbData["oneRmSq"])/100)*int(repSetData["pcntrm"]), 2))
                    goalMsg = ("Workout goal selected: " + fbData["exerciseGoal"])
                    wrkWeightMsg = ("You should be lifting: " +
                          str(workingWeight) + " kg's based on your 1 rep max")
                    repsAndSetsMsg = ("You will do: " + str(repSetData["sets"]) +
                          " sets " + " of " + str(repSetData["reps"]) + " reps")
                    print (goalMsg)
                    print (wrkWeightMsg)
                    print (repsAndSetsMsg)
                    sense.show_message(str(goalMsg), scroll_speed=0.05, text_colour=blue)
                    time.sleep(1)
                    sense.show_message(str(wrkWeightMsg), scroll_speed=0.05, text_colour=blue)
                    time.sleep(1)
                    sense.show_message(str(repsAndSetsMsg), scroll_speed=0.05, text_colour=blue)
                    time.sleep(1)
                    workoutData = beginExercise(repSetData)
                    workoutData['guuid'] = fbData["guuid"]
                    workoutData['userId'] = fbData["uid"]
                    workoutData['email'] = fbData["email"]
                    workoutData['exerciseGoal'] = fbData["exerciseGoal"]
                    workoutData['exerciseType'] = exercise
                    workoutData['workingWeight'] = (str(workingWeight))
                    pushDb(workoutData)
                    workoutData.clear()
                    fbData.clear()

            time.sleep(2)
    except:
        print("An exception occurred in main")
