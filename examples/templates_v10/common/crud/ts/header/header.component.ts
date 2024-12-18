import { HttpClient } from '@angular/common/http';
import { ChangeDetectorRef, Component, OnInit, Output } from '@angular/core';
import { EventEmitter } from '@angular/core';
import { ApplicationInfo } from '../crud/model';
import { environment } from 'src/environments/environment';
import { GcSubscribers } from '../subscribers';

export interface ApplicationInfo
{
    application: string;
    logo: string;
    version: string;
    ReleaseDate: string;
    plugins: Array<string>;
    theme: string;
}

@Component({
  	// tslint:disable-next-line:component-selector
  	selector: 'gc-header',
  	templateUrl: './header.component.html',
	styleUrls: ['./header.component.scss']
})
// @ts-ignore
export class GcHeaderComponent extends GcSubscribers // implements OnInit
{
	// @ts-ignore
	@Output() onToggleSidebar: EventEmitter<any> = new EventEmitter(); 
	headerTitle: string = 'Application';
	headerLogo: string = 'logo.png';
    themeColor: string = 'light-theme';
	release: string = 'R2019-01';
	releaseDate: string = '01 October 2019';
    public timeStamp;
    
	constructor( private cdRef: ChangeDetectorRef, protected httpClient: HttpClient )
	{ 
        super();
        this.timeStamp = (new Date()).getTime();
		if ( environment.headerTitle !== undefined && environment.headerTitle != null )
		{
			this.headerTitle = environment.headerTitle;
		}
		if ( environment.headerLogo !== undefined && environment.headerLogo != null )
		{
            this.headerLogo = `/assets/${this.themeColor}/${environment.headerLogo}`;
		}
		if ( environment.release !== undefined && environment.release != null )
		{
			this.release = environment.release;
		}
		if ( environment.releaseDate !== undefined && environment.releaseDate != null )
		{
			this.releaseDate = environment.releaseDate;
		}
        this.registerSubscription( httpClient.get( '/api/application/info' ).subscribe( (data:ApplicationInfo) => {
            this.release = data.version
            this.releaseDate = data.ReleaseDate;
            this.headerTitle = data.application
            this.headerLogo = data.logo;
            this.themeColor = data.theme;
            this.headerLogo = `/assets/${this.themeColor}/${data.logo}`;
        } ) );
		return;
    }
    
	public toggleSidebar()
	{
		this.onToggleSidebar.emit();
		return;
	}
}
