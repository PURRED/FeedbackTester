import socketio
from events import Events
from injector import singleton, inject

@singleton
class IOClient:

    @inject
    def __init__(self):
        self.sio = None
        self.events = Events()


    def connect(self, wsUrl):
        try:
            sio = socketio.Client()

            @sio.on("connect")
            def on_connect():
                print("Connected")
                self.events.connect()

            @sio.on("message")
            def on_message(message):
                self.events.message(message)

            @sio.on("disconnect")
            def on_disconnect():
                print("disconnect")
                self.events.disconnect("Conneced")

            self.sio = sio
            self.sio.connect(wsUrl)
        except Exception as ex:
            print("예외가 발생했습니다", ex)

    def disconnect(self):
        if self.sio:
            self.sio.disconnect()

    # def init_member(self, member_id):
    #     self.sio.emit('initMember', {"memberID": member_id, "memberType": "DEVICE"})