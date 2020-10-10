import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { MatDialogRef, MatDialog } from '@angular/material';
import { ConfirmDialogComponent } from './confirm-dialog.component';
import { take, map } from 'rxjs/operators';

@Injectable({
    providedIn: 'root'
})
export class ConfirmDialogService 
{
    dialogRef: MatDialogRef<ConfirmDialogComponent>;

    constructor( private dialog: MatDialog ) 
    { 
        return;
    }

    public open( options: { title?: string, message: string, cancelText?: string, confirmText?: string } ) 
    {
        this.dialogRef = this.dialog.open( ConfirmDialogComponent, { data: options } );  
    } 

    public confirmed(): Observable<any> 
    {
        return this.dialogRef.afterClosed().pipe( take( 1 ), 
                                                  map( res => {
                return res;
            }
        ) );
    }
}
