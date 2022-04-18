# Returns workout instructions object based on the fitness goal of the user
# Ian Mullins

def getWorkoutData(goalType):
    try:
        goal = goalType.lower().replace(" ", "")
        if goal == "endurance":
            data = {
                "sets": 3,
                "reps": 12,
                "pcntrm": 65,
                "restPeriod": 30,
                "eccentric": 6,
                "isometric1": 2,
                "concentric": 2,
                "isometric2": 2
            }
            return data
        elif goal == "hypertrophy":
            data = {
                "sets": 3,
                "reps": 8,
                "pcntrm": 75,
                "restPeriod": 60,
                "eccentric": 4,
                "isometric1": 1,
                "concentric": 1,
                "isometric2": 1
            }
            return data
        elif goal == "strength":
            data = {
                "sets": 5,
                "reps": 4,
                "pcntrm": 85,
                "restPeriod": 180,
                "eccentric": 2,
                "isometric1": 1,
                "concentric": 1,
                "isometric2": 1
            }
            return data
        else:
            data = {
                "sets": 2,
                "reps": 5,
                "pcntrm": 75,
                "restPeriod": 5,
                "eccentric": 3,
                "isometric1": 1,
                "concentric": 2,
                "isometric2": 1
            }
            return data
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


if __name__ == "__main__":
    getWorkoutData("strength")
    getWorkoutData("hypertrophy")
    getWorkoutData("endurance")
