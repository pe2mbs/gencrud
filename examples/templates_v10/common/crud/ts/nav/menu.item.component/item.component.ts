import { Component, HostBinding, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { animate, state, style, transition, trigger } from '@angular/animations';
import { GcMenuItem } from '../model';
import { isNullOrUndefined } from 'util';


@Component({
  	// tslint:disable-next-line:component-selector
  	selector: 'gc-menu-list-item',
  	templateUrl: './item.component.html',
	styleUrls: [ './item.component.scss' ],
  	animations: [
    	trigger('indicatorRotate', [
      		state( 'collapsed', style( { transform: 'rotate(0deg)' } ) ),
      		state( 'expanded', style( { transform: 'rotate(180deg)' } ) ),
      		transition('expanded <=> collapsed',
        		animate('225ms cubic-bezier(0.4,0.0,0.2,1)')
      		),
    	] )
  	]
} )
export class GcMenuListItemComponent implements OnInit
{
	public expanded: boolean;
	@HostBinding( 'attr.aria-expanded' ) ariaExpanded;
	@Input() item: GcMenuItem;
	@Input() depth: number;

	constructor( public router: Router )
	{
		if ( isNullOrUndefined( this.ariaExpanded ) )
		{
			this.ariaExpanded = this.expanded;
		}	
		if ( isNullOrUndefined( this.depth ) )
		{
			this.depth = 0;
		}
		return;
	}

	public ngOnInit(): void 
	{
		// Check if the memu item is expanded.
		this.expanded = localStorage.getItem( this.item.id ) === 'expanded';
		return;
	}

	get active(): boolean 
	{
		return this.item.route ? this.router.isActive( this.item.route, true ): false;
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
			localStorage.setItem( this.item.id, this.expanded ? 'expanded': '' );
		}
		return;
	}
}
