import { Component, ViewChild, Input, OnChanges, EventEmitter, OnInit, AfterViewInit, HostListener, OnDestroy } from '@angular/core';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { MatSort, SortDirection, MatSortable } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { isNullOrUndefined, isNull } from 'util';
import { merge, of as observableOf } from 'rxjs';
import { startWith, switchMap, map, catchError } from 'rxjs/operators';
import { HttpErrorResponse } from '@angular/common/http';
import { GcFilterEvent, GcFilterRecord } from './filter.record';
import { GcCrudServiceBase } from './crud.service.base';
import { GcCrudPageInfo, TableDefintion } from './model';
import { GcDeleteDialog } from '../dialog/delete.dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { GcContextMenuModel } from '../input/context-menu/context.menu.component';
import { environment } from 'src/environments/environment';
import { GcSubscribers } from '../subscribers';


class CustPageEvent extends PageEvent{
	cacheDeactivator?: number;
}

@Component({
  selector: 'app-cust-data-table',
  templateUrl: 'cust.data.table.component.html',
  styleUrls: [ '../common-mat-card.scss' ]
})
export class CustDataTableComponent extends GcSubscribers implements OnInit, AfterViewInit, OnChanges, OnDestroy
{
	@Input()    definition: TableDefintion<any>;  
	@Input()    id: string;
	@Input()    value: any;
    @Input()    mode: string = "edit";
	@Input()    displayedColumns: string[] = null;

	@ViewChild( 'bot_paginator', { static: true }) bot_paginator: MatPaginator;
	@ViewChild( MatSort, { static: true }) sort: MatSort;
	protected debug: boolean = false;
	public dataService: GcCrudServiceBase<any>;
	public dataSource: MatTableDataSource<any>;
	public paginatorEvent: EventEmitter<CustPageEvent> = new EventEmitter<CustPageEvent>();
	public filterRecord: GcFilterRecord = null;
	public resultsLength: number = 0;
	public isLoadingResults: boolean = true;
	public pageData: GcCrudPageInfo = { pageIndex: 0, pageSizeOptions: [ 5,10,20,50,100 ], pageSize: 20, filters: [] };
	// public displayedColumns: string[] = null;
	public self: CustDataTableComponent;
	public filterField = '';
    public toggleUpdate: boolean = false;
    private updateSubscription: any;    // NodeJS.Timer

	isDisplayContextMenu: boolean;
	rightClickMenuItems: Array<GcContextMenuModel> = [];
	rightClickMenuPositionX: number;
	rightClickMenuPositionY: number;
	contextMenuData: any;
	constructor( protected dialog: MatDialog, public route: ActivatedRoute )
	{
		super();
		this.debug = true;
        this.dataSource = new MatTableDataSource<any>();
		return;
	}

	private isPageEvent( event: any )
	{
		const pev: PageEvent = event as PageEvent;
		return ( pev && !isNullOrUndefined( pev.pageIndex ) );
	}

	private isFilterEvent( event: any )
	{
		const fev: GcFilterEvent = event as GcFilterEvent;
		return ( fev && !isNullOrUndefined( fev.filter ) );
	}

	ngOnInit() 
	{	
		this.registerSubscription(
			this.route.queryParams.subscribe( params => {
				if (params.mode && params.mode == 'filter') {
					if (params.id) this.id = params.id;    // Contains the key field, currently only the primary key is supported.
					if (params.value) this.value = params.value; // Contains val value for the key field.
					if (params.mode) this.mode = params.mode;  // edit or new, filter only supported on the table component.
				}
			})
		);
		this.self = this.definition.self;
		const filterFields = new Array<string>();
		if ( this.debug )
		{
			console.log( `mode: ${this.mode} id: ${this.id} value: ${this.value}` );
		}
		if ( this.mode === 'filter' )
		{
			// Custom filter, need to remove the column from the view
			//this.filterField = this.id;
		}
		if (isNullOrUndefined(this.displayedColumns) || this.displayedColumns.length == 0) {
			this.displayedColumns = new Array<string>();
			this.definition.columns.forEach( elem => {
				if ( this.debug )
				{
					console.log( 'ngOnChanges => ', elem );
				}
				if ( elem.display && this.filterField !== elem.columnDef )
				{
					this.displayedColumns.push( elem.header );
				}
			} );
		}
		this.definition.columns.forEach( elem => {
			if ( elem.filter )
			{
				filterFields.push( elem.filterField != null ? elem.filterField : elem.columnDef );
			}
		} );
        if ( !isNullOrUndefined( this.definition.defaultSortField ) )
        {
            this.pageData.sorting = {
                column: this.definition.defaultSortField,
                direction: this.definition.defaultSortDirection as 'asc' | 'desc',
                disabled: this.definition.sortDisableClear
			};
        }
		// restore settings stored for the table previously
		this.restoreView();
		// however, the id filter for the record comes in afterward
        this.filterRecord = new GcFilterRecord( filterFields );
		if ( !isNullOrUndefined( this.filterRecord ) && this.mode === 'filter' )
		{
			this.filterRecord.set( this.id, this.value );
			// disable visual filter option for the user on the column
			// that filters on the screen record id
			this.definition.columns.forEach(column => {
				if (column["columnDef"] == this.id) {
					column["filter"] = false;
				}
			})
		}
		// set further default filters to apply regardless of the mode
		this.updateDefaultFilter();

		// set page data
		this.dataService = this.definition.dataService;
        this.setPageData( this.pageData );
		// call ngOnDestroy on refresh
		window.onbeforeunload = () => this.ngOnDestroy();
		return;
	}

