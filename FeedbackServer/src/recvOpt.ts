import {Subject} from "rxjs";

class MySubject
{
    private subject = new Subject();

    get Subject()
    {
        return this.subject;
    }

    public publish (req: {})
    {
        this.subject.next(req);
    }
}

const mySubject = new MySubject();

export {mySubject};
