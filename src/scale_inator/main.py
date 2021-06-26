'''
   ###  ###
    ######
  ###########
 ##############
 ## Mansikka ##
 ##############
 ##############
  ############
   ##########
    ########
     #####
      ###

https://cdn.discordapp.com/attachments/624244854754377758/857616413937106954/unknown.png
'''

from argparse import ArgumentParser
from inspect import currentframe, getframeinfo
# import datetime
import atexit
import random
import serial
import sys
# import time
try:
    from . import UI
    from . import data
except ImportError:
    import UI
    import data


class SerialPretend:
    '''
    Serial like weight generator, Replaces serial input for demo
    '''
    def __init__(self):
        return None

    def readline(self):
        return round(random.uniform(10, 60), 2)

    def close(self):
        print("Closed successfully")


def cleanup():
    '''
    Close serial and file gracefully
    '''
    print("Cleaning up")
    ser.close()
    # file close


def arg_parser(args):
    parser = ArgumentParser()
    parser.add_argument("-p", "--pretend", action="count",
                        help="Use dummy data instead of reading from serial")
    parser.add_argument("--no-gui", action="count",
                        help="Do not show GUI")
    return parser.parse_args()


def setup_serial(arguments):
    global ser
    if not arguments.pretend:
        # serial init
        ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            #parity=serial.PARITY_NONE,
            #stopbits=serial.STOPBITS_ONE,
            #bytesize=serial.EIGHTBITS,
            timeout=1)
    else:
        ser = SerialPretend()


def readinput(arguments):
    # set variable for id
    previousID = None


    while (True):
        currentID = input("Scan ID, Q to exit, \"undo\" to remove last write: ")
        try:
            if currentID.upper() == "Q":
                print("Quitting...")
                break
                # no quit
            elif currentID.lower() == "undo":
                data.undo()  # remove last line incase of wrong data
                continue
            else:
                # convert id to int
                currentID = int(currentID)
        except ValueError:
            print("Invalid input, try again.")
            continue
        # read weight from scale
        weight = ser.readline().decode('ascii')
        # ID processing # scam prevention, check same persons all baskets pls
        if currentID == previousID:
            print("SAME AS PREVIOUS,\nNOT ACCEPTED.")
            if not arguments.no_gui:
                UI.createWindow(False, 0, 0)
            continue
        # prints & collector
        collector = ((currentID-1)//20)+1  # calculates collector from ID
        # try save
        try:
            data.dataHandler(weight, currentID, collector)
            print("#%s, SUCCESSFULLY SAVED %skg" % (collector, weight))
            if not arguments.no_gui:
                UI.createWindow(True, collector, weight)
        # save fails:
        except OSError:
            print("saving failed! line %s" %
                  getframeinfo(currentframe()).lineno)
        # csv write weight+ID same row different columns
        previousID = currentID


def main():
    '''
    Main function
    '''

    # Argument parsing
    arguments = arg_parser(sys.argv[1:])

    atexit.register(cleanup)

    setup_serial(arguments)

    readinput(arguments)


if __name__ == "__main__":
    main()
