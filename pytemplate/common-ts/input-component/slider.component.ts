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
    useExisting: forwardRef( () => PytSliderInputComponent ),
    multi: true
};

@Component( {
    selector: 'pyt-slider-input-box',
    template: `<div class="form">
    <mat-slider thumbLabel
                id="{{ id }}"
                [displayWith]="{{ formatLabel }}"
                tickInterval="{{ interval }}"
                min="{{ min }}"
                max="{{ max }}"
                [formControl]="control">
    </mat-slider>
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
export class PytSliderInputComponent extends PytBaseComponent
{
    @Input()    min;
    @Input()    max;
    @Input()    interval;
    @Input()    displayWith;

    constructor( formGroupDir: FormGroupDirective ) 
    {
        super( formGroupDir );
        return;
    }

    ngAfterViewInit()
    {
        super.ngAfterViewInit();
        if ( this.interval === '' || this.interval === null ||
                  this.interval === undefined )
        {
            this.interval = 1;
        }
        if ( this.min === '' || this.min === null ||
                  this.min === undefined )
        {
            this.min = 0;
        }
        if ( this.max === '' || this.max === null ||
                  this.max === undefined )
        {
            this.max = 100;
        }
        if ( this.displayWith === '' || this.displayWith === null ||
                  this.displayWith === undefined )
        {
            this.displayWith = 'formatLabel';
        }
        return;
    }
}
