import {mySubject} from "../recvOpt";
import * as socketIO from "socket.io"
import * as http from "http";

export class WsController
{
    private io: socketIO.Server;

    connectSocket = (socket) => {
        console.log("새로운 클라이언트 접속!", socket.id);

        socket.on("disconnect", this.disconnectSocket);
    };

    disconnectSocket = (socket) => {
      console.log("disconnect 수신");
    };

    constructor(private http: http.Server) {

        this.io = socketIO.listen (http);

        this.io.sockets.on("connection", this.connectSocket);

        mySubject.Subject.subscribe({
            next: (req) => {
                this.io.sockets.emit("message", req);
                console.log(req);
            }
        });
    }
}
