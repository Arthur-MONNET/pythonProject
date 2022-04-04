class BuilderProtocole:
    def __init__(self,typeData,values):
        self.typeData = typeData
        self.values = values
    def build(self):
        print("data : "+self.typeData+", "+str(self.values[0]))
        string = self.typeData + ":"
        mult = False
        print("before create : "+string)
        for val in self.values:
            string += str(val)
            if(mult):
                string += ";"
            mult = True
        print("after create : "+string)
        if(string[-1] == ";"):
            print("before -1 : "+string)
            string = string[:len(string)-1]
            print("after -1 : "+string)
        return string
