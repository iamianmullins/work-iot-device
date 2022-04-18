# Sensehat script
# Allows a user to select exercise type
# Ian Mullins

from sense_hat import SenseHat
green = (0, 255, 0)
scroll = 0.05


def getExercise():
    try:
        sense = SenseHat()
        str = "Select workout.."
        print(str)
        sense.show_message(str, scroll_speed=scroll)
        option = None
        if option is not None:
            del option
        # Wait for user exercise selection via sensehat joystick
        # Joystick left = Deadlift
        # Joystick right = Squat
        # Joystick up = Bench Press
        while True:
            for event in sense.stick.get_events():
                if event.direction == "left":
                    option = "Deadlifts"
                    sense.show_message(
                        option, text_colour=green, scroll_speed=scroll)
                    sense.clear()
                    return option
                elif event.direction == "right":
                    option = "Squats"
                    sense.show_message(
                        option, text_colour=green, scroll_speed=scroll)
                    sense.clear()
                    return option
                elif event.direction == "up":
                    option = "Bench-press"
                    sense.show_message(
                        option, text_colour=green, scroll_speed=scroll)
                    sense.clear()
                    return option
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


if __name__ == "__main__":
    option = getExercise()
    print(option)
    sense.clear()
