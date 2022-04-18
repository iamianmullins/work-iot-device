# Modified GPSD client script
# Original guide can be found at:
# https://wiki.52pi.com/index.php?title=EZ-0048#Addictional_solution_for_GPS_client
# https://gpsd.gitlab.io/gpsd/client-howto.html

import serial
import time
import json

# Access control serial port for USB GPS device
port = "/dev/ttyACM0"


def parseGPS(data):
    try:
        sdata = data.decode().split(",")

        # Ian Mullins -------------------------------------
        if sdata[0] == "$GPRMC":  # Recommended data provided by Glonass
            if sdata[2] == 'V':
                print("no satellite data available")
                return
            print("-------------------")
            print("---Parsing GPRMC---")
            print("-------------------")
            # Longitude and Latitude Formatting
            latf = float(sdata[3])/100
            longf = float(sdata[5])/100
            # Long and latitude data produce absolute values only
            # IF GPS heading is S or W, display negative value
            if sdata[4] == "S":
                latf *= -1
            if sdata[6] == "W":
                longf *= -1
            print(latf)
            print(longf)
            data = {
                "lat": latf,
                "long": longf
            }
            jsonString = json.dumps(data)
            with open('locationData.json', 'w') as locfile:
                locfile.write(jsonString)
            time.sleep(3600)
            # -----------------------------------------------
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")

# Decode byte data


def decode(coord):
    try:
        x = coord.split(".")
        head = x[0]
        tail = x[1]
        deg = head[0:-2]
        min = head[-2:]
        return deg + " deg " + min + "." + tail + " min"
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")


print("Receiving GPS data")
ser = serial.Serial(port, baudrate=9600, timeout=0.5)
while True:
    data = ser.readline()
    parseGPS(data)
