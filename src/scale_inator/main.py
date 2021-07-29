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


class SerialPretend:
    '''
    Serial like weight generator, Replaces serial input for demo
    '''
    def __init__(self):
        return None

    def readline(self):
        return ("ST,G    " +
                str(round(random.uniform(10, 60), 2)) +
                "0000kg").encode("utf8")

    def close(self):
        return True


def cleanup():
    '''
    Close file gracefully
    '''
    print("Cleaning up")
    # file close


def arg_parser(args):
    parser = ArgumentParser()
    parser.add_argument("-p", "--pretend", action="count",
                        help="Use dummy data instead of reading from serial")
    parser.add_argument("--gui", action="count",
                        help="Show GUI (REQUIRES TK)")
    parser.add_argument("--config", help="dd")
    return parser.parse_args()


# remove barcode zeros, failsafe maybe add later?
def zeroremove(string):
    if string[0] == "0":
        return zeroremove(string[1:])
    else:
        return string


def createWindowUIwrap(ifsuccess, collector, weight):
    if arguments.gui:
        try:
            from .UI import createWindow
        except ImportError:
            from UI import createWindow
        createWindow(ifsuccess, collector, weight)


def readscale():
    while 1:  # fix this with pretend later maybe?
        # ser needs to be set everytime before reading it to get value
        if not arguments.pretend:
            ser = serial.Serial(
                port='/dev/ttyUSB0',
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        else:
            ser = SerialPretend()
        weight = ser.readline().decode('ascii')
        if len(weight) < 17:
            continue
        else:
            break
    ser.close()
    return weight


def readinput():
    try:
        from . import data
    except ImportError:
        import data

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
                currentID = int(zeroremove(currentID))

        except ValueError:
            print("Invalid input, try again.")
            continue
        # read weight from scale
        weight = readscale()
        if "-" in weight:
            print("negative value not accepted.")
            continue
        # cut "ST,G    x.xxKG"
        weight = weight[8:-2]  # cut 8 first("ST,G    "), and 2 last(kg)
        # kg still appears in data.csv? it cant calculate total with letters
        # ID processing # scam prevention, check same persons all baskets pls
        if currentID == previousID:
            print("SAME AS PREVIOUS,\nNOT ACCEPTED.")
            createWindowUIwrap(False, 0, 0)
            continue
        # prints & collector
        collector = data.get_collectorID(currentID)
        # try save
        try:
            data.dataHandler(weight, currentID, collector)
            print("#%s, SUCCESSFULLY SAVED %s" % (collector, weight))
            createWindowUIwrap(True, collector, weight)
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
    global arguments
    arguments = arg_parser(sys.argv[1:])

    atexit.register(cleanup)

    readinput()


if __name__ == "__main__":
    main()
