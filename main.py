import json
import time
import timer
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
      cardId = None
      cardId = nfcscanner.scan()
      if cardId is not None:
         print("Card found with the following id: " + cardId)
         #fbData = getFirebaseData(cardId)
         fbData =  '{ "user":"Ian", "id":"123456A", "1rm":100, "goal":"strength"}'
         if fbData is not None:
            # parse fbData:
            userData = json.loads(fbData)
            print ("found: " + userData["user"])
            exercise = getExercise.getExercise(userData["user"])
            print(exercise)
      time.sleep(2)
#   timer.countdown(10,blue)
#   timer.countdown(3,orange)
#   timer.countdown(1,red)
#   timer.countdown(3,green)


