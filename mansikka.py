###################
#### main file ####
###################
import UI, data #only works with aliohjelmas
#illegal goods import
import serial, datetime, sys

#serial init
ser = serial.Serial(
    port='COM5',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

#serial read
weight = ser.readline()
#serial close
ser.close()
