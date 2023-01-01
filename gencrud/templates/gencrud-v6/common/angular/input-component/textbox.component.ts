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
         FormGroupDirective} from '@angular/forms';
import { PytBaseComponent, CUSTOM_ANIMATIONS_CONTROLE } from './base.input.component';


export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef( () => PytTextInputComponent ),
    multi: true
};

@Component( {
    selector: 'pyt-text-input-box',
    template: `<div class="form">
    <mat-form-field color="accent">
        <input  matInput 
                class="custom-input"
                id="{{ id }}"
                [attr.readonly]="readonly"
                [attr.readonly]="disabled"
                placeholder="{{ placeholder }}"
                [formControl]="control"/>
        <mat-hint *ngIf="hint !== undefined">{{ hint }} </mat-hint>
        <mat-error *ngIf="error !== undefined && error === true"> {{ GetErrorMessage() }} </mat-error>
        <mat-icon matPrefix *ngIf="prefixType == 'icon'">{{ prefix }}</mat-icon>
        <mat-icon matSuffix *ngIf="suffixType == 'icon'">{{ suffix }}</mat-icon>
        <span matPrefix *ngIf="prefixType == 'text'">{{ prefix }}</span>
        <span matSuffix *ngIf="suffixType == 'text'">{{ suffix }}</span>
    </mat-form-field>
</div>`,
    styles: [   'custom-input { width: 100%; }',
                'mat-form-field { width: 100%; }' ],
    providers: [ CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR ],
    animations: CUSTOM_ANIMATIONS_CONTROLE
} )
export class PytTextInputComponent extends PytBaseComponent
{
    constructor( formGroupDir: FormGroupDirective ) 
    {
        super( formGroupDir );
        this.debug = true;
        return;
    }
}
