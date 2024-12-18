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
import { Component, Input,  forwardRef } from '@angular/core';
import { NG_VALUE_ACCESSOR, FormGroupDirective } from '@angular/forms';
import { GcBaseComponent, CUSTOM_ANIMATIONS_CONTROLE } from './base.input.component';


export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef( () => GcCheckboxInputComponent ),
    multi: true
};


@Component( {
    // tslint:disable-next-line:component-selector
    selector: 'gc-checkbox-input',
    template: `<div class="form">
    <mat-checkbox class="custom-input__input" id="{{ id }}" [color]="color" [attr.readonly]="readonly" [attr.readonly]="disabled"
                  [labelPosition]="labelPosition" [(indeterminate)]="indeterminate" [formControl]="control">
        {{ placeholder }}
    </mat-checkbox>
</div><br/>`,
    styles: [   'custom-input { width: 100%; }',
                'mat-form-field { width: 100%; }' ],
    providers: [ CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR ],
    animations: CUSTOM_ANIMATIONS_CONTROLE
} )
export class GcCheckboxInputComponent extends GcBaseComponent
{
    @Input() labelPosition = 'after';
    @Input() indeterminate = false;

    constructor( formGroupDir: FormGroupDirective ) 
    {
        super( formGroupDir );
        return;
    }
}
