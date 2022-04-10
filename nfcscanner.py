# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example shows connecting to the PN532 with I2C (requires clock
stretching support), SPI, or UART. SPI is best, it uses the most pins but
is the most reliable and universally supported. In this example we put the PN532
into low power mode and sleep for 1 second in-between trying to read tags.
After initialization, try waving various 13.56MHz RFID cards over it!
"""
import time
import board
import busio
from digitalio import DigitalInOut

from sense_hat import SenseHat
sense = SenseHat()
blue = [0, 0, 255]
msg = "N"

# I2C import
from adafruit_pn532.i2c import PN532_I2C

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)

# With I2C, we recommend connecting RSTPD_N (reset) to a digital pin for manual
# harware reset
reset_pin = DigitalInOut(board.D6)
# On Raspberry Pi, you must also connect a pin to P32 "H_Request" for hardware
# wakeup! this means we don't need to do the I2C clock-stretch thing
req_pin = DigitalInOut(board.D12)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

def scan():
   print("Waiting for RFID/NFC card...")
   while True:
       # Check if a card is available to read
       sense.show_letter(str(msg), blue)
       uid = pn532.read_passive_target(timeout=0.5)
       print(".", end="")
       nfcId = ""
       if uid is not None:
           uidToString = [str(int) for int in uid]
           uidToString = "".join(uidToString).strip("0")
#           print("Found card with UID:", [hex(i) for i in uid])
           print ("Found card with UID: ", uidToString)
           nfcId= uidToString
           sense.clear()
           return nfcId
       pn532.power_down()
       time.sleep(1.0)


if __name__ == "__main__":
   scan()
