/*
#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2020 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation.
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
#
#   gencrud: 2020-12-10 13:12:05 version 2.0.616 by user A480226
*/
import { Injectable, EventEmitter } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subscription } from 'rxjs';
import { environment } from 'src/environments/environment';
import { isNullOrUndefined } from 'util';


export interface NewsItem
{
	N_ID: number;
	N_ACTIVE: boolean;
	N_ALERT: string;        
	N_KEEP: string; 
    N_MESSAGE: string;
    N_START_DATE: string;
	N_END_DATE: string;
	N_PERIOD?: string;
}

interface NewsMessages
{
    N_NEWS: NewsItem[];
    N_TOTAL_ITEMS: number;        
    N_POLL_INTERVAL: number;        
}


@Injectable( {
	providedIn: 'root',
} )
export class GcTickerDataService
{
    private uri = '/api/news/getnews';
	protected triggerEvent = new EventEmitter<any>();
	public updateEvent = new EventEmitter<any>();
	protected subscribedEvent: Subscription = null;
	protected msgs: NewsMessages = null;
	protected newsAvailable: boolean = false;
	protected pollInterval: number = 5;
	
    constructor( private httpClient: HttpClient )
    {
		if ( !environment.readNews )
		{
			// Do NOT start the news reader.
			return;
		}
		this.triggerEvent.subscribe( () => {
			if ( this.subscribedEvent != null )
            {
				this.subscribedEvent.unsubscribe();
			}
			this.subscribedEvent = this.httpClient.get<NewsMessages>( this.uri ).subscribe( result => { 
				this.msgs = result;
				this.pollInterval = this.msgs.N_POLL_INTERVAL; 
				this.updateEvent.emit( this.msgs.N_NEWS );
				setTimeout( () => { 
					this.triggerEvent.emit();
				}, this.pollInterval * 1000 );
			} );       
		} );
		setTimeout( () => { 
            this.triggerEvent.emit();
        }, this.pollInterval * 1000 );
        return;
    }

    public getNews(): NewsItem[]
    {
		if ( isNullOrUndefined( this.msgs ) )
		{
			return [];
		}
        return ( this.msgs.N_NEWS );
	}
	
	public get NewsAvailable(): boolean
	{
		return ( this.newsAvailable ) ;
	}
}
