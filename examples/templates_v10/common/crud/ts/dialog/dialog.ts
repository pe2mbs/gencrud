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
import { FormControl, FormGroup } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { GcCrudServiceBase } from '../crud/crud.service.base';
import { GcSubscribers } from '../subscribers';
import { isNullOrUndefined } from 'util';


export class GcBaseDialog extends GcSubscribers
{
    protected debug: boolean = false;
    public dialogRef: MatDialogRef<any>;
    public dataService: GcCrudServiceBase<any>;
    public formControl: FormControl;
    public formGroup: FormGroup;
    protected fixedValues: any = null;
    public mode: string;

	constructor( dialogRef: MatDialogRef<any>, 
				 dataService: GcCrudServiceBase<any>, 
				 mode: string = 'edit', 
				 fixed_values: any = null )
    {
        super();
        this.dialogRef = dialogRef;
        this.dataService = dataService;
        this.mode = mode;
        this.fixedValues = fixed_values;
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

    protected updateFixedValues(): void
    {
		console.log("this.fixedValues", this.fixedValues);
		if ( !isNullOrUndefined( this.fixedValues ) )
        {
        	if ( this.isEditMode() )
        	{
				// For the fixed value fields, they should be "readonly" !!!
				for (const [key, value] of Object.entries( this.fixedValues ) ) 
				{
					console.log( "KEY ", key );
					const ctrl = this.formGroup.get( key );
                	if ( ctrl != null )
                	{
                    	ctrl.disable( { onlySelf: true } );
                	}
				}
			}
			this.formGroup.patchValue( this.fixedValues );
        }
        return;
    }

    submit() 
    {
        // empty stuff
        return;
    }

    public onSaveClick(): void 
    {
        if ( this.debug )
        {
            console.log( 'onSaveClick() close' );
        }
        this.dialogRef.close( 1 );
        return;
    }

    public onCancelClick(): void 
    {
        if ( this.debug )
        {
            console.log( 'onCancelClick() close' );
        }
        this.dialogRef.close( 0 );
        return;
    }
}
