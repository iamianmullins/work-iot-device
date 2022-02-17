import json

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
#   get card id from NFC scanner
#   cardId = nfcscanner.scan()
#   print("Card found with the followinf id: " + cardId)

   # getfirebase
   # not yet implemented
   # getfirebasedata(cardId)
   fbData =  '{ "user":"Ian", "id":"123456A", "1rm":100, "goal":"strength"}'

   # parse fbData:
   userData = json.loads(fbData)

#   exercise = getExercise.getExercise(userData["user"])
#   print(exercise)
   timer.countdown(10,blue)
   timer.countdown(3,orange)
   timer.countdown(1,red)
   timer.countdown(3,green)


