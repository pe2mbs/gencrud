import { DataSource } from '@angular/cdk/collections';
import { BehaviorSubject, merge, Observable } from 'rxjs';
import { MatPaginator, MatSort } from '@angular/material';
import { map } from 'rxjs/operators';
import { CrudDataService } from './crud-dataservice';

export class CrudDataSource<T> extends DataSource<T> 
{
    protected _filterChange = new BehaviorSubject( '' );

    public get filter(): string
    {
        return this._filterChange.value;
    }

    public set filter( filter: string ) 
    {
        this._filterChange.next( filter );
    }

    public filteredData: T[] = [];
    public renderedData: T[] = [];

    constructor( public _databaseTable: CrudDataService<T>,
                 public _paginator: MatPaginator,
                 public _sort: MatSort ) 
    {
        super();
        // Reset to the first page when the user changes the filter.
        this._filterChange.subscribe(() => this._paginator.pageIndex = 0);
    }

    protected castRecord( record: any ) : T
    {
        return ( record );
    }

    protected castRecords( record: any[] ) : T[]
    {
        return ( record );
    }

    public makeSearchString( record: any ) : string
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
            this._paginator.page
        ];

        this._databaseTable.getAll();

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

    public disconnect() : void
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

    public resolveListItem( list: any, id: any ): string
    {
        let result: string;
        console.log( 'resolveListItem', list, id );
        list.forEach( function ( value )
        {
            console.log( value[ 'value' ], id );
            if ( value[ 'value' ] === id )
            {
                result = value[ 'label' ];
                return;
            }
        } );
        return ( result );
    }
}
