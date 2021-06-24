###################
#### main file ####
###################
#import UI, data           #only works with aliohjelmas
#illegal goods import
import serial, datetime, sys, random
import time
#serial init
"""ser = serial.Serial(
    port='COM5',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
"""

def serRep(): #replaces w serial input for demo
    return round(random.uniform(1,6), 2)

## MAIN
def main():
    prevID = ""
    while(1):
        currentID = int(input("SCAN ID: "))
        time.sleep(1)
        #serial read weight on scale
        """weight = ser.readline()"""
        weight = serRep()
        if currentID == prevID: # scam prevention, check same persons all baskets pls
            print("SAME AS PREVIOUS,\n NOT ACCEPTED.")
            continue
        else:
            if currentID < 5: #korit [0-4]
                #write
                print("accepted, ", currentID)
                print("WEIGHT WRITTEN SUCCESSFULLY", weight, "kg.")
                print()
            elif currentID >= 5 and currentID < 10: #korit [5-9]
                #write
                print("accepted, ", currentID)
                print("WEIGHT WRITTEN SUCCESSFULLY", weight, "kg.")
                print()
            elif currentID >= 10 and currentID < 15: #korit [10-14]
                #write
                print("accepted, ", currentID)
                print("WEIGHT WRITTEN SUCCESSFULLY", weight, "kg.")
                print()
        prevID = currentID
main()
#serial close
"""ser.close()"""
