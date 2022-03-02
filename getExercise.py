#Enables a user to select an exercise type
from sense_hat import SenseHat
sense = SenseHat()
green = (0,255,0)
scroll=0.05

#Initialise global variables
option = "deadlift"
exerciseSelected = False

# if joystick direction detected, update and display option
def left(event):
 if event.action == 'released':
    global option 
    option = "deadlift"
    sense.show_message(option, scroll_speed=scroll)
    sense.clear()

def right(event):
 if event.action == 'released':
    global option 
    option = "squat"
    sense.show_message(option, scroll_speed=scroll)
    sense.clear()

def up(event):
 if event.action == 'released':
    global option 
    option = "bench-press"
    sense.show_message(option, scroll_speed=scroll)
    sense.clear()

# If joystick direction == down, update exercise selected boolean to true
def down(event):
 if event.action == 'released':
    sense.show_message(option, scroll_speed=scroll, text_colour=green)
    sense.clear()
    global exerciseSelected
    exerciseSelected = True
             
# Assigned sensehat joystick directions
sense.stick.direction_up = up
sense.stick.direction_left = left
sense.stick.direction_right = right
sense.stick.direction_down = down
sense.stick.direction_middle = sense.clear 

def getExercise():
   #variable control for main.py while loop
   global option
   option=""
   global exerciseSelected
   exerciseSelected= False
   str = "Select workout.."
   sense.show_message(str, scroll_speed=scroll)
   # Do while exerciseSelected is False
   # Is only returned True when the direction_down is selected
   # Then return global option
   while not exerciseSelected:
      pass
   print (option)
   return option


if __name__ == "__main__":
   option=getExercise()
   print(option)
   sense.clear()
