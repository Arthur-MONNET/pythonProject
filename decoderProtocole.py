class DecoderProtocole:
    def __init__(self, string):
        self.string = string
    
    def decodeData(self):
        split = self.string.split(":")
        self.typeVal = split[0].split(".")[0]
        self.name = split[0].split(".")[1]
        self.keyValues = list(map(lambda x: x.split(">"), split[1].split(";")))

class ConnectionDecoderProtocole:
    def __init__(self, string):
        self.string = string
    
    def decodeData(self):
        split = self.string.split(":")
        self.typeVal = split[1].split(".")[0]
        self.name = split[1].split(".")[1]
        
        