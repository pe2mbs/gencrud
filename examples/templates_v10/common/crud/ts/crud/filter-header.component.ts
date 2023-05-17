import { Component, EventEmitter, Input, ChangeDetectionStrategy, Output,  OnInit, SimpleChanges, OnChanges, AfterViewInit, ViewChild } from '@angular/core';
import { Directive, HostListener } from "@angular/core";
import { isNullOrUndefined } from 'util';
import { GcConditionItem, GcSelectList } from './model';
import { GcFilterRecord, GcFilterEvent } from './filter.record';
import { Observable, Subscription } from 'rxjs';
import { GcSubscribers } from '../subscribers';


export const CONDITIONS_LIST_SIMPLE: GcConditionItem[] = [
	{ value: "EQ", 		label: "Is equal ==", param: 0 },
	{ value: "!EQ", 	label: "Is not equal !=", param: 0 },
];


export const CONDITIONS_LIST: GcConditionItem[] = [
	{ value: "EQ", 		label: "Is equal ==", param: 1 },
	{ value: "!EQ", 	label: "Is not equal !=", param: 1 },
	{ value: "GT", 		label: "Greater than >", param: 1 },
	{ value: "GT|EQ",	label: "Greater or equal than >=", param: 1 },
	{ value: "LE", 		label: "Less than <", param: 1 },
	{ value: "LE|EQ",	label: "Less or equal than <=", param: 1 },
	{ value: "BT",		label: "Between", param: 2 },
	{ value: "SW",		label: "Startswith", param: 1 },
	{ value: "EW",		label: "Endswith", param: 1 },
	{ value: "CO",		label: "Contains", param: 1 },
	{ value: "!CO",		label: "Not contains", param: 1 },
	{ value: "EM", 		label: "Is empty", param: -1 },
	{ value: "!EM", 	label: "Is not empty", param: -1 },
];


export const CONDITION_FIELDS = {
	// Default value is 1
	"BT": 2,
	"EM": 0,
	"!EM": 0,
};


@Directive( {
	// tslint:disable-next-line:directive-selector
	selector: "[mat-filter-item]"
} )
export class GcFilterItemDirective
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
	templateUrl: 'filter-header.component.html',
	styles: [ `.cond_option { font-size: inherit; line-height: 1.5em!important; height: 1.5em!important; }`,
				'.action-button { width: 50px; margin-left: 5px; margin-right: 5px;  }',
				'.title-highlight { font-weight: bolder; }'
	]
} )
export class GcFilterHeaderComponent extends GcSubscribers implements OnInit, AfterViewInit
{
	public 		conditionsList: GcConditionItem[];
	public 		conditionPosition: string = "CO";
	public 		value: string[] = ["", ""];
	public 		valuePosition: number = null;
	public 		caption: string[] = [ 'Value', 'Max. value' ];
	public 		fields: number = 1;
	public		title_filter = "";
	public	    resolveItems: GcSelectList[];
	@Input()	title: string;
	@Input()	field: string;
	@Input()	items: GcSelectList[] | Observable<GcSelectList[]>;
	@Input()	filterRecord: GcFilterRecord;
	@Output()	applyFilter: EventEmitter<GcFilterEvent> = new EventEmitter<GcFilterEvent>();

	constructor()
	{
		super();
		return;
	}

	public ngOnInit(): void 
	{
		if ( isNullOrUndefined( this.items ) )
		{
			this.fields = 1;
			this.conditionsList = CONDITIONS_LIST;
		}
		else
		{
			// check concrete type is observable or not
			if ("subscribe" in this.items ) {
				this.registerSubscription(this.items.subscribe(items => {
					this.resolveItems = items;
				}));
			} else {
				this.resolveItems = this.items;
			}
			this.conditionsList = CONDITIONS_LIST_SIMPLE;
			this.conditionPosition = "EQ";
			this.fields = 0;
		}
		return;
	}


