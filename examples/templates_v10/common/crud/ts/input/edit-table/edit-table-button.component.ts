import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Router } from '@angular/router';
import { isNullOrUndefined } from 'util';


@Component({
    selector: 'app-edit-table-button',
    template: `<button  *ngIf="dialog" mat-icon-button color="primary" [id]="serviceName" [value]="value"
                        [name]="serviceName" [disabled]="disabled"
                        [matTooltip]="tooltip" (click)="onClick( $event )"
                        matDialogClose>
                    <mat-icon>{{ icon }}</mat-icon>
                </button>
                <button  *ngIf="!dialog" mat-icon-button color="primary" [id]="serviceName" [value]="value"
                                        [name]="serviceName" [disabled]="disabled"
                                        [matTooltip]="tooltip" (click)="onClick( $event )">
                    <mat-icon>{{ icon }}</mat-icon>
                </button>`,
    styles: [ '' ]
})
export class EditTableButtonComponent 
{
    @Input( 'id' )                  id: string;
    @Input( 'value' )               value: number;
    @Input( 'serviceName' )         serviceName: string;
    @Input( 'tooltip' )             tooltip: string;
    @Input( 'disabled' )            disabled: boolean = false;
    @Input( 'icon' )                icon: string;
    @Input( 'func' )                func: string;
    @Input( 'self' )                self: any;
    @Input( 'dialog' )              dialog: boolean = false;
    @Output( 'editButtonClicked' )  editButtonClicked: EventEmitter<any> = new EventEmitter<any>(); 

    constructor( public router: Router ) 
    { 
        return;
    }

    public onClick( $event )
    {
        this.editButtonClicked.emit( $event );
        if (!isNullOrUndefined(this.func) && !isNullOrUndefined(this.self)) {
            // execute (mixin) method for passed function
            const self = this.self;
            return eval(this.func);
        }
        else {
            // default behavior, redirect to service screen
            console.log("*****", this.serviceName, this.value)
            this.router.navigate(['/' + this.serviceName + '/edit'], { queryParams: { id: this.id, mode: 'edit', value: this.value } });
        }
    }
}