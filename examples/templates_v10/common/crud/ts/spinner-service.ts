import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

// TODO: This needs to be REMOVED!!!!

@Injectable({
    providedIn: 'root'
})
export class GcSpinnerService
{
    public visibility: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
    constructor()
    {
        return;
    }

    show()
    {
        this.visibility.next( true );
        return;
    }

    hide()
    {
        this.visibility.next( false );
        return;
    }
}
