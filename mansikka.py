###################
#### main file ####
###################
#import UI, data           #only works with aliohjelmas
#illegal goods import
import serial, datetime, sys, random
import time
#serial init
"""ser = serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)"""


def serRep(): #replaces serial input for demo
    return round(random.uniform(1,6), 2)

## MAIN
def main():
    prevID = ""
    while(1):
        currentID = int(input("SCAN ID: "))
        time.sleep(1)
        #serial read weight on scale
        """weight = ser.readline()"""
        weight = serRep() #read "serial"
        if currentID == prevID: # scam prevention, check same persons all baskets pls
            print("SAME AS PREVIOUS,\n NOT ACCEPTED.")
            continue
        collector = ((currentID-1)//20)+1
        prevID = currentID
main()

#serial close
"""ser.close()"""
