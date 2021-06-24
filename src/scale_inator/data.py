# mansikka data
import random
import datetime
import sys
import csv
#illegal aliens

def dataHandler(weight,currentID,collector):
    date = datetime.datetime.now()
    date=date.strftime("%d.%m.%Y")

    f = open("data.csv", "a",  newline="")

    writer = csv.writer(f)
    info=(weight,currentID,collector,date)
    writer.writerow(info)
    f.close()

def totalSorter():
    print("oof")




"""notes"""
    #change filename to date
    #data.csv name not optimal? daily new data.


# totalSorter()
#dataHandler(1,12,1)
