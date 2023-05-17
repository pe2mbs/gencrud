import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { GcMenuItem } from './model';
import { GcNavService } from './nav.service';


@Component({
  	// tslint:disable-next-line:component-selector
  	selector: 'gc-nav-sidebar',
  	template: '<mat-nav-list><gc-menu-list-item *ngFor="let item of navItems" [item]="item"></gc-menu-list-item></mat-nav-list>',
	styleUrls: [ './sidebar.component.scss' ],
})
export class GcNavSidebarComponent implements OnInit 
{
    navItems: GcMenuItem[] = [];

    constructor( private navService: GcNavService,
                 private router: Router )
    {
        return;
    }

    public ngOnInit(): void
    {
        this.navService.menuItems().subscribe( response => { this.navItems = response; console.log(this.navItems) } );
        return;
    }
}
