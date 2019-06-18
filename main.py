import serial

from com import *

# open pump serial
pump = serial.Serial()
pump.baudrate = 9600
pump.port = '/dev/cu.usbserial'
pump.parity = serial.PARITY_EVEN
pump.stopbits = serial.STOPBITS_ONE
pump.open()

addr = "01"

# standard message
start = "e901044357580148"
stop = "e901044357580049"
read_flow = 'e9010643525442'
read_syringe = 'e9010343524457'