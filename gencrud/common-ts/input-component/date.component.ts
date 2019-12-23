/*
#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2019 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation; either version 2 of the
#   License, or (at your option) any later version.
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
import { Component,
         forwardRef, Input } from '@angular/core';
import { NG_VALUE_ACCESSOR, 
         FormGroupDirective} from '@angular/forms';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { PytBaseComponent } from './base.input.component';
import * as moment_ from 'moment';

export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef( () => PytDateInputComponent ),
    multi: true
};

@Component( {
  selector: 'pyt-date-input-box',
  template: `<div class="form">
    <mat-form-field color="accent">
        <input id="{{ id }}_DATE"
                class="custom-input"
                matInput [matDatepicker]="datepicker"
                id="{{ id }}"
                [disabled]="readonly"
                placeholder="{{ placeholder }}"
                [formControl]="control"
                [min]="minDate"
                [max]="maxDate"
                (dateChange)="dateChange( $event )">
        <mat-datepicker-toggle matSuffix [for]="datepicker">
        </mat-datepicker-toggle>
        <mat-datepicker #datepicker
                        [disabled]="disabled"
                        [touchUi]="touchUi"
                        startView="{{startView}}">
        </mat-datepicker>
        <mat-icon matPrefix *ngIf="prefixType == 'icon'">{{ prefix }}</mat-icon>
        <mat-icon matSuffix *ngIf="suffixType == 'icon'">{{ suffix }}</mat-icon>
        <span matPrefix *ngIf="prefixType == 'text'">{{ prefix }}</span>
        <span matSuffix *ngIf="suffixType == 'text'">{{ suffix }}</span>
    </mat-form-field>
</div>`,
  styles: [   'custom-input { width: 100%; }',
                'mat-form-field { width: 100%; }' ],
  providers: [ CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR ],
  animations: [ trigger(
      'visibilityChanged', [
        state( 'true', style( { 'height': '*', 'padding-top': '4px' } ) ),
        state( 'false', style( { height: '0px', 'padding-top': '0px' } ) ),
        transition( '*=>*', animate( '200ms' ) )
      ]
    )
  ]
} )
export class PytDateInputComponent extends PytBaseComponent
{
    public                  maxDate: number;
    public                  minDate: number;
    public                  startView: string = 'month'; // | 'year' | 'multi-year';;
    public                  touchUi: boolean = false;
    // TODO: Check why thisis needed
    @Input( 'disabled' )    disabled: boolean = false;
    constructor( formGroupDir: FormGroupDirective ) 
    {
        super( formGroupDir );
        return;
    }

    public getDefaultValue(): any
    {
        return new Date();
    }

    public dateChange( $event )
    {
        return;
    }
}
