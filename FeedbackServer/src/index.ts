import * as express from "express"
import {mySubject} from "./recvOpt";
import {WsController} from "./ws/wsController";
import * as http from "http";
import * as bodyParser from "body-parser";
import * as logger from "morgan"

interface Err extends Error {
    status: number
    data?: any
}

class App {
    public application: express.Application;

    public wsController: WsController;

    private readonly server: http.Server;

    constructor() {
        this.application = express();

        this.init();

        this.server = http.createServer(this.application);
        this.server.listen(7777, () => {
            console.log("start");
        });

        this.wsController = new WsController(this.server);
    }

    private init ()
    {
        this.application.use(logger('dev'));
        this.application.use(bodyParser.json());
        this.application.use(bodyParser.urlencoded({ extended: false }));


        this.application.get("/", (req: express.Request, res: express.Response) => {
            res.send("index");
        });

        // catch 404 and forward to error handler
        this.application.use ((req: express.Request, res: express.Response, next: express.NextFunction) => {

            if (req.method == "POST")
            {
                console.log(req.body);
                mySubject.publish(req.body);
                res.send("post");
            }
            else {
                let err = new Error('Not Found') as Err;
                err.status = 404;
                next(err);
            }
        });
    }
}

new App();
