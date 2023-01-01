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
         AfterViewInit, 
         OnChanges, 
         ViewEncapsulation, 
         OnInit} from '@angular/core';
import { NG_VALUE_ACCESSOR, 
         ControlValueAccessor, 
         FormGroupDirective,
         FormControl } from '@angular/forms';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { PytBaseComponent } from './base.input.component';
import * as moment from 'moment';


export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef( () => PytLabelComponent ),
    multi: true
};

@Component( {
  selector: 'pyt-label-box',
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
export class PytLabelComponent extends PytBaseComponent
{
    @Input( 'pipe' )        pipe:   string = '';
    @Input( 'format' )      format: string = '';

    constructor( fGD: FormGroupDirective ) 
    {
        super( fGD );
        this.readonly = true
        // this.control.disable();
        return;
    }

    ngOnInit()
    {
        super.ngOnInit()
        this.readonly = true
        return;
    }

    onControlChange()
    {
        super.onControlChange();
        let value = this.control.value;
        if ( value != '' && this.pipe !== '' )
        {
            if ( this.pipe === 'datetime' )
            {
                let defFormat = "YYYY-MM-DD HH:mm:ss";
                var splitted = this.format.split(";", 2);
                if ( splitted.length > 0 )
                {
                    let idx = 0;
                    if ( splitted[ 0 ].length == 2 || splitted[ 0 ].length == 5 )
                    {
                        moment.locale( splitted[ 0 ] );
                        idx++;
                    }
                    if ( idx < splitted.length )
                    {
                        defFormat = splitted[ idx ];
                    }
                }
                let dt = moment( value );
                value = dt.format( defFormat );
                this.control.setValue( value, { emitEvent: false } );
            }
        }
        return;
    }
}
