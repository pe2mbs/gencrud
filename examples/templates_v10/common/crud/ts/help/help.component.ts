import { Component, Input, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { GcHelpDialogComponent } from './help-dialog/help-dialog.component';
import { GcHelpService } from './help-service';
import { Overlay } from '@angular/cdk/overlay';
import { HelpInformationData } from './model';

@Component( {
    // tslint:disable-next-line:component-selector
    selector: 'gc-help',
    template: `<button mat-icon-button [color]="colorTheme" id="help-button" style="float: right;"
                                       [matTooltip]="helpLabel"
                                       (click)="onHelpClick()"><mat-icon aria-label="Help">help_outline</mat-icon>
                                       </button>`,
    styleUrls: []
} )
export class GcHelpComponent implements OnInit
{
    @Input()    helpitem:  string;
    @Input()    fallback:  string;
    @Input()    colorTheme: string = "primary";
    private     helpData:  HelpInformationData;
    public      helpLabel: string  = 'Help';


    constructor( public helpService: GcHelpService
               , public dialog: MatDialog
               , private overlay: Overlay )
    {
        this.helpData = null;
        return;
    }

    public ngOnInit(): void
    {
        this.helpLabel = `Help ${this.helpitem.replace( '-', ' ' ).replace( '_', ' ' )}`;
        return;
    }

    public onHelpClick(): void
    {
        const dialogRef = this.dialog.open( GcHelpDialogComponent, {
                data: this.helpService.getHelp( this.helpitem, this.fallback ),
                autoFocus: false,
                panelClass: 'custom-dialog-container'
            } );
        dialogRef.updateSize( '85%', '85%' );
        return;
    }
}
