import { Component, OnInit, Inject, HostListener } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from "@angular/material";


@Component({
    selector: 'app-confirm-dialog',
    templateUrl: './confirm-dialog.component.html',
    styleUrls: ['./confirm-dialog.component.scss']
})
export class ConfirmDialogComponent implements OnInit 
{
    constructor( @Inject(MAT_DIALOG_DATA) public data: {
        cancelText?: string,
        confirmText?: string,
        message: string,
        title?: string
    }, private mdDialogRef: MatDialogRef<ConfirmDialogComponent> ) 
    { 
        if ( this.data.confirmText == undefined && this.data.cancelText == undefined )
        {
            this.data.confirmText = 'Ok';
        }
        return;
    }

    ngOnInit() 
    {
        return;
    }

    public cancel() 
    {
        this.close( false );
    }
  
    public close( value ) 
    {
        this.mdDialogRef.close( value );
    }
  
    public confirm() 
    {
        this.close( true );
    }
  
    @HostListener("keydown.esc") public onEsc() 
    {
        this.close( false );
    }
}
