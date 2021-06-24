###################
#### main file ####
###################
#import UI, data           #only works with aliohjelmas
#illegal goods import
import serial, datetime, sys, random
import time

def serRep(): #replaces serial input for demo
    return round(random.uniform(1,6), 2)

## MAIN
def main():
    #serial init
    """ser = serial.Serial(
        port='/dev/ttyUSB0',\
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=0)"""
    prevID = None

    try:#while loop failure handling
        while(1):
            try: #scanning failure handling
                currentID = input("SCAN ID, Q to exit and save: ")
                #safe quit
                if currentID == "q":
                    print("Saving...")
                    #file close
                    #serial close
                    """ser.close()"""
                    break
                #no quit
                else: #convert id to int
                    currentID=int(currentID)
            #scan fails:
            except:
                print("SCAN FAILED")
                continue
            time.sleep(0.2)#enhances reading clarity

            #serial read weight on scale
            """weight = ser.readline()"""
            weight = serRep() #read "serial"
            ##ID processing
            if currentID == prevID: # scam prevention, check same persons all baskets pls
                print("SAME AS PREVIOUS,\nNOT ACCEPTED.")
                continue

            #prints & collector
            collector = ((currentID-1)//20)+1 #calculates collector from ID
            print("#",str(collector)+",","SUCCESSFULLY SAVED", weight, "kg")
            #csv write weight+ID same row different columns
            prevID = currentID

    except: #save closing with file & serial
        print("Unexpected error:", sys.exc_info()[0])
        print("Program failed, closing and saving...")
        #file close
        #serial close
        """ser.close()"""
        sys.exit(-1)

if __name__ == "__main__":
    main()