	public ngOnChanges(): void
	{
		if ( this.debug )
		{
			console.log( 'ngOnChanges' );
		}
		if ( !isNullOrUndefined( this.filterRecord ) && this.mode === 'filter' )
		{
			this.filterRecord.set( this.id, this.value );
            this.filterRecord.event.emit();
		}
		return;
	}

	ngOnDestroy(): void
	{
		this.storeView();
		this.stopAutoUpdate();
		return;
	}

	public setFilterRecord(key: string, value: any, operator: string = "EG") {
		if (this.filterRecord) {
			this.filterRecord.set( key, value );
			this.filterRecord.event.emit( null );
			//this.refresh();
		}
	}

	public updateDefaultFilter() {
		if ( this.definition.defaultFilter != null ) {
			const self = this.definition.self;
			for ( var filter of this.definition.defaultFilter ) {
				this.filterRecord.set( filter.column, eval( String( filter.value) ), filter.operator )
			}
		}
	}

	public refresh(): void
	{
		if ( this.debug )
		{
			console.log( 'GcTableBase.refresh' );
		}
		const o     = new CustPageEvent();
		o.pageIndex = this.bot_paginator.pageIndex;
		o.pageSize  = this.bot_paginator.pageSize;
		o.length    = this.bot_paginator.length;
		o.previousPageIndex = this.bot_paginator.pageIndex;
		this.stopAutoUpdate();
		o.cacheDeactivator = (new Date()).getTime();
		this.paginatorEvent.emit( o );
		return;
	}

    protected stopAutoUpdate(): void
    {
        if ( this.toggleUpdate )
        {
            console.log( 'stopAutoUpdate' );
            clearInterval( this.updateSubscription );
            this.toggleUpdate = false;
            this.updateSubscription = null;
        }
        return;
    }

    public toggleAutoUpdate(): void
    {
        if ( !this.toggleUpdate )
        {
            let pollIntervalLocal: number = environment.pollInterval * 1000;
            this.toggleUpdate = true;
            if ( this.definition.autoUpdate < 10 )
            {
                pollIntervalLocal = 10000;
            }
            else if ( this.definition.autoUpdate < 60 )
            {
                pollIntervalLocal = this.definition.autoUpdate;
            }
            this.updateSubscription = setInterval( () => {
                console.log( "trigger-auto-update", this.toggleUpdate );
                this.filterRecord.event.emit( null );
            }, pollIntervalLocal );
        }
        else
        {
            this.stopAutoUpdate();
        }
        console.log( "toggleUpdate", this.toggleUpdate );
        return;
    }

	protected setPaginator( paginator: MatPaginator, o: PageEvent ): void
	{
		paginator.pageIndex = o.pageIndex;
		paginator.pageSize  = o.pageSize;
		paginator.length    = o.length;
		return;
	}

	public pagingEvent( $event, source: string )
	{
		this.setPaginator( this.bot_paginator, $event );
        this.updatePageInfo( $event.pageIndex, $event.pageSize );
        this.paginatorEvent.emit( $event );
		return;
	}

