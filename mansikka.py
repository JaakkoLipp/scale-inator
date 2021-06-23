###################
#### main file ####
###################
#import UI, data           #only works with aliohjelmas
#illegal goods import
import serial, datetime, sys

#serial init
ser = serial.Serial(
    port='COM5',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)


## MAIN
def main():
    currentID = input("SCAN ID: ")
    #serial read weight on scale
    weight = ser.readline()
    if currentID == prevID: # scam prevention, check same persons all baskets pls
        print("SAME AS PREVIOUS, NOT ACCEPTED.")
    else:
        #write
        print("accepted")


#serial close
ser.close()
