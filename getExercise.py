# Sensehat script
# Allows a user to select exercise type

from sense_hat import SenseHat
sense = SenseHat()
green = (0, 255, 0)
scroll = 0.05


def getExercise():
    # default option
    str = "Select workout.."
    sense.show_message(str, scroll_speed=scroll)
    option = "bp"
    # Wait for user exercise selection via sensehat joystick
    # Joystick left = Deadlift
    # Joystick right = Squat
    # Joystick up = Bench Press
    # If Joystick pressed down and held, return relection
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
                sense.show_message(option, text_colour=green,
                                   scroll_speed=scroll)
                sense.clear()
                return option


if __name__ == "__main__":
    option = getExercise()
    print(option)
    sense.clear()
