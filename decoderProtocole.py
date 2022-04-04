class DecoderProtocole:
    def __init__(self, string):
        self.string = string
    
    def decodeData(self):
        split = self.string.split(":")
        self.typeVal = split[0]
        self.valueTab = split[1].split(";")
        """if(splitVal == 'button'):
            self.buttonVal()
        elif(splitVal == 'temp'):
            self.tempVal()
    
    def buttonVal(self):
        if(self.valueTab[0]):
            self.value = True
        else:
            self.value = False
    
    def tempVal(self):
        for val in self.valueTab:
            self.value = """