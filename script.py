from simple_websocket_server import WebSocketServer, WebSocket
from decoderProtocole import DecoderProtocole

class SimpleEcho(WebSocket):
    def handle(self):
        print(self.data)
        data = DecoderProtocole(self.data)
        print(data)
        data.decodeData()
        print(data.typeVal)
        for val in data.valueTab:
            print(val)
        self.send_message(self.data)

    def connected(self):
        self.send_message('connected')
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')


server = WebSocketServer('', 8000, SimpleEcho)
server.serve_forever()