    protected setPageData( o: GcCrudPageInfo ): void
	{
        console.log( 'setPageData', o );
		this.bot_paginator.pageIndex    = o.pageIndex;
		this.bot_paginator.pageSize     = o.pageSize;
        this.filterRecord.setFilters( o.filters );
        this.pageData.sorting = o.sorting;
        
        // this.sort.active    = this.pageData.sorting.column;
        // this.sort.direction = this.pageData.sorting.direction as SortDirection;
        // this.sort.disabled  = this.pageData.sorting.disabled;

        /*
        *   I managed to make it work with the following ugly hack:
        *   https://github.com/angular/components/issues/10242
        */
        const d: MatSortable = {    id:             this.pageData.sorting.column,
                                    start:          this.pageData.sorting.direction as any,
                                    disableClear:   true };
        this.sort.active = this.pageData.sorting.column;
        this.sort.sort( d );
		this.sort.active = this.pageData.sorting.column;
        this.dataSource.sort = this.sort;
        // // ugly hack!
        // const activeSortHeader = this.sort.sortables.get( this.pageData.sorting.column );
        // // tslint:disable-next-line:no-string-literal
        // activeSortHeader[ '_setAnimationTransitionState' ]({
        //     fromState: this.pageData.sorting.direction,
        //     toState: 'active',
        // });
        console.log( 'sorting change: ', d, ' TO ', this.sort );
		return;
    }
    
    private updatePageInfo( pageIndex: number, pageSize: number )
    {
        this.pageData.pageIndex         = pageIndex;
		this.pageData.pageSize          = pageSize;  
        this.pageData.filters           = this.filterRecord.getFilters();
        if ( isNullOrUndefined( this.pageData.sorting ) )
        {
            this.pageData.sorting = {
                column: this.getSortFieldByLabel( this.sort.active ),
                direction: this.sort.direction as any,
                disabled: this.sort.disabled
            }
        }
        else
        {
            this.pageData.sorting.column    = this.getSortFieldByLabel( this.sort.active );
            this.pageData.sorting.direction = this.sort.direction as "desc" | "asc";
            this.pageData.sorting.disabled  = this.sort.disabled;
        }
        return;
    }


	protected getSortFieldByLabel( label: string ): string
	{
		// tslint:disable-next-line:prefer-for-of
		for ( let idx = 0; idx < this.definition.columns.length; idx++ )
		{
			const element = this.definition.columns[ idx ];
			if ( this.debug )
			{
				console.log( "Element:", element, label );
			}
			if ( element.filterField != null ) {
				if ( element.header === label || element.filterField === label || element.columnDef === label ) {
					return element.filterField;
				}
			} else if ( element.header === label || element.columnDef === label )
			{
				return element.columnDef;
			}
		}
		return this.definition.columns[ 0 ].columnDef;
	}

	public ngAfterViewInit(): void
	{
		if ( this.debug )
		{
			console.log( 'GcTableBase.ngAfterViewInit' );
		}
		this.registerSubscription(
			merge( this.paginatorEvent, this.sort.sortChange, this.filterRecord.event )
				.pipe( startWith( {} ),
					switchMap( ($event) => {
						let cacheDeactivator = null;
						if ( $event instanceof CustPageEvent || this.isPageEvent( $event ) )
						{
							const event = $event as CustPageEvent;
							if ( this.debug )
							{
								console.log( "GcTableBase.PageEvent", event );
							}
							this.pageData.pageIndex = event.pageIndex;
							this.pageData.pageSize = event.pageSize;
							cacheDeactivator = event.cacheDeactivator;
						}
						// reset pageIndex to 0 on any filter event!
						if ( $event instanceof GcFilterEvent || this.isFilterEvent( $event ) )
						{
							this.pageData.pageIndex = 0;
						}
						if ( this.debug )
						{
							console.log( `GcTableBase.req.index: ${this.pageData.pageIndex} length: ${this.resultsLength}` );
						}
						this.isLoadingResults = true;
						this.updatePageInfo( this.pageData.pageIndex, this.pageData.pageSize );
						return ( this.dataService.getPage( this.pageData.pageIndex,
														this.pageData.pageSize,
														this.pageData.sorting.direction,
														this.pageData.sorting.column, 
														this.filterRecord,
														cacheDeactivator ) );
					} ),
					map( (data: any ) => {
						// Flip flag to show that loading has finished.
						this.isLoadingResults = false;
						this.resultsLength = data.recordCount;
						if ( this.debug )
						{
							console.log( `GcTableBase.map.index: ${this.pageData.pageIndex} length: ${this.resultsLength}` );
							console.log( 'GcTableBase.data.records', data.records );
							console.log( 'GcTableBase.data.recordCount', data.recordCount );
							console.log( 'GcTableBase.isLoadingResults', this.isLoadingResults );
						}
						return ( data.records );
					} ),
					catchError( err => {
						if ( err instanceof HttpErrorResponse ) 
						{
							if ( err.status === 422 || err.status === 401 ) 
							{
								// This some what brute force, just to avoid injecting the router
								window.location.href = '/#/login';
								return;
							}
						}
						console.error( "GcTableBase.catchError", err );
						this.isLoadingResults = false;
						return observableOf( [] );
					} 
				)
			).subscribe( ( data: any[] ) => {
				this.dataSource.data = data;
			} )
		);
		return;
	}

