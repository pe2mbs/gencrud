import { Component, ElementRef, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { isNullOrUndefined } from 'util';


@Component({
  	// tslint:disable-next-line:component-selector
  	selector: 'gc-default',
      template: `<gc-header (onToggleSidebar)="doToggleSidebar( $event )"></gc-header>
	  <gc-news-ticker (change)="onNewsChange( $event )"></gc-news-ticker> 
	  <gc-menu-bar></gc-menu-bar>     
<mat-drawer-container [ngClass]="drawerClass">
	<mat-drawer mode="side" [opened]="sideBarOpen">
		<gc-nav-sidebar></gc-nav-sidebar>
	</mat-drawer>
	<mat-drawer-content #sidenavcontent autosize="true" >
		<router-outlet></router-outlet>
	</mat-drawer-content>
</mat-drawer-container>
<gc-footer></gc-footer>`,
  	styleUrls: [ './default.component.scss' ]
})
export class GcDefaultComponent 
{
	public sideBarOpen: boolean = false;
    public drawerClass: string = 'without-ticker';

	@ViewChild( 'sidenavcontent', { read: ElementRef, static: true } ) sidenavcontentRef: ElementRef;
    
    viewRendered()
    {
        this.sidenavcontentRef.nativeElement.style.marginLeft = '200px';
        return;
    }
	constructor(private router: Router) 
	{ 
		const sideBarInfo = localStorage.getItem( "sideBarOpen" );
		if (!isNullOrUndefined(sideBarInfo)) {
			this.sideBarOpen = JSON.parse(sideBarInfo);
		}
		return;
	}

	public doToggleSidebar( $event ): void
	{
		this.sideBarOpen = !this.sideBarOpen;
		localStorage.setItem("sideBarOpen", JSON.stringify(this.sideBarOpen));
		return;
	}

    public onNewsChange( $event: boolean )
    {
        this.drawerClass = $event ? 'with-ticker' : 'without-ticker';  
        return;
    }
}
