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
         OnInit,
         ChangeDetectionStrategy} from '@angular/core';
import { NG_VALUE_ACCESSOR, 
         ControlValueAccessor, 
         FormGroupDirective} from '@angular/forms';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { GcBaseComponent } from './base.input.component';
import { Router } from '@angular/router';
import { GcCrudServiceBase } from '../crud/crud.service.base';
import { GcSelectList } from '../crud/model';
import { isNullOrUndefined } from 'util';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef( () => GcChoiceAutoInputComponent ),
    multi: true
};

@Component( {
    // tslint:disable-next-line:component-selector
    selector: 'gc-choice-autocomplete-input',
    template: `<app-base-input [template]="ref" [serviceName]="serviceName" [serviceItem]="control ? control.value : ''"
     [buttonPosition]="buttonPosition" [iconLeft]="iconLeft" [iconRight]="iconRight" [dialog]="dialog"
     [funcToEvaluateLeft]="funcToEvaluateLeft" [funcToEvaluateRight]="funcToEvaluateRight" [contextObject]="contextObject"
     (editButtonClicked)="onEditButtonClick( $event )"
     [disableEdit]="disableEdit">
    <ng-template #ref><div class="form">
        <ng-select class="ng-select" id="{{ id }}" [items]="items" [(ngModel)]="itemValue" (clear)="onClear()" 
                                    [readonly]="readonly" [placeholder]="placeholder" [multiple]="false"
                                    (open)="onOpen( $event )" [appendTo]="'body'" [disabled]="disabled">
        </ng-select>
</div></ng-template></app-base-input>`,
    styleUrls: [ 'choice.scss' ],
    providers: [ CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR ],
    animations: [ trigger(
        'visibilityChanged', [
            state( 'true',  style( { 'height': '*',   'padding-top': '4px' } ) ),
            state( 'false', style( { 'height': '0px', 'padding-top': '0px' } ) ),
            transition( '*=>*', animate( '200ms' ) )
        ]
    ) ],
    encapsulation: ViewEncapsulation.None,
    changeDetection: ChangeDetectionStrategy.OnPush
} )
export class GcChoiceAutoInputComponent extends GcBaseComponent implements OnInit
{
    @Input( 'items')            items:      Array<GcSelectList> = [];
    @Input( 'subscribe' )       subscribe:  Observable<Array<GcSelectList>>;
    @Input() detail_button: string = null;
    @Input() detail_id:     string = null;
    public   selected: GcSelectList    = null;
    public   disabled = true;

    constructor( formGroupDir: FormGroupDirective, public router: Router, private http: HttpClient )
    {
        super( formGroupDir );
        return;
    }

    public ngOnInit(): void 
    {
        super.ngOnInit();
        if ( !isNullOrUndefined( this.subscribe ) )
        {
            this.subscribe.subscribe( data => {
                this.items = data
                if ( data.length > 0 ) this.itemValue = data[0];
                // emit event to update control
                // this.control.patchValue( this.control.value, { emitEvent: true } );
                this.change.emit( { value: this.control.value } );
                this.disabled = false
            } );
        } else {
            this.disabled = false;
        }
        return;        
    }

    public routeToDetail()
    {
        this.router.navigate( [ this.detail_button ], { queryParams: { id: this.detail_id,
                                                                       value: this.control.value,
                                                                       mode: 'edit' } } );
        return;
    }

    public onClear(): void
    {
        if ( this.debug )
        {
            console.log( 'Clear value in auto complete list');
        }
        this.control.setValue( null );
        return;
    }

    public onOpen( $event )
    {
        if ( this.debug )
        {
            console.log("onOpen ", $event, this.items );
        }
        return;
    }

    public getDefaultValue()
    {
        if ( this.debug )
        {
            console.log( 'base-getDefaultValue()' )
        }
        return ( '0' );
    }

    public get itemValue()
    {
        let result  = this.control.value;
        console.log(this.items)
        if ( Array.isArray( this.items ) )
        {
            this.items.forEach(element => {
                if ( element.value === this.control.value )
                {
                    result = element.label;
                    return result;
                }
            });
        }
        return ( result );
    }

    public set itemValue( value )
    {
        this.control.setValue( value.value );
        return;
    }
}
