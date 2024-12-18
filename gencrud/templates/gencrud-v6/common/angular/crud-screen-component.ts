import { Subscribers } from "./subscribers";
import { CrudDataService } from './crud-dataservice';
import { FormControl, FormGroup, FormBuilder } from '@angular/forms';
import { Input, OnDestroy } from '@angular/core';



export class ScreenBaseComponent<T> extends Subscribers implements OnDestroy
{
    public dataService: CrudDataService<T>;
    public row: T;
    public formControl: FormControl;
    public formGroup: FormGroup;
    public mode: string;
    public sub: any;
    protected fixedValues: any = null;
    @Input() id: any;
    @Input() value: any;
    protected debug: boolean = false;

    constructor()
    {
        super();
        return;
    }

    public ngOnDestroy()
    {
        this.dataService.unlockRecord( this.row );
        super.ngOnDestroy();
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
            for ( const key in this.fixedValues )
            {
                if ( key.endsWith( '_ID' ) )
                {
                    const value: number = +this.fixedValues[ key ];
                    const ctrl = this.formGroup.get( key );
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

    public onSaveClick(): void
    {
        if ( !this.isEditMode() )
        {
            if ( this.fixedValues != null )
            {
                for ( const key in this.fixedValues )
                {
                    if ( key.endsWith( '_ID' ) )
                    {
                        const value: number = +this.fixedValues[ key ];
                        const ctrl = this.formGroup.get( key );
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
        window.history.back();
        return;
    }

    public onCancelClick(): void
    {
        window.history.back();
        return;
    }

    public isEditMode(): boolean
    {
        return ( this.mode === 'edit' );
    }

    public getErrorMessage( ctrl_name: any ): string
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
