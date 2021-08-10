import random  # noqa: F401
import datetime
import sys  # noqa: F401
import csv
import os

try:
    from .main import arguments
except ImportError:
    try:
        from main import arguments
    except ImportError:
        # Scuffed problems require scuffed solutions
        class ArgsPretend:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)
        arguments = ArgsPretend(gui=0, pretend=1, savedir=None)


def xdg_data_dir():
    '''
    Was once a proper xdg compliant function, not anymore, sadge moment
    '''
    if arguments.savedir:
        path = arguments.savedir
    else:
        path = os.getenv('XDG_DATA_HOME',
                         os.path.expanduser("~/.local/share/scale_inator"))
    datadir = path
    if not os.path.isdir(datadir):
        os.mkdir(datadir)
    return datadir


def get_collectorID(koppaID):
    '''
    Calculates collector from ID
    '''
    return ((koppaID-1)//20)+1


def get_csv_name():
    '''
    Returns a csv name with current date included
    '''
    return ("data-{}.csv".format(datetime.datetime.now().strftime("%Y%m%d")))


def dataHandler(weight, currentID, collector):
    '''
    Append data to csv
    '''
    date = datetime.datetime.now()
    date = date.strftime("%d.%m.%Y")

    file = open(os.path.join(xdg_data_dir(), get_csv_name()), "a",  newline="")

    writer = csv.writer(file)
    info = (weight, currentID, collector, date)
    writer.writerow(info)
    file.close()


# TODO: needs testing
def undo():
    '''
    Undo last row
    '''
    try:
        print("Undo in progress...")

        # First read all lines into variable then pop last element from that
        # and write it to the file.
        read_file = open(
            os.path.join(
                xdg_data_dir(),
                get_csv_name()
            ),
            "r",
            newline=""
        )

        lines = read_file.readlines()
        lastRow = lines.pop()

        read_file.close()

        write_file = open(
            os.path.join(
                xdg_data_dir(),
                get_csv_name()),
            "w",
            newline=""
        )

        write_file.writelines(lines)

        write_file.close()

        print("Last row successfully removed:\n", lastRow)
    except OSError or IndexError:
        print("Nothing to undo.\n")


# TODO: what is purpose?
def total():
    print("Calculate total not ready.\n")


# TODO: backup to GDrive or blank github repo? github with bash.
def cloudBackup():
    print("Cloud backup not ready.\n")
