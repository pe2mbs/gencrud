import { Component, OnInit, Input, Inject } from '@angular/core';
import { Observable } from 'rxjs';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { HelpInformationData } from '../model';

@Component({
    selector: 'app-help-dialog',
    template: `
    <h2 mat-dialog-title>
        <div fxLayout="row">
            <div fxFlex="95" fxLayoutAlign="center">Help information page</div>
            <div fxFlex="5" fxLayoutAlign="end">
                <button id="button-login" mat-icon-button (click)="closeHelp()">
                    <mat-icon aria-label="Help" class="material-icons">close</mat-icon>
                </button>
            </div>
        </div>
    </h2>
    <div class="mat-typography">
        <markdown [data]="helpInfo.text" class="mat-markdown"></markdown>
    </div>`,
    styleUrls: [ './help-dialog.component.scss' ]
} )
export class GcHelpDialogComponent implements OnInit
{
    public helpInfo: HelpInformationData = { text: "No Help", help: "no_help" } ;
    constructor( public dialogRef: MatDialogRef<GcHelpDialogComponent>
               , @Inject( MAT_DIALOG_DATA ) public data: Observable<HelpInformationData> )
    {
        dialogRef.disableClose = true;
        data.subscribe( result => {

            this.helpInfo = result;
        } );
        return;
    }

    public ngOnInit(): void
    {
        return;
    }

    public closeHelp(): void
    {
        this.dialogRef.close();
        return;
    }
}
