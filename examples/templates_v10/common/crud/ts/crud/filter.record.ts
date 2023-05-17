import { EventEmitter } from '@angular/core';
import { GcFilterColumn } from './filter.column';
import { isNull } from 'util';
import { GcFilterColumnReq } from './model';


export class GcFilterEvent
{
	filter: GcFilterRecord;
}

export class GcFilterRecord
{
	protected debug: boolean;
	event: EventEmitter<GcFilterEvent> = new EventEmitter<GcFilterEvent>();
	filterColumns: GcFilterColumn[] = new Array<GcFilterColumn>();
	constructor( columns: string[], debug = false )
	{
		this.debug = debug;
		if ( this.debug )
		{
			console.log( 'constructor( columns = ', columns, ' )' );
		}
		columns.forEach( field => {
			if ( this.debug )
			{
				console.log( 'constructor => ', field );
			}
			this.filterColumns.push( new GcFilterColumn( field ) );
		} );
		return;
	}

	public findItem( column: string ): GcFilterColumn | null
	{
		let result = null;
		if ( this.debug )
		{
			console.log( 'findItem( columns = ', this.filterColumns, ' )' );
			console.log( `findItem( column = "${column}" )` );
		}
		this.filterColumns.forEach( field =>
		{
			console.log( 'findItem => ', field );
			if ( field.column === column )
			{
				result = field;
				return;
			}
		} );
		return ( result );
	}

	public clear( column: string )
	{
		const col: GcFilterColumn = this.findItem( column );
		if ( col != null )
		{
			col.clear();
		}
		return;
	}

	public set( column: string, value: any, operator: string = 'EQ' ): void
	{
		let col: GcFilterColumn = this.findItem( column );
		if ( isNull( col ) )
		{
			if ( this.debug )
			{
				console.log( `Adding filter to ${column} with value ${value}` );
			}
			this.filterColumns.push( new GcFilterColumn( column ) );
			col = this.findItem( column );
		}
		col.apply( [ value, null ], operator );
		return;
	}

	public apply( column: string, values: any | any[], operator: string )
	{
		const col: GcFilterColumn = this.findItem( column );
		if ( this.debug )
		{
			console.log( "apply", column, values, operator, col );
		}
		if ( col != null )
		{
			col.apply( values, operator );
		}
		return;
	}

	public getFilters(): GcFilterColumnReq[]
	{
		const columns: GcFilterColumnReq[] = new Array<GcFilterColumnReq>();
		this.filterColumns.forEach( field =>
		{
			if ( this.debug )
			{
				console.log( 'getFilters( columns = ', this.filterColumns, ' )' );
				console.log( "getFilter", field );
			}
			if ( field.value != null || field.operator != null )
			{
				columns.push( { column: field.column,
								value: field.value,
								operator: field.operator } );
				return;
			}
		} );
		return ( columns );
	}

	public setFilters( columns: GcFilterColumnReq[] )
	{
		columns.forEach(column => {
			this.apply(column.column, column.value, column.operator)
		});
		return
	}
}
