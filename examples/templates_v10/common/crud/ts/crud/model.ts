import { MatDialog } from '@angular/material/dialog';
import { Observable } from 'rxjs';
import { GcCrudServiceBase } from './crud.service.base';

export interface GcTableButton
{
	label:               string;
	icon?:               string;
	color?:              string;
	action?:             any;
	ngIf?:               string;
	disabled?:           string;
	directive?:          string;
	attributes?:         any;
}

export interface TableColumn2
{
	columnDef:          string;
	header:             string;
	display:            boolean;
	cell:               any;
	width?:             string;
	filter?:            boolean;
	filterField?:       string;
	sort?:              boolean;
	buttons?:           GcTableButton[];
	dataService?:       any;
	resolveList?:       GcSelectList[] | Observable<GcSelectList[]>;
	//resolveParams?:     ResolveParams;
	serviceRef?:        any;
}

export interface GcConditionItem
{
	value:              string;
	label:              string;
	param:              number;
}

export interface GcFilterColumnReq
{
	column:             string;
	value:              string | string[];
	operator:           string;
}

export interface GcChildFilter
{
	table: string;
	foreignKey: string;
	filters?: GcFilterColumnReq[];
	childFilters?: GcChildFilter[];
}


export interface GcCrudPageInfo
{
	pageIndex:          number;
	pageSize:           number;
	pageSizeOptions:    number[];
    filters:            GcFilterColumnReq[];
    sorting?:           GcSortingRequest;
}

export interface GcPagingData
{
	pageIndex:          number;
	pageSize:           number;
	recordCount:        number;
	records:            any[];
}

export interface GcSortingRequest
{
	column:             string|null;
    direction?:         'asc' | 'desc'; 
    disabled?:          boolean;
}

export interface GcPagingRequest
{
	pageIndex:          number;
	pageSize:           number;
	sorting?:           GcSortingRequest;
	filters?:           GcFilterColumnReq[];
	cacheDeactivator?:  number;
}

export interface GcBackEndInfo
{
    code:               number;
    name:               string;
    message:            string;
    url:                string;
    traceback:          any;
    request:            any;
}

export interface GcFilterColumn
{
    column:             string;
}

export interface GcBackendColumnSort
{
    column:             string;
}

export interface GcFilteredListReq
{
    page:               number;
    pageSize:           number;
    columns?:           GcFilterColumn[];
    columnSort?:        GcBackendColumnSort;
}

export interface GcFilteredList<T>
{
    page:               number;
    pageSize:           number;
    recordCount:        number;
    records:            T;
}

export interface GcSelectList
{
    value:              any;
    label:              string;
}

export interface VirtualScrollSort
{
    column:               string;                 // Sorting field
    direction:            string;                 // asc, desc
}

export interface VirtualScrollData
{
    value:                string;
    label:                string,
    page:                 number;                 // Page requested
    pageSize:             number;                 // Page size requested
    current?:             any | null;
    filter?:              string | null;
    count?:               number;                 // actual number of items in table
    last?:                boolean;                // last segement   
    sorting?:             VirtualScrollSort | null;
}

export interface VirtualScrollResponse
{
    data:                 VirtualScrollData;
    items:                GcSelectList[];
}

export interface GcTableFilter
{
	id:                   string;
	value:                any;
}

/*export interface ResolveParams
{
	service:    GcCrudServiceBase<any>;
	valueField: string; 
	labelField: string;
}*/

export interface TableDefintion<T>
{
	name:                 string;
	idField?:             string;
	title?:               string;
	helpTopic?:           string;
	defaultSortField:     string;
	defaultSortDirection: string;
	defaultFilter?:       GcFilterColumnReq[];
	autoUpdate?:          number;
	sortDisableClear:     boolean;
	dataService?:         GcCrudServiceBase<T>;
	resolveList?:         any;
	toggleUpdate?:        boolean;
	self?:                any;
	core?:                any;
	rowDoubleClick:       any;
	dialog?:              MatDialog;
	columns:              TableColumn2[];
	headerButtons?:       GcTableButton[];
	footerButtons?:       GcTableButton[];
}

export interface ApplicationInfo
{
    application: string;
    logo: string;
    version: string;
    ReleaseDate: string;
    plugins: Array<string>;
    theme: string;
}