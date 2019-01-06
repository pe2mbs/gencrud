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
    useExisting: forwardRef( () => PytSlideToggleInputComponent ),
    multi: true
};

@Component( {
    selector: 'pyt-slidetoggle-input-box',
    template: `<div class="form">
    <mat-slide-toggle class="custom-input__input"
                  id="{{ id }}"
                  [formControl]="control">
        {{ placeholder }}
    </mat-slide-toggle>

    <mat-icon matPrefix *ngIf="prefixType == 'icon'">{{ prefix }}</mat-icon>
    <mat-icon matSuffix *ngIf="suffixType == 'icon'">{{ suffix }}</mat-icon>
    <span matPrefix *ngIf="prefixType == 'text'">{{ prefix }}</span>
    <span matSuffix *ngIf="suffixType == 'text'">{{ suffix }}</span>
</div><br/>`,
    styles: [   'custom-input__input{ width: 100%; }',
                'mat-form-field { width: 100%; }' ],
    encapsulation: ViewEncapsulation.None,
    providers: [ CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR ],
    animations: CUSTOM_ANIMATIONS_CONTROLE
} )
export class PytSlideToggleInputComponent extends PytBaseComponent
{
    constructor( formGroupDir: FormGroupDirective ) 
    {
        super( formGroupDir );
        return;
    }
}
