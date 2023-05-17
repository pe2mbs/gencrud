import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material/dialog';


export interface MessageDialogData
{
	message: string;
	caption: string;
	reason?: string;
	status?: string;
}


@Component({
    // tslint:disable-next-line:component-selector
    selector: 'app-message-dialog-component',
    templateUrl: './message.dialog.component.html',
    styleUrls: [ './message.dialog.component.scss' ]
})
export class MessageDialogComponent
{
	constructor( public dialogRef: MatDialogRef<MessageDialogComponent>,
		@Inject( MAT_DIALOG_DATA ) public data: MessageDialogData ) 
	{
		return;
	}

	onCloseClick(): void 
	{
		this.dialogRef.close( false );
		return;
	}
}

export function MessageDialog( dialog: MatDialog, data: MessageDialogData )
{
	dialog.open( MessageDialogComponent, {
		width: '60%',
		data
	} );  
}

