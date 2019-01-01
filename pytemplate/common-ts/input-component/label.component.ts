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
    useExisting: forwardRef( () => PytLabelComponent ),
    multi: true
};

@Component( {
  selector: 'pyt-label-box',
  template:`<div class="form">
    <mat-form-field color="accent">
        <input  matInput 
                class="custom-input__input" 
                readonly
                id="{{ id }}"
                placeholder="{{ placeholder }}"
                [formControl]="control"/>
        <mat-icon matPrefix *ngIf="prefixType == 'icon'">{{ prefix }}</mat-icon>
        <mat-icon matSuffix *ngIf="suffixType == 'icon'">{{ suffix }}</mat-icon>
        <span matPrefix *ngIf="prefixType == 'text'">{{ prefix }}</span>
        <span matSuffix *ngIf="suffixType == 'text'">{{ suffix }}</span>
        <mat-hint *ngIf="hint != ''">{{ hint }}</mat-hint>
        <mat-error *ngIf="error_message != ''">
            {{ error_message }}
        </mat-error>
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
export class PytLabelComponent extends PytBaseComponent
                               implements ControlValueAccessor, 
                                          AfterViewInit, 
                                          OnChanges, OnInit 
{
    constructor( fGD: FormGroupDirective ) 
    {
        super( fGD );
        return;
    }
}