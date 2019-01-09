import { FormControl, FormGroup } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { CrudDataService } from './crud-dataservice';


export class BaseDialog
{
    protected debug: boolean = false;
    public dialogRef: MatDialogRef<any>;
    public dataService: CrudDataService<any>;
    public formControl: FormControl;
    public formGroup: FormGroup;
    public mode: string;

    constructor( dialogRef: MatDialogRef<any>, dataService: CrudDataService<any>, mode: string = 'edit' ) 
    {
        this.dialogRef = dialogRef;
        this.dataService = dataService;
        this.mode = mode;
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

    submit() 
    {
        // emppty stuff
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
