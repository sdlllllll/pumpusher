"""
Pumpusher
Programing control LSP longerpump. Input config file name, program
will automatic check config feasibility and run after press [ENTER].
Config file should write as [config_template.csv].

Version: 2.1
"""
import threading
import time
import csv

import serial


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
    pdu = return_message.hex()
    pdu = pdu[6:-2]
    return pdu


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


def make_message(a, pdu):
    newpdu = ''
    pdulist = []
    for i in range(0, len(pdu), 2):
        pdulist.append(pdu[i:i + 2])
    for i in pdulist:
        if i == 'e8':
            newpdu = newpdu + i + '00'
        elif i == 'e9':
            newpdu = newpdu + 'e8' + '01'
        else:
            newpdu = newpdu + i
    l = '{:02x}'.format(int(len(pdulist)))
    addr = '{:02x}'.format(int(a))
    body = addr + l + newpdu
    bcccheck = bcc(body)
    return 'e9'+body+bcccheck


def pump_start(addr, pdu):
    send(make_message(addr, pdu))
    send(make_message(addr, start))
    print(time.asctime(time.localtime(time.time())))
    print(pdu)


# open pump serial
pump = serial.Serial()
pump.baudrate = 9600
pump.port = '/dev/cu.usbserial'     # fit port to your system
pump.parity = serial.PARITY_EVEN
pump.stopbits = serial.STOPBITS_ONE
pump.open()

# standard message
start = "43575801"
stop = "43575800"
read_flow = '435254'
read_syringe = '435244'
yes = '59'

csv_name = input("Please input config csv name:")
# csv_name = 'config2.csv'
with open(csv_name) as f:
    f_csv = csv.reader(f)
    body = []
    i = 0
    for row in f_csv:
        body.append([])
        body[i] = []
        for colum in row:
            body[i].append(colum)
        i +=1
    for step in body:
        i = 0
        j = 1
        for argument in step:
            if i == 0:
                pass
            if i == 1:
                addr = argument
            if i == 2:
                if argument == 'start':
                    flag = True
                elif argument == 'stop':
                    flag = False
                else:
                    print('Parameter error at {}, {}.'.format(j,i))
                    exit()
            if i == 3:
                flow_rate = argument
            if i == 4:
                flow_unit = argument
            i += 1
        if flag:
            send(make_message(addr, set_flow(0, '1ml', flow_rate, flow_unit)))
            receive_tmp = receive()
            if receive_tmp == yes:
                send(make_message(addr, read_flow))
                receive_tmp = receive()
                if not receive_tmp[6:18] == set_flow(0, '1ml', flow_rate, flow_unit)[8:20]:
                    print('Cannot set flow rate at line {}.'.format(j))
                    exit()
            else:
                print('Unknown error.')
                exit()
            time.sleep(1)
        j += 1
    print('Config file is OK.')
    input('Press [ENTER] start program.')
    for step in body:
        i = 0
        for argument in step:
            if i == 0:
                step_time = eval(argument)
            if i == 1:
                addr = argument
            if i == 2:
                if argument == 'start':
                    flag = True
                elif argument == 'stop':
                    flag = False
                else:
                    print('Parameter error at {}, {}.'.format(j,i))
                    exit()
            if i == 3:
                flow_rate = argument
            if i == 4:
                flow_unit = argument
            i += 1
        if flag:
            s = threading.Timer(step_time, pump_start, args=(addr, set_flow(0,'1ml',flow_rate,flow_unit),))
            s.start()
        elif not flag:
            s = threading.Timer(step_time, send, args=(make_message(addr, stop),))
            s.start()

    print('Wait for all pump.')
    s.join()
print('Program finished.')
input('Press [ENTER] quit.')
exit()
