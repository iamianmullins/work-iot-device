from warnings import catch_warnings
from sense_hat import SenseHat
import numpy as np
from time import sleep

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
    try:
        # Display current timer in 10 second intervals
        while sec >= 10:
            if sec % 10 == 0:
                sense.show_message(
                    str(sec), scroll_speed=0.025, text_colour=blue)
                sleep(1)
                print(sec)
                sec -= 1
            elif sec % 10 != 0:
                sense.clear()
                print(sec)
                sec -= 1
                sleep(1)
        # Countdown to 1
        while sec > 0:
            sense.show_letter(str(sec), colour)
            print(sec)
            sec -= 1
            sleep(1)
        sense.clear()
        return True
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


# Control for repitition phase
def reps(sec, phase):
    try:
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
            # print(sec)
            acceleration = sense.get_accelerometer_raw()
            y = acceleration['y']
            y = abs(round(y, 2))
            yList.append(y)
            orientation = sense.get_orientation()
            roll = round(orientation["roll"], 0)
            pitch = round(orientation["pitch"], 0)
            if phase == "concentric" or phase == "eccentric":
                if sec in np.arange(0, 1, 0.25) and (round(np.amax(yList), 2) in np.arange(0.98, 1.03, 0.01)):
                    print("Fatigue detected")
                    fatigueInd = True
                elif sec in np.arange(0.5, initialTime-0.5) and (np.amax(yList) > 1.5):
                    print("Speed detected")
                    speedInd = True
                if pitch in range(0, 11) or pitch in range(350, 361):
                    if roll not in range(80, 101):
                        print("Bar tilt detected!")
                        tiltInd = True
            sec -= .25
            sleep(0.25)
        sense.clear()
        if tiltInd:
            failInd = True
        if speedInd:
            failInd = True
        if fatigueInd:
            failInd = True
        else:
            failInd = False
        return failInd
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


def beginExercise(data, exercise):
    try:
        global tiltInd
        global speedInd
        global fatigueInd
        failList = {}
    # sets for loop
        for set in range(1, data["sets"]+1):
            tiltInd = False
            speedInd = False
            fatigueInd = False
            print("Current Set: " + str(set))
            if set != 1:
                # rest period between sets
                countdown(data["restPeriod"], blue)
            else:
                # Countdown to begin workout
                countdown(20, blue)
            # reps for loop
            for rep in range(1, data["reps"]+1):
                failInd = []
                print("Current Rep: " + str(rep))
                # Reps function returns a boolean value
                # This is appended to the tiltInd list
                if (exercise == "Bench-press" or exercise == "Squats"):
                    failInd.append(reps(data["eccentric"], "eccentric"))
                    failInd.append(reps(data["isometric1"], "isometric1"))
                    failInd.append(reps(data["concentric"], "concentric"))
                    failInd.append(reps(data["isometric2"], "isometric2"))
                elif (exercise == "Deadlifts"):
                    failInd.append(reps(data["concentric"], "concentric"))
                    failInd.append(reps(data["isometric1"], "isometric1"))
                    failInd.append(reps(data["eccentric"], "eccentric"))
                    failInd.append(reps(data["isometric2"], "isometric2"))
                    failString = ""
                if (speedInd and tiltInd) or (fatigueInd and speedInd) or (fatigueInd and tiltInd):
                    failString = "Multiple"
                elif speedInd:
                    failString = "Speed"
                elif tiltInd:
                    failString = "Bar-tilt"
                elif fatigueInd:
                    failString = "Fatigue"
                else:
                    failString = "N/A"
                # failInd list is assessed for any true values
                # if any fail is detected, fail data is appended to the failList
                failList["reasonSet"+str(set)] = failString
                failList["repsSet"+str(set)] = rep
                failList["totalReps"] = (set * rep)
        for set in range(data["sets"]+1, 6):
            failList["reasonSet"+str(set)] = "N/A"
            failList["repsSet"+str(set)] = 0
            # print("FAILLIST")
            print(failList)
        return failList
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


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
    print(type(failList))
    print(failList)
