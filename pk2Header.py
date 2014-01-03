from struct import *
class pk2Header(object):
    """description of class"""
    def __init__(self, block):
        unpacked = unpack("<30s4sB16s205s",block)
        self.name = unpacked[0]
        self.version = unpacked[1]
        self.encryption = unpacked[2]
        self.verfiy = unpacked[3]
        self.reserved = unpacked[4]
        if self.encryption != 1:
            print("Invalid .pk2 File!")
            exit()
