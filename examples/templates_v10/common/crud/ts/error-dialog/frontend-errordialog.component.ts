import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  	selector: 'app-root',
  	templateUrl: './errordialog.component.html'
})
export class FrontendErrorDialogComponent 
{
  	title = 'Frontend error';
	constructor( private dialogRef: MatDialogRef<FrontendErrorDialogComponent>, 
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
