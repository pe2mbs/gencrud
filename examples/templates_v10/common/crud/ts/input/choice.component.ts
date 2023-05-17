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
import { Component, Input, forwardRef, OnInit, ViewChild, AfterViewInit, NgZone, OnDestroy } from '@angular/core';
import { NG_VALUE_ACCESSOR, FormGroupDirective } from '@angular/forms';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { GcBaseComponent } from './base.input.component';
import { GcSelectList } from '../crud/model';
import { GcCrudServiceBase } from '../crud/crud.service.base';
import { isNullOrUndefined } from 'util';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, fromEvent } from 'rxjs';
import {filter, map, pairwise, scan, throttleTime, debounceTime, distinctUntilChanged} from 'rxjs/operators';
import { NgSelectComponent } from '@ng-select/ng-select';
import { GcFilterRecord } from '../crud/filter.record';

export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef( () => GcChoiceInputComponent ),
    multi: true
};

@Component( {
    // tslint:disable-next-line:component-selector
    selector: 'gc-choice-input',
    template: `<app-base-input [template]="ref" [serviceName]="serviceName"
    [serviceItem]="control ? control.value : ''" [buttonPosition]="buttonPosition" [iconLeft]="iconLeft" [iconRight]="iconRight"
    [funcToEvaluateLeft]="funcToEvaluateLeft" [funcToEvaluateRight]="funcToEvaluateRight" [contextObject]="contextObject"
    [disableEdit]="disableEdit">
    <ng-template #ref>
        <ng-select #ngSelect class="ng-select" id="ngSelect-{{ id }}" [(ngModel)]="itemValue" (clear)="onClear()" 
                            [readonly]="readonly" [placeholder]="placeholder" [multiple]="false"
                            (open)="onOpen( $event )" [appendTo]="'body'" [disabled]="disabled"
                            [loading]="loading" [virtualScroll]="true" [searchFn]="searchFunction"
                            [openOnEnter]="false" [keyDownFn]="keyDownHandler" (keydown.Enter)="initFilter($event, this)">
            <ng-option *ngFor="let option of options$ | async" [value]="option.value">
                {{option.label}}
            </ng-option>
        </ng-select>
        <!--<div class="spinner-item">
            <mat-progress-spinner [mode]="'indeterminate'" [diameter]="50"></mat-progress-spinner>
        </div>-->
    </ng-template></app-base-input>`,
    styleUrls: [ 'choice.scss' ],
    providers: [ CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR ],
    animations: [ trigger(
        'visibilityChanged', [
            state( 'true', style( { 'height': '*', 'padding-top': '4px' } ) ),
            state( 'false', style( { height: '0px', 'padding-top': '0px' } ) ),
            transition( '*=>*', animate( '200ms' ) )
        ]
    ) ]
} )
export class GcChoiceInputComponent extends GcBaseComponent implements OnInit, AfterViewInit, OnDestroy
{
    @Input()    service:        GcCrudServiceBase<any> | null = null;  
    @Input()    labelField:     string | null = null;
    @Input()    valueField:     string | null = null;
    @Input()    filterDict:     any;

    @ViewChild('ngSelect', { static: false }) ngSelect: NgSelectComponent;

    pageSize = 30;
    pageIndex = 0;
    total = 1000;

    public      selected:                any;
    public      loading:                 boolean = false;
    public      initialLoaded:           boolean = false;
    public      resetObserver:           boolean = false;
    public      searchMode:              boolean = false;
    public      filter:                  GcFilterRecord = null;

    options = new BehaviorSubject<GcSelectList[]>([]);
    options$: Observable<GcSelectList[]>;
    
    constructor( formGroupDir: FormGroupDirective, private http: HttpClient ) 
    {
        super( formGroupDir );
        this.initSubscription();
        window.onbeforeunload = () => this.ngOnDestroy();
        return;
    }

    public initSubscription() {
        // create observable for the options list that concats new items with old on each next() call
        const subscription = this.options.asObservable().pipe(
            scan((acc, curr) => {
                if (this.resetObserver) {
                    this.resetObserver = false;
                    return curr;
                }
                return [...acc, ...curr];
            }, [])
        );
        this.options$ = subscription;
    }

