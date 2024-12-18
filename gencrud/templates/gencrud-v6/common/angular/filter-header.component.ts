import { Component,
		 OnInit,
		 EventEmitter,
		 Input,
		 ChangeDetectionStrategy,
		 Output } from '@angular/core';
import { Directive, HostListener } from "@angular/core";


export const CONDITIONS_LIST = [
	{ value: "EQ", 		label: "Is equal == " },
	{ value: "!EQ", 	label: "Is not equal !=" },
	{ value: "GT", 		label: "Greater than >" },
	{ value: "GT|EQ",	label: "Greater or equal than >=" },
	{ value: "LE", 		label: "Less than <" },
	{ value: "LE|EQ",	label: "Less or equal than <=" },
	{ value: "CO",		label: "Contains" },
	{ value: "!CO",		label: "Not contains" },
	{ value: "EM", 		label: "Is empty" },
	{ value: "!EM", 	label: "Is not empty" },
];


@Directive({
	// tslint:disable-next-line:directive-selector
	selector: "[mat-filter-item]"
})
export class FilterItemDirective
{
	@HostListener( "click", [ "$event" ] ) onClick( e: MouseEvent )
	{
    	e.stopPropagation();
    	e.preventDefault();
    	return false;
  	}
}


@Component({
    changeDetection: ChangeDetectionStrategy.OnPush,
    // tslint:disable-next-line:component-selector
    selector: 'filter-header',
	template: `<div class="header" click-stop-propagation>
	{{ title }}
	<button mat-icon-button class="btn-toggle" [matMenuTriggerFor]="menu">
		<mat-icon>keyboard_arrow_down</mat-icon>
	</button>
</div>
<mat-menu #menu>
	<div mat-menu-item mat-filter-item [disableRipple]="true" class="menu-title">
		<div fxLayout="row">
			<div fxFlex>Field</div>
			<div fxFlex fxLayoutAlign="end">{{ title }}</div>
		</div>
	</div>
	<div mat-menu-item mat-filter-item [disableRipple]="true">
		<mat-form-field>
		<mat-select [panelClass]="'mat-elevation-z10'" placeholder='Conditions' [(value)]="searchCondition.position">
			<mat-option *ngFor="let condition of conditionsList" [value]="condition.value" class="cond_option">
				{{ condition.label }}
			</mat-option>
		</mat-select>
		</mat-form-field>
	</div>
	<div mat-menu-item mat-filter-item [disableRipple]="true">
		<mat-form-field>
			<input matInput placeholder="Value" [(ngModel)]="filterRecord[ field ]">
		</mat-form-field>
	</div>
	<div mat-menu-item [disableRipple]="true">
		<div fxLayout="row">
			<button mat-raised-button fxFlex class="action-button" (click)="clearColumnFilter( field )">Clear</button>
			<button mat-raised-button color="primary" fxFlex class="action-button" (click)="applyColumnFilter()">Search</button>
		</div>
	</div>
</mat-menu>`,
	styles: [ `.cond_option { font-size: inherit; line-height: 1.5em!important; height: 1.5em!important; }`,
				'.action-button { width: 50px; margin-left: 5px; margin-right: 5px;  }'
	]
} )
export class FilterHeaderComponent implements OnInit
{
	public 		filter: any;
	public 		searchCondition: any = {};
	public 		conditionsList = CONDITIONS_LIST;
	@Input()	title: string;
	@Input()	field: string;
	@Input()	record: any;
	@Input()	filterRecord: any;
	@Input()	dataSource: any;
	@Output()	clearFilter: EventEmitter<any> = new EventEmitter<any>();
	@Output()	applyFilter: EventEmitter<any> = new EventEmitter<any>();

	constructor()
	{
		return;
	}

	public ngOnInit(): void
	{
		this.dataSource.filterPredicate = ( p: any, filtre: any ) => {
			let result = true;
			// keys of the object data 
			const keys = Object.keys( p ); 
			for ( const key of keys ) 
			{
				// get search filter method
			  	const searchCondition = filtre.conditions[ key ]; 
				if ( searchCondition && searchCondition !== 'none' ) 
				{
					// invoke search filter 
					if ( filtre.methods[ searchCondition ]( p[ key ], filtre.values[ key ] ) === false ) 
					{
						// if one of the filters method not succeed the row will be remove from the filter result 
						result = false; 
				  		break;
					}
			  	}
			}
			return ( result );
		};
	}

	public clearColumnFilter( columnKey: string ): void
	{
		console.log( "clearColumnFilter", this.filterRecord );
		this.filterRecord[ columnKey ] = null;
		this.searchCondition.position = 0;
		this.applyColumnFilter();
		return;
	}

	public applyColumnFilter(): void 
	{
		console.log( "applyColumnFilter", this.filterRecord );
		return;
	}
}
