import time


def send(s):
    for i in range(0, len(s), 2):
        pump.write(bytes.fromhex(s[i:i+2]))
        time.sleep(0.005)


def receive():
    return_message = pump.read_all()
    return return_message


def check(expect_message):
    return_message = pump.read_all()
    if return_message == expect_message:
        return True


def set_syringe(comp, volume):
    CWD = "435744"
    if comp == "custom":
        mode_code = "55"
        if 1 <= int(volume) <= 5000:
            arguments_code = volume
        else:
            print("[Error] wrong volume arguments.")
    else:
        print("[Error] wrong company arguments.")
        return
    return CWD+mode_code+arguments_code


def set_flow(volume, volume_unit, flow, flow_unit):
    CWT1 = "43575401"
    if 0 <= int(volume) <= 9999:
        volume_code = '{:04d}'.format(int(volume))
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
        flow_code = '{:04d}'.format(int(flow))
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
    elif flow_unit == '0.001ul/m':
        flow_unit_code = '05'
    elif flow_unit == '0.01ul/m':
        flow_unit_code = '06'
    elif flow_unit == '0.1ul/m':
        flow_unit_code = '07'
    elif flow_unit == '1ul/m':
        flow_unit_code = '08'
    elif flow_unit == '0.01ml/h':
        flow_unit_code = '09'
    elif flow_unit == '0.1ml/h':
        flow_unit_code = '0a'
    elif flow_unit == '1ml/h':
        flow_unit_code = '0b'
    elif flow_unit == '0.01ml/m':
        flow_unit_code = '0c'
    elif flow_unit == '0.1ml/m':
        flow_unit_code = '0d'
    elif flow_unit == '1ml/m':
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
        else:
            newpdu = newpdu + i
    l = '{:02x}'.format(int(len(newpdu)/2))
    body = addr + l + newpdu
    bcccheck = bcc.bcc(body)
    return 'e9'+body+bcccheck

