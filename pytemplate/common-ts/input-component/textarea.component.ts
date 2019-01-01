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
import { trigger, state, style, transition, animate } from '@angular/animations';
import { PytBaseComponent } from './base.input.component';

export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef( () => PytTextareaInputComponent ),
    multi: true
};

@Component( {
  selector: 'pyt-textarea-input-box',
  template:`<div class="form">
  <mat-form-field color="accent">
    <textarea matInput
           rows="{{ rows }}" cols="{{ cols }}" 
           class="custom-input__input" 
           id="{{ id }}"
           placeholder="{{ placeholder }}"
           [formControl]="control">
           {{ value }}
    </textarea>
  </mat-form-field>
</div>`,
  styles: [ 'custom-input__input{ width: 100%; }',
            'mat-form-field { width: 100%; }' ],
  encapsulation: ViewEncapsulation.None,
  providers: [ CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR ],
  animations:[ trigger(
      'visibilityChanged',[
        state( 'true', style( { 'height':'*','padding-top':'4px' } ) ),
        state( 'false', style( { height:'0px','padding-top':'0px' } ) ),
        transition( '*=>*', animate( '200ms' ) )
      ]
    )
  ]
} )
export class PytTextareaInputComponent extends PytBaseComponent
                                       implements ControlValueAccessor, 
                                                  AfterViewInit, 
                                                  OnChanges, OnInit 
{
    constructor( formGroupDir: FormGroupDirective ) 
    {
        super( formGroupDir );
        return;
    }
}