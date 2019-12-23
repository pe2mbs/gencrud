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
         Input, 
         forwardRef, 
         AfterViewInit, 
         OnChanges, 
         ViewEncapsulation, 
         OnInit} from '@angular/core';
import { NG_VALUE_ACCESSOR, 
         ControlValueAccessor, 
         FormGroupDirective} from '@angular/forms';
import { PytBaseComponent, CUSTOM_ANIMATIONS_CONTROLE } from './base.input.component';


export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef( () => PytSliderToggleInputComponent ),
    multi: true
};

@Component( {
    selector: 'pyt-slidertoggle-input-box',
    template: `<div class="form">
    <mat-slide-toggle class="custom-input"
                  id="{{ id }}"
                  [color]="color"
                  [disabled]="readonly"
                  [labelPosition]="labelPosition"
                  [formControl]="control">
        {{ placeholder }}
    </mat-slide-toggle>
</div><br/>`,
    styles: [  'custom-input { width: 100%; }' ],
    providers: [ CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR ],
    animations: CUSTOM_ANIMATIONS_CONTROLE
} )
export class PytSliderToggleInputComponent extends PytBaseComponent
{
    @Input() labelPosition;

    constructor( formGroupDir: FormGroupDirective ) 
    {
        super( formGroupDir );
        return;
    }
}
