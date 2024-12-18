import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class SpinnerService
{
    public visibility: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
    constructor()
    {
        return;
    }

    show()
    {
        this.visibility.next(true);
        return;
    }

    hide()
    {
        this.visibility.next(false);
        return;
    }
}