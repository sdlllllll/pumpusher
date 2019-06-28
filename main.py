"""
Pumpusher
Programing control LSP longerpump. Input config file name, program
will automatic check config feasibility and run after press [ENTER].
Config file should write as [config_template.csv].

Version: 1.0
"""

import serial

import time
import csv


def ex(s):
    return s[2:4]+s[0:2]


def bcc(s):
    b = 0x00
    for i in range(0, len(s), 2):
        b = b ^ int(s[i:i+2], 16)
    return '{:02x}'.format(b)


def send(s):
    global pump
    for i in range(0, len(s), 2):
        pump.write(bytes.fromhex(s[i:i+2]))
        time.sleep(0.005)
    time.sleep(0.1)


def receive():
    time.sleep(0.1)
    return_message = pump.read_all()
    return_message = return_message.replace(b'\xe8\x01',b'\xe9').replace(b'\xe8\x00',b'\xe8')
    return return_message


def set_syringe(comp, volume, ):
    CWD = "435744"
    channel4 = 49152
    if comp == "custom":
        mode_code = "55"
        if 1 <= int(volume) <= 5000:
            arguments_code = ex("{:04x}".format(int(volume)+channel4))
        else:
            print("[Error] wrong volume arguments.")
            return 1
    elif comp == "BD":
        mode_code = "4d"    # M
        if volume == "0.5ml_plastic":
            arguments_code = "4201"     # B1
        elif volume == "1ml_glass":
            arguments_code = "4302"     # C2
        else:
            return 2
    else:
        print("[Error] wrong company arguments.")
        return 3
    return CWD+mode_code+arguments_code


def set_flow(volume, volume_unit, flow, flow_unit):
    CWT1 = "43575401"
    if 0 <= int(volume) <= 9999:
        volume_code = ex('{:04x}'.format(int(volume)))
    else:
        return 1
    if volume_unit == '0.001ul':
        volume_unit_code = '01'
    elif volume_unit == '0.01ul':
        volume_unit_code = '02'
    elif volume_unit == '0.1ul':
        volume_unit_code = '03'
    elif volume_unit == '1ul':
        volume_unit_code = '04'
    elif volume_unit == '0.01ml':
        volume_unit_code = '05'
    elif volume_unit == '0.1ml':
        volume_unit_code = '06'
    elif volume_unit == '1ml':
        volume_unit_code = '07'
    else:
        return 2
    if 1 <= int(flow) <= 9999:
        flow_code = ex('{:04x}'.format(int(flow)))
    else:
        return 3
    if flow_unit == '0.001ul/h':
        flow_unit_code = '01'
    elif flow_unit == '0.01ul/h':
        flow_unit_code = '02'
    elif flow_unit == '0.1ul/h':
        flow_unit_code = '03'
    elif flow_unit == '1ul/h':
        flow_unit_code = '04'
    elif flow_unit == '0.001ul/min':
        flow_unit_code = '05'
    elif flow_unit == '0.01ul/min':
        flow_unit_code = '06'
    elif flow_unit == '0.1ul/min':
        flow_unit_code = '07'
    elif flow_unit == '1ul/min':
        flow_unit_code = '08'
    elif flow_unit == '0.01ml/h':
        flow_unit_code = '09'
    elif flow_unit == '0.1ml/h':
        flow_unit_code = '0a'
    elif flow_unit == '1ml/h':
        flow_unit_code = '0b'
    elif flow_unit == '0.01ml/min':
        flow_unit_code = '0c'
    elif flow_unit == '0.1ml/min':
        flow_unit_code = '0d'
    elif flow_unit == '1ml/min':
        flow_unit_code = '0e'
    else:
        return 4
    return CWT1+volume_code+volume_unit_code+flow_code+flow_unit_code


def make_message(addr, pdu):
    newpdu = ''
    pdulist = []
    for i in range(0, len(pdu), 2):
        pdulist.append(pdu[i:i + 2])
    for i in pdulist:
        if i == 'e8':
            newpdu = newpdu + i + '00'
        if i == 'e9':
            newpdu = newpdu + 'e8' + '01'
        else:
            newpdu = newpdu + i
    l = '{:02x}'.format(int(len(newpdu)/2))
    body = addr + l + newpdu
    bcccheck = bcc(body)
    return 'e9'+body+bcccheck


# open pump serial
pump = serial.Serial()
pump.baudrate = 9600
pump.port = '/dev/cu.usbserial'     # fit port to your system
pump.parity = serial.PARITY_EVEN
pump.stopbits = serial.STOPBITS_ONE
pump.open()

addr = "01"

# standard message
start = "e901044357580148"
stop = "e901044357580049"
read_flow = 'e9010343525447'
read_syringe = 'e9010343524457'
yes = b'\xe9\x01\x01YY'

csv_name = input("Please input config csv name:")
with open(csv_name) as f:
    f_csv = csv.reader(f)
    head = next(f_csv)
    if not head == ['syringe ID(0.01mm)', 'flow', 'flow unit', 'flow time(s)', 'stop time(s)']:
        print('Head line wrong, please check config file.')
        exit()
    line_number = 0
    for row in f_csv:
        line_number = line_number + 1
        send(make_message(addr, set_syringe('custom', row[0])))
        if receive() == yes:
            send(read_syringe)
            check_tmp = receive()[6:8]
            if not check_tmp == bytes.fromhex(set_syringe('custom', row[0]))[4:6]:
                print('Cannot set syringe ID at {}.'.format(line_number))
                exit()
        send(make_message(addr, set_flow(0, '1ml', row[1], row[2])))
        if receive() == yes:
            send(read_flow)
            check_tmp = receive()[6:12]
            if not bytes.fromhex(set_flow(0,'1ml',row[1],row[2]))[4:10] == check_tmp:
                print('Cannot set flow at {}.'.format(line_number))
                exit()
    f.seek(0.0)
    print('Config file is OK.')
    input('Press [ENTER] start program.')
    head = next(f_csv)
    for row in f_csv:
        send(make_message(addr,set_syringe('custom',row[0])))
        print("Set syringe ID as {} mm.".format(int(row[0])*0.01))
        send(make_message(addr,set_flow(0,'1ml',row[1],row[2])))
        print("Set flow as {} {}.".format(row[1],row[2]))
        send(start)
        print("Start push for {} min.".format(eval(row[3])/60))
        time.sleep(eval(row[3]))
        send(stop)
        print("Stop flow for {} min.".format(eval(row[4])/60))
        time.sleep(eval(row[4]))
print('Program finished.')
print('Press [ENTER] quit.')
exit()
