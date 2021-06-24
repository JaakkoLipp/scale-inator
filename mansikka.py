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
    try:
        while(1):
            try:
                currentID = input("SCAN ID, Q to exit and save: ")
                if currentID == "q":
                    print("Saving...")
                    #file close
                    break
                else:
                    currentID=int(currentID)
            except:
                print("SCAN FAILED")
                continue
            time.sleep(1)
            #serial read weight on scale
            """weight = ser.readline()"""
            weight = serRep() #read "serial"
            if currentID == prevID: # scam prevention, check same persons all baskets pls
                print("SAME AS PREVIOUS,\nNOT ACCEPTED.")
                continue
            collector = ((currentID-1)//20)+1
            print("#",str(collector)+",","SUCCESSFULLY SAVED", weight, "kg")
            #csv write weight+ID same row different columns
            prevID = currentID
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Program failed, closing and saving...")
        #file close
        sys.exit(-1)

main()

#serial close
"""ser.close()"""
