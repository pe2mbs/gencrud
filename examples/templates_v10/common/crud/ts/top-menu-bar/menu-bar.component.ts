import { Component, OnInit  } from '@angular/core';
import { Router } from '@angular/router';
import { GcMenuItem } from '../nav/model';
import { GcNavService } from '../nav/nav.service';


@Component({
  	// tslint:disable-next-line:component-selector
  	selector: 'gc-menu-bar',
  	template: '<mat-toolbar class="gc-toolbar" color="primary"><gc-menu *ngFor="let item of navItems" [item]="item" [isRootNode]="true"></gc-menu></mat-toolbar>',
	styleUrls: [ './menu-bar.component.scss' ],
})
export class GcMenuBarComponent implements OnInit
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
