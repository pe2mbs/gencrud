import { GcSubscribers } from "../../subscribers";
import { CrudDataService } from './crud-dataservice';
import { FormControl, FormGroup, FormBuilder } from '@angular/forms';
import { Input } from '@angular/core';
import { isNullOrUndefined } from 'util';
import { ActivatedRoute, Router } from '@angular/router';

export class ActionEvent<T>
{
    public Record: T;
    public Status: boolean;
    public Data: any;

    constructor( status: boolean, record: T = null, data: any = null )
    {
        this.Status = status;
        this.Record = record;
        this.Data = data;
    }
};


export class ScreenBaseComponent<T> extends GcSubscribers
{
    private callBack: ( event: ActionEvent<T> ) => any;
    public callBackData: any = null;
    public dataService: CrudDataService<T>
    public row: T;
    public formControl: FormControl;
    public formGroup: FormGroup;
    public mode: string;
    public sub: any;
    public tabIndex: number = 0;
    protected fixedValues: any = null;
    @Input( 'id' )      id: any;
    @Input( 'value' )   value: any;
    protected debug: boolean = false;

    constructor( public name: string
               , protected route: ActivatedRoute
               , protected router: Router )
    {
        super();
        return;
    }

    public ngOnInit(): void
    {
        const val = sessionStorage.getItem( `${this.name}.tabIndex` );
        if ( !isNullOrUndefined( val ) )
        {
            this.tabIndex = +val;
            // console.log( `${this.name}.tabIndex`, this.tabIndex );
        }
    }

    ngOnDestroy()
    {
        this.dataService.unlockRecord( this.row );
        super.ngOnDestroy();
        return;
    }

    public doInitialize( value: number, callback: ( event: ActionEvent<T> ) => any, data: any ): void
    {
        this.value = value;
        this.id = 'key';            // dummy value
        this.mode = 'edit';         // doInitialize only used for editing
        this.callBack = callback;
        this.callBackData = data;
        return;
    }

    protected updateFixedValues( fixed_values: any = null ): void
    {
        if ( fixed_values != null )
        {
            this.fixedValues = fixed_values;
        }
        if ( this.fixedValues != null )
        {
            for ( let key in this.fixedValues )
            {
                if ( key.endsWith( '_ID' ) )
                {
                    let value: number = +this.fixedValues[ key ];
                    let ctrl = this.formGroup.get( key );
                    if ( ctrl != null )
                    {
                        ctrl.setValue( value );
                        if ( !this.isEditMode() )
                        {
                            ctrl.disable( { onlySelf: true } );
                        }
                    }
                }
            }
        }
        return;
    }

    public onTabChange( $event ): void
    {
        this.tabIndex = $event;
        sessionStorage.setItem( `${this.name}.tabIndex`, this.tabIndex.toString() );
        // console.log( `${this.name}.tabIndex`, this.tabIndex );
        return;
    }

    public onSaveClick(): void
    {
        if ( !this.isEditMode() )
        {
            if ( this.fixedValues != null )
            {
                for ( let key in this.fixedValues )
                {
                    if ( key.endsWith( '_ID' ) )
                    {
                        let value: number = +this.fixedValues[ key ];
                        let ctrl = this.formGroup.get( key );
                        if ( ctrl != null )
                        {
                            ctrl.enable( { onlySelf: true } );
                            ctrl.setValue( value );
                        }
                    }
                }
            }
            this.dataService.addRecord( this.formGroup.value );
        }
        else
        {
            this.dataService.updateRecord( this.formGroup.value );
        }
        if ( isNullOrUndefined( this.callBack ) )
        {
            window.history.back();
        }
        else
        {
            this.callBack( new ActionEvent<T>( true, this.formGroup.value, this.callBackData ) );
        }
        return;
    }

    public onCancelClick(): void
    {
        if ( isNullOrUndefined( this.callBack ) )
        {
            window.history.back();
        }
        else
        {
            this.callBack( new ActionEvent<T>( false ) );
        }
        return;
    }

    public isEditMode(): boolean
    {
        return ( this.mode === 'edit' );
    }

    public getErrorMessage( ctrl_name: any ) : string
    {
        let ctrl = null;
        if ( typeof ctrl_name === 'string' )
        {
            ctrl = this.formGroup.get( ctrl_name );
        }
        else
        {
            ctrl = ctrl_name;
        }
        if ( ctrl == null || ctrl.valid )
        {
            return ( '' );
        }
        if ( this.debug )
        {
            console.log( 'getErrorMessage( ctrl_name = "' + ctrl_name + '" )' );
        }
        let result = 'Unknown error';
        if ( ctrl.hasError( 'required' ) )
        {
            result = 'Required field';
        }
        else if ( ctrl.hasError( 'email' ) )
        {
            result = 'Not a valid email';
        }
        else if ( ctrl.hasError( 'maxlength' ) )
        {
            result = 'The data is too long, allowed (' + ctrl.errors.maxlength.requiredLength + ')';
        }
        else if ( ctrl.invalid )
        {
            console.log( result, ctrl );
        }
        if ( this.debug )
        {
            console.log( "getErrorMessage() => " + result );
        }
        return ( result );
    }
}
