from sense_hat import SenseHat
from time import sleep

#Sensehat setup
sense = SenseHat()
blue = [0, 0, 255]

def countdown(sec, colour):
   timer = []
   #Display current timer in 10 second intervals
   while sec >= 10:
      if sec % 10 == 0:
         sense.show_message(str(sec), scroll_speed=0.05, text_colour=blue)
         sleep(1)
         sec -=1
         print(sec)
      elif sec % 10 != 0:
         sense.clear()
         print(sec)
         sec -=1
         sleep(1)
   #Countdown to 1
   while sec > 0:
      sense.show_letter(str(sec),colour)
      sec -=1
      sleep(1)
   sense.clear()
   return True





if __name__ == "__main__":
   sense.clear()
   countdown(20,blue)
