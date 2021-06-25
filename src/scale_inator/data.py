# mansikka data
import random  # noqa: F401
import datetime
import sys  # noqa: F401
import csv
import os
# illegal aliens


def xdg_data_dir():
    datadir = os.path.join(
        os.getenv('XDG_DATA_HOME',
                  os.path.expanduser("~/.local/share")),
        "scale_inator")
    if not os.path.isdir(datadir):
        os.mkdir(datadir)
    return datadir


def dataHandler(weight, currentID, collector):
    date = datetime.datetime.now()
    filename = ("data-{}.csv".format(date.strftime("%Y%m%d")))
    date = date.strftime("%d.%m.%Y")

    f = open(os.path.join(xdg_data_dir(), filename), "a",  newline="")

    writer = csv.writer(f)
    info = (weight, currentID, collector, date)
    writer.writerow(info)
    f.close()


def totalSorter():
    print("oof")


'''
NOTES:
 change filename to date
 data.csv name not optimal? daily new data.
'''

# totalSorter()
# dataHandler(1,12,1)
