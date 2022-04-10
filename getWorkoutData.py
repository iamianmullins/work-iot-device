def getWorkoutData(goalType):
    goal = goalType.lower().replace(" ", "")
    if goal == "endurance":
        data = {
            "sets": 3,
            "reps": 12,
            "pcntrm": 65,
            "restPeriod": 30,
            "eccentric": 3,
            "isometric1": 1,
            "concentric": 4,
            "isometric2": 1
        }
        return data
    elif goal == "hypertrophy":
        data = {
            "sets": 3,
            "reps": 8,
            "pcntrm": 75,
            "restPeriod": 60,
            "eccentric": 3,
            "isometric1": 1,
            "concentric": 4,
            "isometric2": 1
        }
        return data
    elif goal == "strength":
        data = {
            "sets": 5,
            "reps": 4,
            "pcntrm": 85,
            "restPeriod": 180,
            "eccentric": 3,
            "isometric1": 1,
            "concentric": 4,
            "isometric2": 1
        }
        return data
    else:
        data = {
            "sets": 2,
            "reps": 2,
            "pcntrm": 75,
            "restPeriod": 25,
            "eccentric": 3,
            "isometric1": 1,
            "concentric": 4,
            "isometric2": 1
        }
        return data


if __name__ == "__main__":
    getWorkoutData("strength")
    getWorkoutData("hypertrophy")
    getWorkoutData("endurance")
