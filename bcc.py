#! /usr/bin/python3
"""
Block Check Character
"""

def bcc(s):
    b = 0x00
    for i in range(0, len(s), 2):
        b = b ^ int(s[i:i+2], 16)
    return hex(b)
