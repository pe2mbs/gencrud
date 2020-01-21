/*#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2020 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation; either version 2 of the
#   License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   Library General Public License for more details.
#
#   You should have received a copy of the GNU Library General Public
#   License GPL-2.0-only along with this library; if not, write to the
#   Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301 USA
#*/
import { Subscription } from 'rxjs';

export class Subscribers {
    private observableSubscriptions = [];

    constructor()
    {
        return;
    }

    /***************************************************************************************************
    / When dealing with RxJs Observables and Subscriptions, it can easily happen, that you leak some memory.
    / That is because your component is destroyed, but the function you registered inside of the observable
    / is not. That way, you not only leak memory but probably also encounter some odd behavior.
    /***************************************************************************************************/
    public registerSubscription( subscription: Subscription ): void
    {
        this.observableSubscriptions.push( subscription );
        return;
    }

    /***************************************************************************************************
    / To prevent memory leajs, make sure to unsubscribe from your subscriptions, when the component is destroyed.
    / One good place to do so, would be the ngOnDestroy lifecycle hook.
    /***************************************************************************************************/
    ngOnDestroy()
    {
        for ( let subscription of this.observableSubscriptions )
        {
            subscription.unsubscribe();
            console.log( 'kill subscriptions' );
        }
    }
}