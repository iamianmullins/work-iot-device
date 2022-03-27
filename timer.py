from sense_hat import SenseHat
from time import sleep
import numpy

# Sensehat setup
sense = SenseHat()
blue = [0, 0, 255]
grn = [0, 255, 0]
red = [255, 0, 0]
og = [252, 65, 3]
b = [0, 0, 0]

# LED martix arrows
# Green up arrow
arrowUp = [
    b, b, b, grn, grn, b, b, b,
    b, b, grn, grn, grn, grn, b, b,
    b, grn, b, grn, grn, b, grn, b,
    grn, b, b, grn, grn, b, b, grn,
    b, b, b, grn, grn, b, b, b,
    b, b, b, grn, grn, b, b, b,
    b, b, b, grn, grn, b, b, b,
    b, b, b, grn, grn, b, b, b
]
# Orange down arrow
arrowDown = [
    b, b, b, og, og, b, b, b,
    b, b, b, og, og, b, b, b,
    b, b, b, og, og, b, b, b,
    b, b, b, og, og, b, b, b,
    og, b, b, og, og, b, b, og,
    b, og, b, og, og, b, og, b,
    b, b, og, og, og, og, b, b,
    b, b, b, og, og, b, b, b
]

# Countdown timer using sensehat LED matrix
# Used to display rest period timer between sets


def countdown(sec, colour):
    # Display current timer in 10 second intervals
    while sec >= 10:
        if sec % 10 == 0:
            sense.show_message(str(sec), scroll_speed=0.05, text_colour=blue)
            sleep(1)
            sec -= 1
            print(sec)
        elif sec % 10 != 0:
            sense.clear()
            print(sec)
            sec -= 1
            sleep(1)
    # Countdown to 1
    while sec > 0:
        sense.show_letter(str(sec), colour)
        sec -= 1
        sleep(1)
    sense.clear()
    return True


# Control for repitition phase
def reps(sec, phase):
    # phase provides user instruction for
    # lifting(concentric),
    # stationary(isometric1)or(isometric2)
    # lowering(eccentric),
    if phase == "concentric":
        sense.set_pixels(arrowUp)
    elif phase == "eccentric":
        sense.set_pixels(arrowDown)
    elif phase == "isometric1" or phase == "isometric2":
        sense.show_letter("!", red)
    # Tilt indicator is set to False
    # If orientation is not between 85-96,
    # tilt is detected and tiltInd is set to true
    tiltInd = False
    while sec > 0:
        orientation = sense.get_orientation()
        roll = round(orientation["roll"], 0)
        print(roll)
        if roll not in range(85, 96):
            print("Bar tilt detected!")
            tiltInd = True
        sec -= .25
        sleep(0.25)
    sense.clear()
    return tiltInd


def beginExercise(data):
    failList = []
# sets for loop
    for set in range(1, data["sets"]+1):
        print("Current Set: " + str(set))
        if set != 1:
            # rest period between sets
            countdown(data["restPeriod"], blue)
        else:
            countdown(30, blue)
        # reps for loop
        for rep in range(1, data["reps"]+1):
            tiltInd = []
            print("Current Rep: " + str(rep))
            # Reps function returns a boolean value
            # This is appended to the tiltInd list
            tiltInd.append(reps(data["concentric"], "concentric"))
            tiltInd.append(reps(data["isometric1"], "isometric1"))
            tiltInd.append(reps(data["eccentric"], "eccentric"))
            tiltInd.append(reps(data["isometric2"], "isometric2"))
            # tiltInd list is assessed for any true values
            # if any fail is detected, fail data is appended to the failList
            if numpy.any(tiltInd):
                print("Set: " + str(set) + ", Rep: " + str(rep) + " failed")
                fail = ("Set: " + str(set) + ", Rep: " + str(rep) + " failed")
                failList.append(fail)
    print(failList)
    return failList


if __name__ == "__main__":
    data = {
        "sets": 2,
        "reps": 2,
        "pcntrm": 75,
        "restPeriod": 10,
        "eccentric": 3,
        "isometric1": 1,
        "concentric": 4,
        "isometric2": 1
    }
    failList = beginExercise(data)
    print(failList)
