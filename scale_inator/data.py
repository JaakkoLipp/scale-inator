# mansikka data
import random
import datetime
import sys
import csv
#illegal aliens

def dataHandler(weight,currentID,collector):
    date = datetime.datetime.now()
    date=date.strftime("%d.%m.%Y")
    #change filename to date
    f = open("data.csv", "a",  newline="")
    #this not sustainable
    writer = csv.writer(f)
    info=(weight,currentID,collector,date)
    writer.writerow(tup)
    f.close()

def totalSorter():
    print("oof")



# totalSorter()
# dataHandler(1,12,1)
