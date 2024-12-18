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
import { Component,
         Input, 
         forwardRef, 
		 OnInit } from '@angular/core';
import { NG_VALUE_ACCESSOR, 
         FormGroupDirective } from '@angular/forms';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { GcBaseComponent } from './base.input.component';
import * as moment from 'moment';
import { toLocalTimeString } from 'src/app/addons/date-parser';


export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef( () => GcLabelComponent ),
    multi: true
};

@Component( {
  // tslint:disable-next-line:component-selector
  selector: 'gc-label',
  template: `<div class="form">
    <mat-form-field color="accent">
        <input  matInput 
                class="custom-input__input"
               [attr.readonly]="readonly"
               [attr.readonly]="disabled"
                id="{{ id }}"
                placeholder="{{ placeholder }}"
                [formControl]="control"/>
        <mat-icon matPrefix *ngIf="prefixType == 'icon'">{{ prefix }}</mat-icon>
        <mat-icon matSuffix *ngIf="suffixType == 'icon'">{{ suffix }}</mat-icon>
        <span matPrefix *ngIf="prefixType == 'text'">{{ prefix }}</span>
        <span matSuffix *ngIf="suffixType == 'text'">{{ suffix }}</span>
        <mat-hint *ngIf="hint != ''">{{ hint }}</mat-hint>
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
export class GcLabelComponent extends GcBaseComponent implements OnInit
{
    @Input()      pipe: string = '';
    @Input()      format: string;

    constructor( fGD: FormGroupDirective ) 
    {
        super( fGD );
        this.readonly = true;
        // this.control.disable();
        return;
    }

    ngOnInit()
    {
        super.ngOnInit();
        this.readonly = true;
        return;
    }

    onControlChange()
    {
        super.onControlChange();
        let value = this.control.value;
        if ( value !== '' && this.pipe !== '' )
        {
            if ( this.pipe === 'datetime' )
            {
                const dtString = toLocalTimeString(value, this.format || "") || ""
                this.control.setValue( dtString, { emitEvent: false } );
            }
        }
        return;
    }
}
