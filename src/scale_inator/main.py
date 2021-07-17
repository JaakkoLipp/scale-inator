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
    from . import data
except ImportError:
    import data


class SerialPretend:
    '''
    Serial like weight generator, Replaces serial input for demo
    '''
    def __init__(self):
        return None

    def readline(self):
        return str(round(random.uniform(10, 60), 2)).encode("utf8")

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
    parser.add_argument("--gui", action="count",
                        help="Show GUI (REQUIRES TK)")
    return parser.parse_args()


def setup_serial(arguments):
    global ser
    if not arguments.pretend:
        # serial init
        #19200 9600 4800 2400 1200 are possible baudrates
        ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)
    else:
        ser = SerialPretend()


def createWindowUIwrap(arguments, ifsuccess, collector, weight):
    if arguments.gui:
        try:
            from .UI import createWindow
        except ImportError:
            from UI import createWindow
        createWindow(ifsuccess, collector, weight)


def readinput(arguments):
    # set variable for id
    previousID = None

    while (True):
        currentID = input(
            "Scan ID, Q to exit, to remove last write \"undo\": "
        )
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
        ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)
        while 1:
            weight = ser.readline().decode('ascii')
            if "-" in weight:
                print("negative value not accepted.")
                continue
            if len(weight) < 17:
                continue
            else:
                break
        ser.close()
        # cut "ST,G    x.xxKG"
        weight=weight[8:-2] # cut 8 first("ST,G    "), and 2 last(kg)
        # ID processing # scam prevention, check same persons all baskets pls
        if currentID == previousID:
            print("SAME AS PREVIOUS,\nNOT ACCEPTED.")
            createWindowUIwrap(arguments, False, 0, 0)
            continue
        # prints & collector
        collector = data.get_collectorID(currentID)
        # try save
        try:
            data.dataHandler(weight, currentID, collector)
            print("#%s, SUCCESSFULLY SAVED %s" % (collector, weight))
            createWindowUIwrap(arguments, True, collector, weight)
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
