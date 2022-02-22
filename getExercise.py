#Sensehat script
#Allows a user to select exercise type

from sense_hat import SenseHat
sense = SenseHat()
green = (0,255,0)
scroll=0.05

def getExercise(name):
   #print("Welcome: " + name)
   #default option
   str = "Select workout.."
   sense.show_message(str, scroll_speed=scroll)
   option = "bp"
   while True:
      for event in sense.stick.get_events():
         if event.direction == "left":
            option = "deadlift"
            sense.show_message(option, scroll_speed=scroll)
            sense.clear()
         elif event.direction == "right":
            option = "squat"
            sense.show_message(option, scroll_speed=scroll)
            sense.clear()
         elif event.direction == "up":
            option = "bench-press"
            sense.show_message(option, scroll_speed=scroll)
            sense.clear()
         elif event.direction == "down" and event.action == "held":
            sense.show_message(option, text_colour=green, scroll_speed=scroll)
            sense.clear()
            return option
   return option

if __name__ == "__main__":
   option=getExercise("Ian")
   print(option)
   sense.clear()
