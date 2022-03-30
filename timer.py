from sense_hat import SenseHat
import numpy as np
from time import sleep
import numpy

# Sensehat setup
sense = SenseHat()
blue = [0, 0, 255]
grn = [0, 255, 0]
red = [255, 0, 0]
og = [252, 65, 3]
b = [0, 0, 0]

tiltInd = False
speedInd = False
fatigueInd = False

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
    initialTime = sec
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
    global tiltInd
    global speedInd
    global fatigueInd
    failInd = False
    xList = []
    yList = []
    zList = []
    while sec > 0:
        print(sec)
        acceleration = sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']
        x = abs(round(x, 2))
        y = abs(round(y, 2))
        z = abs(round(z, 2))
        xList.append(x)
        yList.append(y)
        zList.append(z)
        if phase == "concentric" or phase == "eccentric":
            if sec in np.arange(0, 0.5, 0.25) and ((np.average(xList) < 1 and np.average(yList) < 1 and np.average(zList) < 1)):
                print("Fatigue detected")
                fatigueInd = True
            elif sec in np.arange(0.5, initialTime-0.5) and (x > 1.075 or y > 1.075 or z > 1.075):
                print("Speed detected")
                speedInd = True

        orientation = sense.get_orientation()
        roll = round(orientation["roll"], 0)
        # print(roll)
        if roll not in range(85, 96):
            print("Bar tilt detected!")
            tiltInd = True
        sec -= .25
        sleep(0.25)
    sense.clear()
    if speedInd and tiltInd:
        failInd = True
    elif tiltInd:
        failInd = True
    elif speedInd:
        failInd = True
    elif fatigueInd:
        failInd = True
    else:
        failInd = False
    return failInd


def beginExercise(data):
    global tiltInd
    global speedInd
    failList = {}
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
            tiltInd = False
            speedInd = False
            failInd = []
            print("Current Rep: " + str(rep))
            # Reps function returns a boolean value
            # This is appended to the tiltInd list
            failInd.append(reps(data["concentric"], "concentric"))
            failInd.append(reps(data["isometric1"], "isometric1"))
            failInd.append(reps(data["eccentric"], "eccentric"))
            failInd.append(reps(data["isometric2"], "isometric2"))
            failString = ""
            if (speedInd and tiltInd) or (fatigueInd and speedInd) or (fatigueInd and tiltInd):
                failString = "multiple"
            elif speedInd:
                failString = "speed"
            elif tiltInd:
                failString = "bar-tilt"
            elif fatigueInd:
                failString = "fatigue"
            else:
                failString = " successful"
            # failInd list is assessed for any true values
            # if any fail is detected, fail data is appended to the failList
            failList["reasonSet"+str(set)] = failString
            failList["repsSet"+str(set)] = rep
            failList["totalReps"] = (set * rep)

    return failList


if __name__ == "__main__":
    data = {
        "sets": 1,
        "reps": 3,
        "pcntrm": 75,
        "restPeriod": 15,
        "eccentric": 4,
        "isometric1": 1,
        "concentric": 5,
        "isometric2": 1
    }
    failList = beginExercise(data)
    print(failList)