    public ngOnInit()
    {
        super.ngOnInit();
        return;
    }

    public initColumnFilter() {
        if ( this.filterDict != null ) {
            try {
                this.filter = new GcFilterRecord( Object.keys( this.filterDict ) );
                for ( let key of Object.keys( this.filterDict ) ) {
                    if ( typeof this.filterDict[key] == "string" ) {
                        const value = (this.filterDict[key] as String);
                        if ( value.startsWith("row.") ) {
                            this.filter.set(key, this.contextObject.row[value.slice(4)], 'EQ');
                        }
                    } else {
                        this.filter.set(key,  this.filterDict[key], 'EQ');
                    }
                }
            } catch (e) {
                console.log(e)
            }
        }
    }

    public ngAfterViewInit(): void {
        this.registerSubscription(
            this.ngSelect.scroll.pipe(debounceTime(200), distinctUntilChanged()).subscribe( (event) => {
                if ( event.end != null && event.end >= ((this.pageIndex - 1) * this.pageSize + this.pageSize * 0.5 ) && (this.pageIndex * this.pageSize < this.total) ) {
                    if ( this.debug ) {
                        console.log("fetch more!", event.end, this.pageIndex * this.pageSize);
                    }
                    this.fetchMore();
                }
            })
        );
    }

    public ngOnDestroy(): void {
        this.options.unsubscribe();
    }

    public onOpen( $event )
    {
        if ( this.debug )
        {
            console.log("onOpen ", $event, this.options );
        }
        return;
    }

    public onClear(): void
    {
        if ( this.debug )
        {
            console.log( 'Clear value in auto complete list');
        }
        this.control.setValue( 0 );
        // reset filter and observer to load again without filter
        //this.filter = null;
        this.filter.clear( this.labelField )
        this.searchMode = false;
        this.resetObserver = true;
        this.pageIndex = 0;
        this.fetchMore();
        return;
    }

    public fetchMore() {
        let result = [];
        if ( this.service != null ) {
            if ( this.pageIndex == 0 && !this.initialLoaded ) {
                this.initialLoaded = true;
                this.initColumnFilter();
            }
            this.pageIndex += 1;
            this.service.getSelectList( this.valueField, this.labelField, null, null, this.filter, null,
                { pageSize: this.pageSize, pageIndex: this.pageIndex - 1}, this.control.value).toPromise().then( (data: any) => {
                // this.items = data.itemList;
                result = data.itemList;
                this.total = data.totalItems;
                this.loading = false;
                this.options.next(result);
            } );
        }
    }

    public searchFunction(term: string, item: any): boolean {
        return true;
    }

    public keyDownHandler($event: any): boolean {
        console.log($event)
        if ( $event.key == "Enter" ) {
            $event.preventDefault();
            $event.stopPropagation();
            return false;
        }
        return true;
    }

    public initFilter($event, context): void {
        var target = $event.target;
        // access the id value of the ngSelect
        const searchTerm = target.value;
        if ( searchTerm != null ) {
            // reset variables for filter
            this.searchMode = true;
            this.pageIndex = 0;
            this.resetObserver = true;
            // set the current filter based on the record
            if ( this.filter == null ){
                this.filter = new GcFilterRecord([this.labelField]);
            }
            this.filter.set(this.labelField, searchTerm.toLocaleLowerCase(), "CO");
            this.fetchMore();
        }
    }

    public get itemValue()
    {
        let result  = this.control.value;
        if ( result != 0 && !this.initialLoaded ) {
            this.initialLoaded = true;
            this.initColumnFilter();
            this.fetchMore();
        } else if ( result == 0 || result == null || result == "" ) {
            return "No " + (this.placeholder != "" ? this.placeholder : "item selected");
        }
        return ( result );
    }

    public set itemValue( value )
    {
        if ( value != null ) {
            this.control.setValue( value );
        }
        return;
    }
}
