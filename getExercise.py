from sense_hat import SenseHat

sense = SenseHat()


def getExercise(name):
   print("Welcome: "+name)
   #default option
   option = "bp"
   while True:
      for event in sense.stick.get_events():
         if event.direction == "left":
            option = "dl"
            sense.show_message(option)
         if event.direction == "right":
            option = "sq"
            sense.show_message(option)
         if event.direction == "up":
            option = "bp"
            sense.show_message(option)
         elif event.direction == "middle":
            print(event.direction, event.action)
            return option
   return option

if __name__ == "__main__":
   option=getExercise("Ian")
   print(option)

   sense.clear()
