import { Injectable } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ErrorDialogComponent } from './errordialog.component';
import { BackendErrorDialogComponent } from './backend-errordialog.component';
import { FrontendErrorDialogComponent } from './frontend-errordialog.component';

@Injectable()
export class ErrorDialogService 
{
	public isDialogOpen: boolean = false;
	dialogRef: MatDialogRef<any> = null;
	constructor( public dialog: MatDialog ) 
	{ 
		return;
	}

	protected handleDialog( dialogRef: any )
	{
		if ( this.isDialogOpen ) 
		{
            return ( false );
        }
		this.isDialogOpen = true;
		this.dialogRef = dialogRef;
        dialogRef.afterClosed().subscribe( result => {
            console.log( 'The dialog was closed' );
			this.isDialogOpen = false;
			this.dialogRef = null;
        });
		return ( true );
	}

	openDialog( data ): boolean
	{
		return ( this.handleDialog( this.dialog.open( ErrorDialogComponent, {
            width: '50%',
            // tslint:disable-next-line:object-literal-shorthand
			data: data,
			disableClose: true
        } ) ) );
	}
	
	public openDialogBackendError( error: any ): boolean
	{
		return ( this.handleDialog( this.dialog.open( BackendErrorDialogComponent, {
            width: '50%',
            // tslint:disable-next-line:object-literal-shorthand
            data: error,
			disableClose: true
        } ) ) );
	}

	public openDialogFrontendError( error: any ): boolean
	{
		return ( this.handleDialog( this.dialog.open( FrontendErrorDialogComponent, {
            width: '50%',
            // tslint:disable-next-line:object-literal-shorthand
            data: error,
			disableClose: true
        } ) ) );
	}
}
