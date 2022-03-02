import json
import time
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
   #get card id from NFC scanner
   while True:
      exercise =""
      cardId = None
      cardId = nfcscanner.scan()
      if cardId is not None:
         print(exercise+ "HERE")
         print("Card found with the following id: " + cardId)
         #fbData = getFirebaseData(cardId)
         fbData =  '{ "user":"Ian", "id":"123456A", "pcntrm":100, "goal":"strength", "sets":3, "reps":3}'
         if fbData is not None:
            # parse fbData:
            userData = json.loads(fbData)
            print ("found: " + userData["user"])
            exercise = getExercise.getExercise()
            print(exercise + " selected")
            repSetData = getWorkoutData(userData["goal"])
            print ("Workout selected for: " + userData["goal"])
            print ("You should be lifting: " + str(repSetData["pcntrm"]) + " kg's based on your 1 rep max")
            print ("You will do: " + str(repSetData["sets"])+ " sets " + " of " + str(repSetData["reps"]) + " reps")
            beginExercise(repSetData)
      time.sleep(2)


