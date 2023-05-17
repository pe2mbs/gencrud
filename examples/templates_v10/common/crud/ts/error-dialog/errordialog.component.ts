import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  	selector: 'app-root',
  	templateUrl: './errordialog.component.html'
})
export class ErrorDialogComponent 
{
  	title = 'Application error';
	constructor( private dialogRef: MatDialogRef<ErrorDialogComponent>, 
				 @Inject( MAT_DIALOG_DATA ) public data: any ) 
	{
		return;
	}
	  
	public closeDialog()
	{
		this.dialogRef.close( 0 );
		return;
	}
}
