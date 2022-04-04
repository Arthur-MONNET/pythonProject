from simple_websocket_server import WebSocketServer, WebSocket
from decoderProtocole import DecoderProtocole
import os
i=0
class State:
    def __init__(self,tempLim,proxLim, tempState, proxState):
        self.tempLim = tempLim
        self.proxLim = tempLim
        self.tempState = tempState
        self.proxState = proxState
        
    def test(self):
        if self.tempState == 1 and self.proxState == 1:
            self.goodState = True
        else:
            self.goodState = False
    
    def changeTemp(self, val):
        newState = 0
        if val>self.tempLim:
            newState = 1
        if newState != self.tempState:
            self.tempState = newState
            self.testState()
            
    def changeProx(self, val):
        newState = 0
        if val>self.proxLim:
            newState = 1
        if newState != self.proxState:
            self.proxState = newState
            self.testState()
        
state = State(30,120,20,200)
class SimpleEcho(WebSocket):
    def handle(self):
        print(self.data)
        data = DecoderProtocole(self.data)
        print(data)
        data.decodeData()
        print(data.typeVal)
        for val in data.valueTab:
            print(val)
        if data.typeVal == 'button' and data.valueTab[0] == '1':
            #os.system("raspistill -o ./images/image.jpg")
        elif data.typeVal == 'temp':
            state.changeTemp(int(data.valueTab[0]))
            state.changeTemp(int(data.valueTab[1]))
        self.send_message(self.data)

    def connected(self):
        self.send_message('connected')
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')

state = State()
server = WebSocketServer('', 8000, SimpleEcho)
server.serve_forever()