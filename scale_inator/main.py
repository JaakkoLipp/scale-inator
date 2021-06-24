##################
#### mansikka ####
##################
#https://cdn.discordapp.com/attachments/624244854754377758/857616413937106954/unknown.png
from argparse import ArgumentParser
# import datetime
import random
import serial
import sys
# import time
import UI

def serRep():
    '''
    Serial like weight generator, Replaces serial input for demo
    '''
    return round(random.uniform(1, 6), 2)


def cleanup():
    '''
    Close serial and file gracefully
    '''
    if not arguments.pretend:
        ser.close()  # noqa: F821
    # file close


def main():
    '''
    Main function and program loop
    '''
    # Argument parsing
    parser = ArgumentParser()
    parser.add_argument("-p", "--pretend", action="count",
                        help="Use dummy data instead of reading from serial")
    global arguments
    arguments = parser.parse_args()

    if not arguments.pretend:
        # serial init
        """ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0)"""

    # set variable for id
    previousID = None

    # while loop failure handling
    try:
        while (True):
            currentID = input("Scan ID, Q to exit and save: ")
            if currentID.upper() == "Q":
                print("Saving...")
                # file close
                # serial close
                if not arguments.pretend:
                    ser.close()
                break
                # no quit
            else:
                # convert id to int
                currentID = int(currentID)

            # read weight from scale
            if not arguments.pretend:
                weight = ser.readline()
            else:
                weight = serRep()

            # ID processing

            # scam prevention, check same persons all baskets pls
            if currentID == previousID:
                print("SAME AS PREVIOUS,\nNOT ACCEPTED.")
                UI.createWindow(False,0,0)
                continue

            # prints & collector
            collector = ((currentID-1)//20)+1  # calculates collector from ID
            print("#%s, SUCCESSFULLY SAVED %skg" % (collector, weight))
            UI.createWindow(True,collector,weight)
            # csv write weight+ID same row different columns
            previousID = currentID
    except:  # noqa: E722
        # save closing with file & serial
        print("Unexpected error: %s" % sys.exc_info()[0])
        print("Program failed, closing and saving...")
        cleanup()
        sys.exit(-1)
    cleanup()


if __name__ == "__main__":
    main()
