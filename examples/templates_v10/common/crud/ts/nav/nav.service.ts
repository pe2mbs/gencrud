import { Injectable } from '@angular/core';
import { Observable, EMPTY } from 'rxjs';
import { GcMenuItem } from './model';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  	providedIn: 'root'
})
export class GcNavService 
{
	constructor( private http: HttpClient ) 
	{ 
		return;
	}

	public menuItems(): Observable<GcMenuItem[]>
	{
		return ( this.http.get<GcMenuItem[]>( environment.apiUrl + '/menu' ) );
	}
}
