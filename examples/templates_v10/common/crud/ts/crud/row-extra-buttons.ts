import { Component, Input, OnInit } from '@angular/core';
import { CustDataTableComponent } from './cust.data.table.component';

@Component({
    selector: 'app-row-extra-button',
    template: `
    <ng-container [ngSwitch]="directive">
        <app-compare-files-button
        *ngSwitchCase="'app-compare-files-button'"
        [cssClass]="cssClass"
        [id]="attributes.id"
        [value]="attributes.value"
        [record]="record"
        [advancedTIOCMode]="attributes.advancedTIOCMode"
        [table]="table"
        [tooltip]="attributes.tooltip">
        </app-compare-files-button>

        <app-jira-button
        *ngSwitchCase="'app-jira-button'"
        [cssClass]="cssClass"
        [id]="attributes.id"
        [value]="attributes.value"
        [name]="attributes.name"
        [issueID]="attributes.issueID"
        [tooltip]="attributes.tooltip">
        </app-jira-button>

        <app-delete-button
        *ngSwitchCase="'app-delete-button'"
        [cssClass]="cssClass"
        [id]="attributes.id"
        [value]="attributes.value"
        [record]="record"
        [tooltip]="attributes.tooltip">
        [column]="attributes.column"
        [table]="attributes.table"
        [discriminateColumn]="attributes.discriminateColumn"
        [disabled]="attributes.disabled">
        </app-delete-button>

        <app-screen-tab-select-button
        *ngSwitchCase="'app-screen-tab-select-button'"
        [cssClass]="cssClass"
        [id]="attributes.id"
        [icon]="attributes.icon"
        [record]="record"
        [route]="attributes.route"
        [useCachedRecord]="attributes.useCachedRecord"
        [tabIndex]="attributes.tabIndex"
        [tooltip]="attributes.tooltip">
        </app-screen-tab-select-button>
    </ng-container>
    `,
    styles: [ '' ]
})
export class RowExtraButtonsComponent
{
    @Input( 'directive' )           directive: string;
    @Input( 'attributes' )          attributes: any = {};
    @Input( 'record' )              record: any = {};
    @Input( 'cssClass' )            cssClass: string;
    @Input( 'table' )               table: CustDataTableComponent;

    constructor() {}

}
