# WorkIOT main script

import time
from firebase import getUser
from firebase import pushDb
from getWorkoutData import getWorkoutData
from timer import beginExercise
import getExercise
#import nfcscanner
from sense_hat import SenseHat
from gpiozero import Button
import time
import os

sense = SenseHat()
red = [255, 0, 0]
green = [0, 255, 0]
white = [255, 255, 255]
black = [0, 0, 0]
blue = [0, 0, 255]
orange = [247, 177, 0]


def shutdown():
    sense.clear(red)
    time.sleep(2)
    sense.clear()
    os.popen("sudo shutdown now").read()


def displayWorkoutData(exerciseGoal, workingWeight, sets, reps):
    try:
        goalMsg = ("Workout goal selected: " + exerciseGoal)
        wrkWeightMsg = ("You should be lifting: " +
                        str(workingWeight) + " kg's based on your 1 rep max")
        repsAndSetsMsg = ("You will do: " + str(sets) +
                          " sets " + " of " + str(reps) + " reps")
        print(goalMsg)
        print(wrkWeightMsg)
        print(repsAndSetsMsg)
        sense.show_message(str(goalMsg), scroll_speed=0.05, text_colour=blue)
        time.sleep(1)
        sense.show_message(str(wrkWeightMsg),
                           scroll_speed=0.05, text_colour=blue)
        time.sleep(1)
        sense.show_message(str(repsAndSetsMsg),
                           scroll_speed=0.05, text_colour=blue)
        time.sleep(1)
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


offButton = Button(16, hold_time=0.5)
offButton.when_held = shutdown
if __name__ == "__main__":
    try:
        print("\n----------------------------\n")
        print("----------\nWORKIOT\n----------")
        # get card id from NFC scanner
        while True:
            cardId = None
            exercise = None
            sense.show_message(str("Enter your card ID: "),
                               scroll_speed=0.05, text_colour=blue)
            # Read input for now due to broken hardware
            cardId = input("Enter your card ID: ")
            #cardId = nfcscanner.scan()
            if cardId is not None:
                fbData = getUser(cardId)
                if fbData is not None:
                    exercise = getExercise.getExercise()
                    repSetData = getWorkoutData(fbData["exerciseGoal"])

                    if exercise == "Bench-press":
                        workingWeight = (
                            round(float(int(fbData["oneRmBp"])/100)*int(repSetData["pcntrm"]), 2))
                    elif exercise == "Deadlifts":
                        workingWeight = (
                            round(float(int(fbData["oneRmDl"])/100)*int(repSetData["pcntrm"]), 2))
                    elif exercise == "Squats":
                        workingWeight = (
                            round(float(int(fbData["oneRmSq"])/100)*int(repSetData["pcntrm"]), 2))

                  #  displayWorkoutData(
                  #      fbData["exerciseGoal"], workingWeight, repSetData["sets"], repSetData["reps"])

                    workoutData = beginExercise(repSetData, exercise)
                    workoutData['guuid'] = fbData["guuid"]
                    workoutData['userId'] = fbData["uid"]
                    workoutData['email'] = fbData["email"]
                    workoutData['exerciseGoal'] = fbData["exerciseGoal"]
                    workoutData['exerciseType'] = exercise
                    workoutData['workingWeight'] = (workingWeight)

                    pushDb(workoutData)
#                    del cardId
#                    workoutData.clear()
#                    fbData.clear()

            time.sleep(2)
    except Exception as e:
        print("Oops!", e.__class__, "occurred in main.")
