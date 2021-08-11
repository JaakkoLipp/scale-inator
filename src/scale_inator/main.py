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
'''


class SerialPretend:
    '''
    Dummy class to act like serial output from scale
    '''
    def __init__(self):
        return None

    def readline(self):
        from random import uniform
        return ("ST,G    " +
                str(round(uniform(10, 60), 3)) +
                "0KG").encode("utf8")

    def close(self):
        return True


def arg_parser(args):
    '''
    Argument parsing related code
    (possible redundant to be separated from main())
    '''
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-p", "--pretend", action="count",
                        help="Use dummy data instead of reading from serial")
    parser.add_argument("--gui", action="count",
                        help="Show GUI (REQUIRES TK)")
    parser.add_argument("--savedir",
                        help="Location where data saved")
    parser.add_argument("--xlsxgen", action="count",
                        help="Generate xlsx from data")
    return parser.parse_args()


def zeroremove(string):
    '''
    Remove leading zeros from barcode input
    '''
    if type(string) != str:
        raise TypeError("Only string input is accepted")
    if len(string) < 1:
        return ""

    def zeroremove_inner(string):
        '''
        Workhorse function which is free from preliminary error checking
        '''
        if string[0] == "0":
            return zeroremove_inner(string[1:])
        else:
            return string

    return zeroremove_inner(string)


def createWindowUIwrap(ifsuccess, collector, weight):
    '''
    Wrapper function for showing success/fail window depending on cmd argument
    '''
    if arguments.gui:
        try:
            from .UI import createWindow
        except ImportError:
            from UI import createWindow
        createWindow(ifsuccess, collector, weight)


def readscale():
    '''
    Loop which reads and returns output from serial on the caveat that it first
    checks if its corrupted or not lazily
    '''
    # TODO: fix this with pretend later maybe?
    while (True):
        if not arguments.pretend:
            from serial import Serial, PARITY_NONE, STOPBITS_ONE, EIGHTBITS
            # serial_output needs to be set everytime
            serial_output = Serial(
                port='/dev/ttyUSB0',
                baudrate=9600,
                parity=PARITY_NONE,
                stopbits=STOPBITS_ONE,
                bytesize=EIGHTBITS,
                timeout=1)
        else:
            serial_output = SerialPretend()

        weight = serial_output.readline().decode('ascii')

        # Cheap corruption check
        if len(weight) == 16:  # arbitary length that seems to work
            continue
        else:
            break

    serial_output.close()
    return weight


def readinput(optarg=None):
    try:
        from . import data
    except ImportError:
        import data

    # let optargs work without arguments in global scope
    # this is so that tests work
    if optarg:
        global arguments
        arguments = optarg

    previousID = None

    while (True):
        currentID = input(
            "Scan ID, Q to exit, to remove last write \"undo\": "
        )

        # User input / barcode reader input handling
        try:
            if currentID.upper() == "Q":
                print("Quitting...")
                break
            elif currentID.lower() == "undo":
                data.undo()
                continue
            else:
                currentID = int(zeroremove(currentID))
        except ValueError:
            print("Invalid input, try again.")
            continue

        # Read weight from scale
        weight = readscale()

        if "-" in weight:
            print("negative value not accepted.")
            continue

        # TODO: kg still appears in data.csv?
        # cut 8 first("ST,G    "), and 2 last(kg)
        weight = weight[8:-2]

        if currentID == previousID:
            print("SAME AS PREVIOUS,\nNOT ACCEPTED.")
            createWindowUIwrap(False, 0, 0)
            continue

        collector = data.get_collectorID(currentID)

        try:
            data.dataHandler(weight, currentID, collector)
            print("#%s, SUCCESSFULLY SAVED %s" % (collector, weight))
            createWindowUIwrap(True, collector, weight)
        except OSError:
            from inspect import currentframe, getframeinfo
            print("saving failed! line %s" %
                  getframeinfo(currentframe()).lineno)
        previousID = currentID


def main():
    '''
    Main function
    '''
    from sys import argv

    global arguments
    arguments = arg_parser(argv[1:])

    if not arguments.xlsxgen:
        readinput()
    else:
        try:
            from .xlsx import create_xlsx
        except ImportError:
            from xlsx import create_xlsx
        create_xlsx()


if __name__ == "__main__":
    main()
