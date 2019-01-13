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
    template: `<div class="form custom-input__input">
    {{ placeholder }}
    <mat-slider id="{{ id }}"
                class="custom-input__input"
                [thumbLabel]="thumbLabel"
                [vertical]="vertical"
                [disabled]="disabled"
                [invert]="invert"
                [step]="step"
                [tickInterval]="interval"
                [color]="color"
                [min]="min"
                [max]="max"
                [formControl]="control">
    </mat-slider>
</div><br/>`,
    styles: [   'custom-input__input{ width: 100%; }',
                'mat-form-field { width: 100%; }',
                '.mat-slider-horizontal { width: 100%; }',
                '.mat-slider-vertical { height: 300px; }' ],
    encapsulation: ViewEncapsulation.None,
    providers: [ CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR ],
    animations: CUSTOM_ANIMATIONS_CONTROLE
} )
export class PytSliderInputComponent extends PytBaseComponent
{
    @Input()    min;
    @Input()    max;
    @Input()    interval;
    @Input()    thumbLabel;
    @Input()    vertical;
    @Input()    disabled;
    @Input()    invert;
    @Input()    step;

    constructor( formGroupDir: FormGroupDirective ) 
    {
        super( formGroupDir );
        this.Init();
        return;
    }

    ngAfterViewInit()
    {
        super.ngAfterViewInit();
        this.Init();
        return;
    }

    Init()
    {
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
        if ( this.vertical === '' || this.vertical === null ||
                  this.vertical === undefined )
        {
            this.vertical = false;
        }
        if ( this.disabled === '' || this.disabled === null ||
                  this.disabled === undefined )
        {
            this.disabled = false;
        }
        if ( this.invert === '' || this.invert === null ||
                  this.invert === undefined )
        {
            this.invert = false;
        }
        if ( this.step === '' || this.step === null ||
                  this.step === undefined )
        {
            this.step = 1;
        }
        if ( this.thumbLabel === '' || this.thumbLabel === null ||
                  this.thumbLabel === undefined )
        {
            this.thumbLabel = true;
        }
        if ( this.debug )
        {
            console.log( 'this.interval', this.interval );
            console.log( 'this.min', this.min );
            console.log( 'this.max', this.max );
            console.log( 'this.vertical', this.vertical );
            console.log( 'this.disabled', this.disabled );
            console.log( 'this.invert', this.invert );
            console.log( 'this.step', this.step );
            console.log( 'this.thumbLabel', this.thumbLabel );
        }
        return;
    }
}
