from sroBlowfish import sroBlowfish
from pk2Entry import pk2Entry
from pk2Header import pk2Header
from struct import *
class pk2Reader(object):
    """description of class"""
    def __init__(self, filename):
        try:
            self.file = open(filename,"rb")
            self.entries = []
            bKey = [0x32, 0xCE, 0xDD, 0x7C, 0xBC, 0xA8] #Key used for blowfish encryption. May be different for other versions.
            self.blowfish = sroBlowfish()
            self.blowfish.Initilize(bKey, 0, 6)
            self.readHeader() #Read the header and check if it is a valid .pk2 File
            self.read(256) #Start reading at the end of the Header
        except IOError as e:
            print("{0} : {1}".format(filename,e.strerror))

    def readHeader(self):
        try:
            self.header = pk2Header(self.file.read(256))
        except IOError as e:
            print(e.strerror)

    def close(self):
        self.file.close()

    def changeDirectory(self, dir):
        for entry in self.entries:
            if entry.name == dir and entry.type == 1: #Type 1 = Directory Type 2 = File 
                self.entries = [] #clear current directory
                self.read(entry.position)
                print("Changed Directory to '{0}'. Use ls to see all files and directories".format(entry.name))
                return
        print("Directory {0} not found.".format(dir))

    def extractFile(self, filename):
        for entry in self.entries:
            if entry.name == filename and entry.type == 2: #Type 1 = Directory, Type 2 = File 
                outputFile = open(entry.name,"wb")
                self.file.seek(entry.position)
                outputFile.write(self.file.read(entry.size))
                outputFile.close()
                print("File: {0} with size: {1} bytes extracted".format(entry.name,entry.size))
                return
        print("File {0} not found".format(filename))

    def ls(self):
        for entry in self.entries:
            if entry.type == 1:
               print("[{0}]".format(entry.name))
            else: 
               print(entry.name)

    def read(self, offset):
        tmpentries = self.getEntries(self.readEntryBlock(offset))
        for e in tmpentries:
            if e.type != 0: # type 0 = Null Entry. 
                self.entries.append(e)
        if tmpentries[19].nextChain != 0: #If more than 20 entries are in the current Directory then the nextChain attribute of the last Entry is the address of the next EntryBlock.
            self.read(tmpentries[19].nextChain)

    def getEntries(self, block):
        entries = []
        for i in range(20):
            unpacked = unpack("<B81sQQQQIQH",block[128 * i : 128 * (i + 1)]) #
            entries.append(pk2Entry(unpacked))
        return entries

    def readEntryBlock(self, offset):
        try:
            self.file.seek(offset)
            pk2EntryBlock = self.file.read(2560)
            decodedBlock = self.blowfish.Decode(pk2EntryBlock,0,2560) #Decode the blowfish encrypted EntryBlock
            return decodedBlock
        except IOError as e:
            print(e.strerror)
            exit()
