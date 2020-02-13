#
# cycle_power.py
# author: Kevin Gates
#
# Meant to cycle power every hour on the
# Agilent E3643A Power supply over RS232
# Run in Parallel to Qt Program QtCSTARS1Connect_v3
# to get past the timeout error
#

import visa
import time
from os import walk


#--------------------
#
# Parameters
#
#--------------------

AWAKE_TIME = 90*60 #1*60*60 #seconds
SLEEP_TIME = 20#30 #seconds
DATA_PATH = '/home/cstars1/Documents/cstars_data_bin'


#--------------------
#
# Functions
#
#--------------------

# Checks to see if Qt program is currently writing files
# to the data directory
def data_bin_open():
    f1 = []  
    for (dirpath, dirnames, filenames) in walk(DATA_PATH):
        f1.extend(filenames)
        break

    time.sleep(5)
    f2 = []  
    for (dirpath, dirnames, filenames) in walk(DATA_PATH):
        f2.extend(filenames)
        break

    if len(f1) == len(f2):
        return True
    else:
        print round(time.time() - start_time,2), ":                   ERR - Data Bin Open, will wait"
        return False

#--------------------
#
# Script
#
#--------------------


rm = visa.ResourceManager('@py')
#print(rm.list_resources()) #Lists resources, assuming device on ttyUSB2

#Opens Device and desplays identification to verify the proper device
psupply = rm.open_resource('ASRL/dev/ttyUSB2::INSTR')
print(psupply.query('*IDN?'))


#Sets initial Pssuply values
psupply.write('*RST')
psupply.write('System:Remote')
psupply.write('Output OFF')
psupply.write('Volt 12.0')
psupply.write('Current 1.0')


print "Press Cntrl-C at any time to exit...\n"
counter = 1
start_time = time.time()
try:
    while 1:
        psupply.write('Output ON')
        print round(time.time() - start_time,2), ":                   turning ON  #" ,counter
        time.sleep(AWAKE_TIME)
        
        while(not data_bin_open()):
            time.sleep(10)
        
        psupply.write('Output OFF')
        print round(time.time() - start_time,2), ":                   turning OFF #" ,counter
        time.sleep(SLEEP_TIME)

        counter = counter + 1

except KeyboardInterrupt:
    pass


psupply.write('Output OFF')
psupply.close()
print "\nGoodbye friendo, I hope you got your data!\n\n"
