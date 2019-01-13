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
    <mat-slide-toggle class="custom-input__input"
                  id="{{ id }}"
                  [color]="color"
                  [labelPosition]="labelPosition"
                  [formControl]="control">
        {{ placeholder }}
    </mat-slide-toggle>
</div><br/>`,
    styles: [   'custom-input__input{ width: 100%; }',
                'mat-form-field { width: 100%; }' ],
    encapsulation: ViewEncapsulation.None,
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
