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
import { Component, Input, forwardRef, OnInit } from '@angular/core';
import { NG_VALUE_ACCESSOR, FormGroupDirective } from '@angular/forms';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { GcBaseComponent } from './base.input.component';
import { GcSelectList } from '../crud/model';
import { GcCrudServiceBase } from '../crud/crud.service.base';
import { isNullOrUndefined } from 'util';
import { HttpClient } from '@angular/common/http';

export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef( () => GcChoiceBasicInputComponent ),
    multi: true
};

@Component( {
    // tslint:disable-next-line:component-selector
    selector: 'gc-choice-base-input',
    template: `<app-base-input [template]="ref" [serviceName]="serviceName"
    [serviceItem]="control ? control.value : ''" [buttonPosition]="buttonPosition" [iconLeft]="iconLeft" [iconRight]="iconRight"
    [funcToEvaluateLeft]="funcToEvaluateLeft" [funcToEvaluateRight]="funcToEvaluateRight" [contextObject]="contextObject"
    [disableEdit]="disableEdit">
    <ng-template #ref>
    <div class="form">
    <mat-form-field color="accent">
        <mat-select [(value)]="selected"
                    class="custom-input__input"
                    id="{{ id }}"
                   [attr.readonly]="readonly"
                   [attr.readonly]="disabled"
                    placeholder="{{ placeholder }}"
                    [formControl]="control">
            <mat-option *ngFor="let item of items" [value]="item.value">
                {{item.label}}
            </mat-option>
        </mat-select>
        <mat-icon matPrefix *ngIf="prefixType == 'icon'">{{ prefix }}</mat-icon>
        <mat-icon matSuffix *ngIf="suffixType == 'icon'">{{ suffix }}</mat-icon>
        <span matPrefix *ngIf="prefixType == 'text'">{{ prefix }}</span>
        <span matSuffix *ngIf="suffixType == 'text'">{{ suffix }}</span>
    </mat-form-field>
</div>
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
export class GcChoiceBasicInputComponent extends GcBaseComponent implements OnInit
{
    @Input()    items:          GcSelectList[];
    
    @Input()    service:        GcCrudServiceBase<any> | null = null;  
    @Input()    labelField:     string | null = null;
    @Input()    valueField:     string | null = null;
    @Input()    serviceUri:     string | null = null;

    public      selected:       any;
    public      loading:        boolean = false;
    
    constructor( formGroupDir: FormGroupDirective, private http: HttpClient ) 
    {
        super( formGroupDir );
        return;
    }

    public ngOnInit()
    {
        super.ngOnInit();
        if ( !isNullOrUndefined( this.service ) )
        {
            if ( this.debug )
            {
                console.log( `Loading from service : ${this.valueField}: ${this.labelField}` );
            }
            this.loading = true;
            // We got the service 
            this.registerSubscription( this.service.getSelectList( this.valueField, this.labelField
                                        ).subscribe( dataList => {
                this.items = dataList;
                this.loading = false;
            } ) );
        }
        else if ( !isNullOrUndefined( this.serviceUri ) )
        {
            this.loading = true;
            if ( this.debug )
            {
                console.log( `Loading from url ${this.serviceUri} : ${this.valueField}: ${this.labelField}` );
            }
            this.http.post<GcSelectList[]>( this.serviceUri, { value: this.valueField, label: this.labelField } 
                                        ).subscribe( data => {
                this.items = data;
                this.loading = false;
            });
        }
        else
        {
            if ( this.debug )
            {
                if ( this.items ) console.log( `Items provided: ${this.items.length}` );
            }
        }
        return;
    }
}
