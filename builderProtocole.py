#typeData.name:prop>num;prop>num;
class BuilderProtocole:
    def __init__(self,typeData,name,keyValues):
        self.typeData = typeData
        self.name = name
        self.keyValues = keyValues
    def build(self):
        string = self.typeData + "." + self.name + ":"
        mult = False
        if(len(self.keyValues)>1):
            mult = True
        for keyVal in self.keyValues:
            string += keyVal[0] + ">" + str(keyVal[1])
            if(mult):
                string += ";"
        if(string[-1] == ";"):
            string = string[:len(string)-1]
        return string

class ConnectionBuilderProtocole:
    def __init__(self,typeData,name):
        self.typeData = typeData
        self.name = name
    def build(self):
        return "connection:" + self.typeData + "." + self.name