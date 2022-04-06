from simple_websocket_server import WebSocketServer, WebSocket
from decoderProtocole import DecoderProtocole
import os
i=0
class SaveData:
    pass
    
class State:
    def __init__(self,tempLim,proxLim, tempState, proxState):
        self.tempLim = tempLim
        self.proxLim = tempLim
        self.tempState = tempState
        self.proxState = proxState
        self.test()
        
    def test(self):
        if self.tempState and self.proxState:
            self.goodState = True
        else:
            self.goodState = False
    
    def changeTemp(self, val):
        print(val)
        newState = False
        if val>self.tempLim:
            newState = True
        if newState != self.tempState:
            self.tempState = newState
            self.test()
            
    def changeProx(self, val):
        print(val)
        newState = False
        if val>self.proxLim:
            newState = True
        if newState != self.proxState:
            self.proxState = newState
            self.test()
        
#stateLike = State(30,120, False, False)
saveData = SaveData()
saveData.buttonfigure="False"
class SimpleEcho(WebSocket):
    def handle(self):
        data = DecoderProtocole(self.data)
        data.decodeData()
        if data.typeVal == 'button':
            if data.keyValues[0][1] == "True" and getattr(saveData,data.typeVal+data.name)=="False":
                #os.system("raspistill -o ./images/image.jpg")
                print("button press")
                os.system("mpg123 ./audio.mp3")
                #state.changeTemp(int("32"))
                #state.changeProx(int("140"))
                #print(state.goodState)
            setattr(saveData,data.typeVal + data.name,data.keyValues[0][1])
        elif data.typeVal == 'temp':
            pass
        self.send_message(self.data)

    def connected(self):
        self.send_message('connected')
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')
        
server = WebSocketServer('', 8000, SimpleEcho)
server.serve_forever()