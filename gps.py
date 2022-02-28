import serial
import time
import json

#Access control serial port for USB GPS device
port = "/dev/ttyACM0"

def parseGPS(data):
     sdata = data.decode().split(",")
     if sdata[0] == "$GPRMC": #Recommended data provided by Glonass
        if sdata[2] == 'V':
            print ("no satellite data available")
            return
        print ("---Parsing GPRMC---")
        #Longitude and Latitude Formatting
        latf=float(sdata[3])/100
        longf=float(sdata[5])/100
        #Long and latitude data produce absolute values only
        #IF GPS heading is S or W, display negative value
        if sdata[4] == "S":
           latf*=-1
        if sdata[6] == "W":
           longf*=-1
        print(latf)
        print(longf)
        data = {
           "lat" : latf,
           "long" : longf
        }
        jsonString = json.dumps(data)
        with open('locationData.json', 'w') as locfile:
           locfile.write(jsonString)
        time.sleep(3600)

#Decode byte data
def decode(coord):
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"

print ("Receiving GPS data")
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
while True:
   data = ser.readline()
   parseGPS(data)
