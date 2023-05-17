/*
#
#   Python backend and Angular frontend code generation by gencrud
#   Copyright (C) 2018-2020 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   Library General Public License for more details.
#
#   You should have received a copy of the GNU Library General Public
#   License GPL-2.0-only along with this library; if not, write to the
#   Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301 USA
#
*/
import { Component,
         forwardRef, 
         Input, 
         OnInit} from '@angular/core';
import { NG_VALUE_ACCESSOR, 
         FormGroupDirective } from '@angular/forms';
import { FileInput } from 'ngx-material-file-input';
import { GcBaseComponent, CUSTOM_ANIMATIONS_CONTROLE } from './base.input.component';


export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef( () => GcFileUploadComponent ),
    multi: true
};

export interface BasicFile
{
    status: boolean;
    filename?: string;
    data?: ArrayBuffer | string;
};

@Component( {
    // tslint:disable-next-line:component-selector
    selector: 'gc-file-upload',
    template: `
    <app-base-input [template]="ref" [buttonPosition]="buttonPosition" [iconLeft]="iconLeft" [iconRight]="iconRight"
    [funcToEvaluateLeft]="funcToEvaluateLeft" [funcToEvaluateRight]="funcToEvaluateRight" [contextObject]="contextObject"
    [disableEdit]="disableEdit">
        <ng-template #ref>
            <div class="form">
                <mat-form-field color="accent">
                    <ngx-mat-file-input id="import.filename"
                    #removableInput
                    placeholder="File to upload" 
                    (change)="changedEvent( $event )"
                    [multiple]="multiple"
                    [(ngModel)]="fileInput"
                    [accept]="accept" class="fullwidth">
                    </ngx-mat-file-input>
                    <mat-icon matSuffix>folder</mat-icon>
                    <button mat-icon-button matSuffix *ngIf="!removableInput.empty" (click)="removableInput.clear($event)">
                        <mat-icon>clear</mat-icon>
                    </button>
                </mat-form-field>
            </div>
        </ng-template>
    </app-base-input>`,
    styles: [   'custom-input { width: 100%; }',
                'mat-form-field { width: 100%; }' ],
    providers: [ CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR ],
    animations: CUSTOM_ANIMATIONS_CONTROLE
} )

export class GcFileUploadComponent extends GcBaseComponent implements OnInit
{
    public fileInput: FileInput;
    public files: Array<BasicFile>;
    public fileName: string;

    @Input() accept: string = "*.*";
    @Input() multiple: boolean = false;
    constructor( formGroupDir: FormGroupDirective ) 
    {
        super( formGroupDir );
        this.debug = true;
        return;
    }

    public ngOnInit(): void {
        super.ngOnInit();
    }


    public changedEvent( event )
    {
        const reader = new FileReader();
        reader.onload = (e: any) => {
            //this.fileContent = e.target.result;
            this.files.push({
                status: true,
                filename: this.fileName,
                data:  e.target.result
            })
            //this.control.patchValue( this.files );
        };
        this.files = [];
        if (this.fileInput && this.fileInput.files.length > 0) {
            for (var inputFile of this.fileInput.files) {
                this.fileName = inputFile.name;
                reader.readAsText( inputFile );
            }
            this.control.patchValue( this.files );
        }
       
    }

}