	public ngAfterViewInit(): void {
		if (this.filterRecord) {
			try {
				const operator = this.filterRecord.findItem(this.field).operator;
				if (operator) this.conditionPosition = operator;
				const value = this.filterRecord.findItem(this.field).value as string[];
				if (!isNullOrUndefined(value)) {
					if ( isNullOrUndefined( this.items ) ) {
						this.value = value;
					} else {
						this.valuePosition = parseInt(value[0]);
					}
					this.title_filter = "title-highlight";
				}
			} catch (e) {
				console.log(e)
			}
		}
	}

	public onKeyDown( event: KeyboardEvent, input: HTMLInputElement = undefined ) {
		if (event.shiftKey) {
			switch(event.key) {
				case "Home": event.preventDefault(); event.stopPropagation();
					this.selectWord(input); break;
				case "End": event.preventDefault(); event.stopPropagation();
					this.selectWord(input); break;
				default: break;
			}
 		} else {
			switch(event.key) {
				case "Home": event.preventDefault(); event.stopPropagation();
					this.moveInput(input, "start"); break;
				case "End": event.preventDefault(); event.stopPropagation();
					this.moveInput(input, "end"); break;
				case "Tab": event.preventDefault(); event.stopPropagation();
					this.handleTabClick(input); break;
				default: break;
			}
		}
	}

	private handleTabClick(input: HTMLInputElement) {
		if(this.fields == 2 && input.id == "first-filter-input") {
			document.getElementById("second-filter-input").focus();
		} else {
			document.getElementById("filter-button").focus();
		}
	}

	private moveInput(input: HTMLInputElement, position) {
		let index = 0;
		if (position == "end") {
			index = input.value.length;
		}

		input.setSelectionRange(index, index);
		input.focus();
	}

	private selectWord(input: HTMLInputElement) {
		input.select();
	}

	
	public selectValue( $event ): void
	{
		console.log( "selectValue", $event );
		return;
	}

	private findConditionItem( value: string ): GcConditionItem
	{
		let item: GcConditionItem = null;
		this.conditionsList.forEach( element => {
			if ( element.value === value )
			{
				item = element;
				return;
			}
		} );
		return ( item );
	}

	public selectCondition( $event ): void
	{
		console.log( "selectCondition", $event, this.conditionPosition, this.resolveItems );
		if ( !isNullOrUndefined( this.resolveItems ) )
		{
			this.fields = 0;
		}
		else
		{
			this.fields = 1;
			this.caption[ 0 ] = 'Value';
			const item = this.findConditionItem( $event.value );
			console.log( 'item', item ) ;
			this.fields = item.param;
			if ( this.fields === 2 )
			{
				this.caption[ 0 ] = 'Min. Value';
			}
		}
		return;
	}

	public clearColumnFilter(): void
	{
		if ( !isNullOrUndefined( this.items ) ) {
			this.conditionPosition = "EQ";
		} else {
			this.conditionPosition = "CO";
		}
		this.value = [ null, null ];
		this.filterRecord.clear( this.field );
		this.title_filter = "";
		const e = new GcFilterEvent();
		e.filter = null;
		this.valuePosition = null;
		this.filterRecord.event.emit( e );
		return;
	}

	public applyColumnFilter(menuTrigger): void 
	{
		if ( isNullOrUndefined( this.resolveItems ) )
		{
			console.log("*********", this.field, this.value, this.conditionPosition)
			this.filterRecord.apply( this.field, 
									 this.value, 
									 this.conditionPosition );
		}									 
		else
		{
			this.filterRecord.apply( this.field, 
									 [ this.valuePosition, null ], 
									 this.conditionPosition );
		}
		this.applyFilter.emit( { filter: this.filterRecord } );
		if ( this.filterRecord.event != null )
		{
			const e = new GcFilterEvent();
			e.filter = this.filterRecord;
			this.filterRecord.event.emit( e );
		}
		this.title_filter = "title-highlight";
		menuTrigger.closeMenu();
		return;
	}
}
