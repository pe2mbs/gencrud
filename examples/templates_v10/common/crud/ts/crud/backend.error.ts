import { GcBackEndInfo } from './model';

export class GcBackendError extends Error
{
    public code: number;
    public backend: string;
    public trace: string;
    public url: string;
    public backendInfo: GcBackEndInfo;
    constructor( message: string, backend_info: GcBackEndInfo )
    {
        const trueProto = new.target.prototype;
        super( message );
        Object.setPrototypeOf(this, trueProto);
        this.code = backend_info.code;
        this.backend = backend_info.message;
        this.trace = backend_info.traceback;
        this.url = backend_info.url;
        this.backendInfo = backend_info;
    }
}