	public deleteRecord( idx: number, row: any, idField: string, title: any = null ): void
	{
		if ( this.debug )
		{
			console.log( 'CustDataTableComponent.deleteRecord( idx = ', idx, 
						 ", row = ", row, 
						 ", idField = ", idField,
						 ", header = ", title, " )" );
		}

		this.dataService.lockRecord( row );
		const dialogConfig = new MatDialogConfig();
		dialogConfig.disableClose = true;
		dialogConfig.width = "auto";
		dialogConfig.data = { record: row,
			title: title,
			id: idField,
			value: row[ idField ] || null,
			mode: 'delete',
			service: this.dataService 
		};
        const dialogRef = this.dialog.open( GcDeleteDialog, dialogConfig );
		this.registerSubscription(
			dialogRef.afterClosed().subscribe( result =>
			{
				if ( this.debug )
				{
					console.log( 'deleteItem() dialog result ', result );
				}
				this.dataService.unlockRecord( row );
				setTimeout(() => this.refresh(), 0);
			} )
		);
		return;
    }
    
	displayContextMenu(event, data)
	{
		this.contextMenuData = data;
		this.isDisplayContextMenu = true;
		this.rightClickMenuItems = [
		    {
			    menuText: 'Copy',
			    menuEvent: 'Copy to Clipboard',
		    }
		];
	
		this.rightClickMenuPositionX = event.clientX;
		this.rightClickMenuPositionY = event.clientY;
	
	}
	
	getRightClickMenuStyle()
	{
    return { position: 'fixed',
		     left: `${this.rightClickMenuPositionX}px`,
		     top: `${this.rightClickMenuPositionY}px` }
	}
	
	handleMenuItemClick(event) {
		switch (event.data) {
		case this.rightClickMenuItems[0].menuEvent:
		    // ugly workaround, create textarea and then copy to
			// clipboard, since Angular 8 does not support clipboard
			// cdk directive yet
			var TempText = document.createElement("input");
			TempText.value = this.contextMenuData["copy"];
			document.body.appendChild(TempText);
			TempText.select();
			document.execCommand("copy");
			document.body.removeChild(TempText);
			break;
		}
	}
	
	@HostListener('document:click')
	documentClick(): void {
	    this.isDisplayContextMenu = false;
	}

    public ngIfCondition( row: any, condition: string ): boolean
    {
        if ( condition !== undefined )
        {
            const self = this.self;
            return eval( condition );
        }
        return ( true );
    }

    public storeView(): void
    {
		// when the table is shown inside a screen, we will store its settings separately
		let config = "";
		if (this.mode == "filter") config += "-filter-id" + this.value;
		if (!isNullOrUndefined(this.definition.dialog)) config += "-dialog";

		if (this.mode == "filter") {
			// do not include the row filter that selects the rows for a screen
			this.pageData.filters = this.pageData.filters.filter(item => !item.column.endsWith("_ID"))
		}

		sessionStorage.setItem( this.definition.name + config, JSON.stringify( this.pageData ) );
		localStorage.setItem( this.definition.name + config + "-pageSize", JSON.stringify( this.pageData.pageSize ) );		
        return;
    }

    public restoreView(): void
    {
		let data = null;
		let pageSize = null;
		let config = "";
		if (this.mode == "filter") config += "-filter-id" + this.value;
		if (!isNullOrUndefined(this.definition.dialog)) config += "-dialog";

		data = sessionStorage.getItem( this.definition.name + config );
		pageSize = localStorage.getItem( this.definition.name + config + "-pageSize" )
        if ( !isNullOrUndefined( data ) )
        {
            this.pageData = JSON.parse( data );
        }
		if ( !isNullOrUndefined( pageSize ) )
        {
            this.pageData.pageSize = JSON.parse( pageSize );
        }
        return;
    }
}
