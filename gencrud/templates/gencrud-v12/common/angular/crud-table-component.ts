import { Subscribers } from './subscribers';
import { fromEvent } from 'rxjs';
import { MatDialog, MatPaginator, MatSort, PageEvent } from '@angular/material';
import { ElementRef, ViewChild, EventEmitter, Input, OnInit, OnDestroy } from '@angular/core';
import { CrudDataSource } from './crud-datasource';
import { ActivatedRoute } from '@angular/router';
import { CrudDataService } from './crud-dataservice';

export class TableBaseComponent<T> extends Subscribers implements OnInit, OnDestroy
{
    index: number;
    @Input() id: any;
    @Input() value: any;
    public mode: string;
    protected backendFilter: any = null;
    public pageSize: number = 10;
    public pageIndex: number = 0;
    public paginatorEvent: EventEmitter<PageEvent>;
    dataSource: CrudDataSource<T>  | null;

    @ViewChild( 'bot_paginator', { static: true } )   bot_paginator: MatPaginator;
    @ViewChild( 'top_paginator', { static: true } )   top_paginator: MatPaginator;
    @ViewChild( MatSort, { static: true } )       sort: MatSort;
    @ViewChild( 'filter', { static: true } )      filter: ElementRef;

    constructor( public componentName: string,
                 public addDialogComponent,
                 public delDialogComponent,
                 public route: ActivatedRoute,
                 public dialog: MatDialog,
                 public dataService: CrudDataService<T> )
    {
        super();
        this.paginatorEvent = new EventEmitter<PageEvent>();
        return;
    }

    public applyFilter( dummy: T )
    {
        return;
    }

    public ngOnInit(): void
    {
        let tmp = localStorage.getItem( this.componentName + '.size' );
        if ( tmp !== null )
        {
            this.pageSize = +tmp;
        }
        if ( this.id !== undefined && this.id !== null )
        {
            this.backendFilter = { id: this.id, value: this.value };
            this.mode = 'filter';
        }
        else
        {
            this.mode = 'view';
            this.registerSubscription( this.route.queryParams.subscribe( params => {
                // console.log( params );
                if ( params.id !== undefined && params.id !== null )
                {
                    this.backendFilter = {
                        id:     params.id,      // Contains the key field.
                        value:  params.value    // Contains val value for the key field.
                    };
                    this.mode = params.mode; // filter, edit or new only supported on the screen component
                }
            } ) );
        }
        console.log( 'ngOnInit: mode', this.mode );
        // console.log( 'ngOnInit: backendFilter', this.backendFilter );
        this.loadData();
        tmp = localStorage.getItem( this.componentName + '.index' );
        if ( tmp !== null )
        {
            this.bot_paginator.pageIndex = +tmp;
        }
        return;
    }

    public ngOnDestroy(): void
    {
        super.ngOnDestroy();
        return;
    }

    public addRecord(): void
    {
        const nRecord = this.newRecord();
        console.log( 'addNew ', nRecord );
        const dialogRef = this.dialog.open( this.addDialogComponent,
        {
            data: { record: nRecord,
                    mode: 'add' },
        } );
        const height: number = ( 6 * 72 ) + 130;
        dialogRef.afterClosed().subscribe( result =>
        {
            console.log( 'addNew() dialog result ', result );
            if ( result === 1 )
            {
                // After dialog is closed we're doing frontend updates
                this.refreshTable();
            }
        } );
        dialogRef.updateSize( '85%', height.toString() + 'px' );
        return;
    }

    public refresh(): void
    {
        this.dataSource.connect();
        return;
    }

    public editRecord( foundIndex: number, edit_record: T ): void
    {
        this.dataService.lockRecord( edit_record );
        const height: number = ( 6 * 72 ) + 190;
        const dialogRef = this.dialog.open( this.addDialogComponent,
        {
            data: { record:     edit_record,
                    mode:       'edit' },
        } );
        dialogRef.updateSize( '85%', height.toString() + 'px' );
        dialogRef.afterClosed().subscribe( result =>
        {
            console.log( 'editRecord() dialog result ', result );
            if ( result === 1 )
            {
                // When using an edit things are little different,
                // firstly we find record inside DataService by id
                console.log( 'editRecord() updating index ', foundIndex );
                // Then you update that record using data from
                // dialogData (values you entered)
                this.dataService.dataChange.value[ foundIndex ] = this.dataService.getDialogData();
                // And lastly refresh table
                this.refreshTable();
            }
            else
            {
                this.dataService.unlockRecord( edit_record );
            }
        } );
        return;
    }

    public pagingEvent( $event )
    {
        this.pageSize = $event.pageSize;
        localStorage.setItem( this.componentName + '.size', $event.pageSize );
        localStorage.setItem( this.componentName + '.index', $event.pageIndex );
        this.bot_paginator.length = $event.length;
        this.bot_paginator.pageSize = $event.pageSize;
        this.bot_paginator.pageIndex = $event.pageIndex;
        this.top_paginator.length = $event.length;
        this.top_paginator.pageSize = $event.pageSize;
        this.top_paginator.pageIndex = $event.pageIndex;
        this.paginatorEvent.emit( $event );
        return ( $event );
    }

    protected refreshTable(): void
    {
        this.bot_paginator._changePageSize( this.bot_paginator.pageSize );
        return;
    }

    public deleteRecord( i: number, delete_record: T, field_name: string = null, id = null ): void
    {
        this.id = id;
        this.lockRecord( delete_record );
        console.log( 'deleteRecord() ', delete_record );
        const dialogRef = this.dialog.open( this.delDialogComponent,
        {
            data: { record: delete_record,
                     label: delete_record[ field_name ] || null,
                     mode: 'delete' }
        } );

        dialogRef.afterClosed().subscribe( result =>
        {
            console.log( 'deleteItem() dialog result ', result );
            if ( result === 1 )
            {
                const foundIndex = this.dataService.dataChange.value.findIndex( x =>
                                    x[ 0 ] === this.id );
                console.log( 'deleteItem() removing index ', foundIndex );
                this.dataService.dataChange.value.splice( foundIndex, 0 );
                this.refreshTable();
            }
            else
            {
                this.unlockRecord( delete_record );
            }
        } );
        return;
    }

    public newRecord(){}
    public lockRecord( record: T ): void{}
    public unlockRecord( record: T ): void{}
    public loadData(): void{}
    public setFilter( filter: string ) {}
}
