import { FormControl, FormGroup } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { CrudDataService } from './crud-dataservice';
import { GcSubscribers } from '../../subscribers';


export class BaseDialog extends GcSubscribers
{
    protected debug: boolean = false;
    public dialogRef: MatDialogRef<any>;
    public dataService: CrudDataService<any>;
    public formControl: FormControl;
    public formGroup: FormGroup;
    protected fixedValues: any = null;
    public mode: string;

    constructor( dialogRef: MatDialogRef<any>, dataService: CrudDataService<any>, mode: string = 'edit', fixed_values: any = null )
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

    protected updateFixedValues(): void
    {
        if ( this.fixedValues != null )
        {
            this.formGroup.patchValue( this.fixedValues );
        }
        if ( this.isEditMode() )
        {
            // For the fixed value fields, they should be "readonly" !!!
            for ( let key in this.fixedValues )
            {
                let ctrl = this.formGroup.get( key );
                if ( ctrl != null )
                {
                    ctrl.disable( { onlySelf: true } );
                }
            }
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
