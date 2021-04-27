/*
#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2020 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   Library General Public License for more details.
#
#   You should have received a copy of the GNU Library General Public
#   License GPL-2.0-only along with this library; if not, write to the
#   Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301 USA
#
*/
import { EventEmitter } from '@angular/core';
import { DataSource } from '@angular/cdk/collections';
import { PageEvent } from '@angular/material';
import { BehaviorSubject, merge, Observable } from 'rxjs';
import { MatPaginator, MatSort } from '@angular/material';
import { map } from 'rxjs/operators';
import { CrudDataService } from './crud-dataservice';
import * as moment from 'moment';


export class CrudDataSource<T> extends DataSource<T> 
{
    protected _filterChange = new BehaviorSubject( '' );
    public filteredData: T[] = [];
    public renderedData: T[] = [];

    constructor( public _databaseTable: CrudDataService<T>,
                 public _paginator: MatPaginator,
                 public _sort: MatSort,
                 public pageEvent: EventEmitter<PageEvent>,
                 protected _backend_filter: any )
    {
        super();
        // Reset to the first page when the user changes the filter.
        this._filterChange.subscribe(() => this._paginator.pageIndex = 0);
    }

    public get filterChange()
    {
        return ( this._filterChange );
    }

    public get filter(): string
    {
        return this._filterChange.value;
    }

    public set filter( filter: string )
    {
        this._filterChange.next( filter );
    }

    protected castRecord( record: any ): T
    {
        return ( record );
    }

    protected castRecords( record: any[] ): T[]
    {
        return ( record );
    }

    public makeSearchString( record: any ): string
    {
        return ( '' );
    }

    /** Connect function called by the table to retrieve one stream containing the data to render. */
    public connect(): Observable<T[]> 
    {
        // Listen for any changes in the base data, sorting, filtering, or pagination
        const displayDataChanges = [
            this._databaseTable.dataChange,
            this._sort.sortChange,
            this._filterChange,
            this.pageEvent
        ];

        this._databaseTable.getAll( this._backend_filter );

        return merge(...displayDataChanges).pipe(map( () => {
            // Filter data
            this.filteredData = this.castRecords( this._databaseTable.data.slice().filter((record: any) => {
                const searchStr = this.makeSearchString( record );
                return ( searchStr.indexOf( this.filter.toLowerCase()) !== -1 );
            } ) );

            // Sort filtered data
            const sortedData = this.sortData( this.filteredData.slice() );
            // Grab the page's slice of the filtered sorted data.
            const startIndex  = this._paginator.pageIndex * this._paginator.pageSize;
            this.renderedData = sortedData.splice(startIndex, this._paginator.pageSize);
            return ( this.renderedData );
        } ) );
    }

    public disconnect(): void
    {
        return;
    }

    public sortActive( active: string, a: any, b: any ): string[] 
    {
      return ( [ null, null ] );
    }

    /** Returns a sorted copy of the database data. */
    public sortData( data: T[] ): T[] 
    {
        if (!this._sort.active || this._sort.direction === '') 
        {
            return data;
        }
        return data.sort( ( a, b ) => {
            let propertyA: number | string = '';
            let propertyB: number | string = '';
            [ propertyA, propertyB ] = this.sortActive( this._sort.active, a, b );
            
            const valueA = isNaN( +propertyA ) ? propertyA : +propertyA;
            const valueB = isNaN( +propertyB ) ? propertyB : +propertyB;

            return (valueA < valueB ? -1 : 1) * ( this._sort.direction === 'asc' ? 1 : -1 );
        } );
    }

    public reFormat( value: string, pipe: string, format: string ): string
    {
        if ( value === undefined || value === null || value === '' )
        {
            return ( value );
        }
        if ( pipe === 'datetime' )
        {
            let defFormat = "YYYY-MM-DD HH:mm:ss";
            const splitted = format.split(";", 2);
            if ( splitted.length > 0 )
            {
                let idx = 0;
                if ( splitted[ 0 ].length === 2 || splitted[ 0 ].length === 5 )
                {
                    moment.locale( splitted[ 0 ] );
                    idx++;
                }
                if ( idx < splitted.length )
                {
                    defFormat = splitted[ idx ];
                }
            }
            value = moment( value ).format( defFormat );
        }
        return ( value );
    }
}
