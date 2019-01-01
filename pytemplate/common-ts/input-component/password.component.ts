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
    useExisting: forwardRef( () => PytPasswordInputComponent ),
    multi: true
};

@Component( {
  selector: 'pyt-password-input-box',
  template:`<div class="form">
  <mat-form-field color="accent">
    <input matInput 
           type="password"
           class="custom-input__input" 
           id="{{ id }}"
           placeholder="{{ placeholder }}"
           [type]="hide ? 'password' : 'text'"
           [formControl]="control"/>
    <mat-icon matSuffix (click)="hide = !hide">
        {{hide ? 'visibility' : 'visibility_off'}}
    </mat-icon>
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
export class PytPasswordInputComponent extends PytBaseComponent
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