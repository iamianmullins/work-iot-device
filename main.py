import json
import time
from firebase import getUser
from getWorkoutData import getWorkoutData
from timer import beginExercise
import getExercise
import nfcscanner

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
                print("Card found with the following id: " + cardId)
                fbData = getUser(cardId)
                if fbData is not None:
                    print(fbData["email"])
                    exercise = getExercise.getExercise()
                    print(exercise + " selected")
                    repSetData = getWorkoutData(fbData["exerciseGoal"])
                    print("Workout selected for: " + fbData["exerciseGoal"])
                    print("You should be lifting: " +
                          str(repSetData["pcntrm"]) + " kg's based on your 1 rep max")
                    print("You will do: " + str(repSetData["sets"]) +
                          " sets " + " of " + str(repSetData["reps"]) + " reps")
 #                   beginExercise(repSetData)
            time.sleep(2)
    except:
        print("An exception occurred in main")
