class pk2Entry(object):
    """description of class"""
    def __init__(self, unpacked):
        self.type = unpacked[0]
        self.name = unpacked[1]
        self.fixName()
        self.accessTime = unpacked[2]
        self.createTime = unpacked[3]
        self.modifyTime = unpacked[4]
        self.position = unpacked[5]
        self.size = unpacked[6]
        self.nextChain = unpacked[7]

    def fixName(self): 
        index = 0
        for c in self.name:
            if c != '\0':
                index += 1
            else:
                break
        self.name = self.name[:index]