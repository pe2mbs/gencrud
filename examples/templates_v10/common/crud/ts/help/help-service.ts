import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  	providedIn: 'root'
})
export class GcHelpService 
{
	constructor( private httpSession: HttpClient ) 
	{ 
		return;
	}

	public getHelp( name: string, fallback: string ): Observable<string>
	{
		return ( this.httpSession.get<string>( '/api/help/' + name ) );
	}
}
