# mansikka data
import random  # noqa: F401
import datetime
import sys  # noqa: F401
import csv
import os
# illegal aliens
try:
    from .main import arguments
except ImportError:
    from main import arguments

def xdg_data_dir():
    if arguments.config:
        path = arguments.config
    else:
        path = "~/.local/share"
    datadir = os.path.join(
        os.getenv('XDG_DATA_HOME',
                  os.path.expanduser(path)),
        "scale_inator")
    if not os.path.isdir(datadir):
        os.mkdir(datadir)
    return datadir


def get_collectorID(koppaID):
    '''
    Calculates collector from ID
    '''
    return ((koppaID-1)//20)+1


def get_csv_name():
    return ("data-{}.csv".format(datetime.datetime.now().strftime("%Y%m%d")))


def dataHandler(weight, currentID, collector):
    date = datetime.datetime.now()
    date = date.strftime("%d.%m.%Y")

    f = open(os.path.join(xdg_data_dir(), get_csv_name()), "a",  newline="")

    writer = csv.writer(f)
    info = (weight, currentID, collector, date)
    writer.writerow(info)
    f.close()


def undo():  # needs testing
    try:
        print("Undo in progress...")
        f1 = open(
            os.path.join(
                xdg_data_dir(),
                get_csv_name()
            ),
            "r",
            newline=""
        )
        lines = f1.readlines()  # get rows into list
        lastRow = lines.pop()  # removes last row -> lastRow var
        f1.close()
        # open with write
        f2 = open(
            os.path.join(
                xdg_data_dir(),
                get_csv_name()),
            "w",
            newline=""
        )
        f2.writelines(lines)
        f2.close()
        # rewrite done
        print("Last row successfully removed:\n", lastRow)
    except OSError or IndexError:
        print("Nothing to undo.\n")


def total():
    print("Calculate total not ready.\n")


def cloudBackup():  # backup to GDrive or blank github repo? github with bash.
    print("Cloud backup not ready.\n")


'''
NOTES:
 change filename to date
 data.csv name not optimal? daily new data.
'''

# total()
# dataHandler(1,12,1)
