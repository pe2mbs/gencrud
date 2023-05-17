import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class SpinnerService
{
    private _url: string = '';
    public visibility: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

    constructor()
    {
        return;
    }

    public setUrl( url: string )
    {
        this._url = url;
        return;
    }

    show( url: string = '' )
    {
        if ( url.startsWith( this._url ) )
        {
            this.visibility.next(true);
        }
        return;
    }

    hide( url: string = '' )
    {
        if ( url.startsWith( this._url ) )
        {
            this.visibility.next(false);
        }
        return;
    }
}
