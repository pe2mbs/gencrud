// src/app/menu/menu.component.ts

import { AfterViewInit, Component, Input, Renderer2, ViewChild } from "@angular/core";
import { Router } from "@angular/router";
import { GcMenuItem } from "../../nav/model";

@Component({
    selector: "gc-menu",
    templateUrl: "./menu.component.html",
    styleUrls: [ "./menu.component.scss" ],
})
export class GcMenuComponent implements AfterViewInit{
    @Input() isRootNode = false;
    @Input() item: GcMenuItem;
	@Input() rootTrigger = null;

	@ViewChild('trigger', {static: false})  trigger: any;


	public expanded: boolean;

    constructor(public router: Router) { }

	public ngAfterViewInit(): void
    {
		/*if ( this.isRootNode ) {
			const target = document.querySelector('#menuContainer')
			document.addEventListener('click', (event) => {
				const withinBoundaries = event.composedPath().includes(target)
				console.log("*************", event, this.trigger)
				if (!withinBoundaries) {
					if (this.trigger) {
						this.trigger.closeMenu()
					}
				}
			})
		}*/
    }

    isExpandable(item: GcMenuItem) : boolean {
        return item.children ? item.children.length > 0 : false;
    }

    public onItemSelected( item: GcMenuItem ): void
	{
		if ( !item.children || !item.children.length )
		{
			this.router.navigate( [ item.route ] );
		}
		if ( item.children && item.children.length )
		{
			this.expanded = !this.expanded;
			// Remember that the menu item is expanded.
			// localStorage.setItem( this.item.id, this.expanded ? 'expanded': '' );
		}
		return;
	}
}