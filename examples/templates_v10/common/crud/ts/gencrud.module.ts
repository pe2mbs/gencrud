/*#
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
#*/
// Angular modules
import { NgModule, ModuleWithProviders, CUSTOM_ELEMENTS_SCHEMA, SecurityContext } from '@angular/core';
import { CommonModule, HashLocationStrategy, LocationStrategy } from '@angular/common';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';
import { BrowserModule } from '@angular/platform-browser';
import { OverlayModule } from '@angular/cdk/overlay';
import { CdkTreeModule } from '@angular/cdk/tree';
import { PortalModule } from '@angular/cdk/portal';
import { Route, RouterModule } from '@angular/router';
import { ScrollingModule } from '@angular/cdk/scrolling';
// Other modules
import { MonacoEditorModule } from 'ngx-monaco-editor';
import { MarkdownModule } from 'ngx-markdown';
import { GridsterModule } from 'angular-gridster2';
import { NgSelectModule } from '@ng-select/ng-select';
import { NgxMaterialTimepickerModule } from 'ngx-material-timepicker';
import { MaterialFileInputModule } from 'ngx-material-file-input';

// Material cmodules
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatButtonModule } from '@angular/material/button';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatChipsModule } from '@angular/material/chips';
import { MatRippleModule, DateAdapter, MAT_DATE_FORMATS, MatNativeDateModule } from '@angular/material/core';
import { MatDividerModule } from '@angular/material/divider';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatPaginatorModule, MatPaginatorIntl } from '@angular/material/paginator';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatSortModule } from '@angular/material/sort';
import { MatTableModule } from '@angular/material/table';
import { MatTabsModule } from '@angular/material/tabs';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTreeModule } from '@angular/material/tree';
import { MatBadgeModule } from '@angular/material/badge';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatRadioModule } from '@angular/material/radio';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatSliderModule } from '@angular/material/slider';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatPasswordStrengthModule } from '@angular-material-extensions/password-strength';
import { MatMomentDateModule } from '@angular/material-moment-adapter';
import { MessageDialogComponent } from './message-dialog/message.dialog.component';
import { GcBaseComponent } from './input/base.input.component';
import { EditTableButtonComponent } from './input/edit-table/edit-table-button.component';
import { JiraButtonComponent } from '../components/jira/jira-button.component';
import { TabSelectButtonComponent } from '../components/tab-select/tab-select-button.component'
import { CompareFilesButtonComponent } from '../components/compare-files/compare-files-button-component';
import { DeleteButtonComponent } from '../components/delete/delete-button.component';
import { DialogDeleteFilterComponent } from '../components/delete/filter-dialog.component';
// Gencrud components
import { GcFileUploadComponent } from './input/fileupload.component';
import { GcTextInputComponent } from './input/textbox.component';
import { GcChoiceInputComponent } from './input/choice.component';
import { GcChoiceBasicInputComponent } from './input/choice.basic.component';
import { GcChoiceAutoInputComponent } from './input/choice.auto.component';
import { GcComboInputComponent } from './input/combobox.component';
import { GcDateInputComponent } from './input/date.component';
import { GcDatePickerInputComponent } from './input/date.picker.component';
import { GcDateTimeInputComponent } from './input/datetime.component';
import { GcDateTimePickerInputComponent } from './input/datetime.picker.component';
import { GcNumberInputComponent } from './input/number.component';
import { GcPasswordInputComponent } from './input/password.component';
import { GcEmailInputComponent } from './input/email.component';
import { GcTextareaInputComponent } from './input/textarea.component';
import { GcTimeInputComponent } from './input/time.component';
import { GcTimePickerInputComponent } from './input/time.picker.component';
import { GcLabelComponent } from './input/label.component';
import { GcCheckboxInputComponent } from './input/checkbox.component';
import { GcContextMenuComponent } from './input/context-menu/context.menu.component';
import { GcSliderToggleInputComponent } from './input/slidertoggle.component';
import { GcSliderInputComponent } from './input/slider.component';
import { GcMonacoEditorComponent } from './input/monaco.component';
import { GcFilterHeaderComponent, GcFilterItemDirective } from './crud/filter-header.component';
import { GcClickStopPropagation } from './click-stop-propagation';
import { GcDefaultComponent } from './default.component';
import { GcHeaderComponent } from './header/header.component';
import { GcFooterComponent } from './footer.component';
import { GcNavSidebarComponent } from './nav/sidebar.component';
import { GcHelpComponent } from './help/help.component';
import { GcHelpService } from './help/help-service';
import { GcHelpDialogComponent } from './help/help-dialog/help-dialog.component';
import { GcMenuListItemComponent } from './nav/menu.item.component/item.component';
import { GcMenuBarComponent } from './top-menu-bar/menu-bar.component';
import { GcMenuComponent } from './top-menu-bar/menu-item/menu.component';
import { GcNavService } from './nav/nav.service';
import { GcTickerComponent } from './ticker/ticker.component';
import { GcTickerDataService } from './ticker/service';
import { GcDeleteDialog } from './dialog/delete.dialog';
import { CustDataTableComponent } from './crud/cust.data.table.component';
import { RowExtraButtonsComponent } from './crud/row-extra-buttons';
import { ErrorDialogComponent } from './error-dialog/errordialog.component';
import { FrontendErrorDialogComponent } from './error-dialog/frontend-errordialog.component';
import { BackendErrorDialogComponent } from './error-dialog/backend-errordialog.component';
import { ErrorDialogService } from './error-dialog/errordialog.service';
import { GcChoiceVirtualInputComponent } from './input/choice.virtual.component';
import { SelectDefaultEnvironmentComponent } from './select-default-environment/select-default-environment.component';
import { DefaultEnvironmentService } from './select-default-environment/default-environment.service';
import { LabelRequiredDirective } from './required.directive';
// deprecated components
// import { CrudDataService } from './crud/deprecated/crud-dataservice';
// import { CrudDataSource } from './crud/deprecated/crud-datasource';
// import { ScreenBaseComponent } from './crud/deprecated/crud-screen-component';
// import { TableBaseComponent } from './crud/deprecated/crud-table-component';
// import { BaseDialog } from './crud/deprecated/dialog';
// import { SpinnerService } from './crud/deprecated/spinner-service';

const defaultRoute: Route = { 	
	path: '',
	component: GcDefaultComponent
};

const importExportModules = [
	OverlayModule,
	PortalModule,
	CdkTreeModule,
	ScrollingModule,
	MatAutocompleteModule,
	MatButtonModule,
	MatCardModule,
	MatCheckboxModule,
	MatChipsModule,
	MatDividerModule,
	MatExpansionModule,
	MatIconModule,
	MatInputModule,
	MatListModule,
	MatMenuModule,
	MatProgressSpinnerModule,
	MatProgressBarModule,
	MatPaginatorModule,
	MatRippleModule,
	MatSelectModule,
	MatSidenavModule,
	MatSnackBarModule,
	MatSortModule,
	MatTableModule,
	MatTabsModule,
	MatToolbarModule,
	MatFormFieldModule,
	MatButtonToggleModule,
	MatTreeModule,
	MatBadgeModule,
	MatGridListModule,
	MatRadioModule,
	MatDatepickerModule,
	MatMomentDateModule,
	MatTooltipModule,
	MatSlideToggleModule,
	MatSliderModule,
	MatDialogModule,
    MatPasswordStrengthModule,
	FlexLayoutModule,
	NgSelectModule,
	NgxMaterialTimepickerModule,
	MaterialFileInputModule
];

const declareExportComponents = [
	SelectDefaultEnvironmentComponent,
	MessageDialogComponent,
	GcBaseComponent,
	EditTableButtonComponent,
	GcTextInputComponent,
	GcChoiceInputComponent,
	GcChoiceBasicInputComponent,
    GcChoiceAutoInputComponent,
	GcChoiceVirtualInputComponent,
	GcComboInputComponent,
	GcContextMenuComponent,
	GcDateInputComponent,
	GcDatePickerInputComponent,
	GcDateTimeInputComponent,
	GcDateTimePickerInputComponent,
	GcNumberInputComponent,
	GcPasswordInputComponent,
	GcTextareaInputComponent,
	GcMonacoEditorComponent,
	GcTimeInputComponent,
	GcTimePickerInputComponent,
	GcEmailInputComponent,
	GcLabelComponent,
	GcCheckboxInputComponent,
	GcSliderToggleInputComponent,
	GcSliderInputComponent,
	GcFilterHeaderComponent,
	GcClickStopPropagation,
	GcFilterItemDirective,
	GcHeaderComponent,
	GcFooterComponent,
	GcNavSidebarComponent,
	GcHelpComponent,
	GcHelpDialogComponent,
	GcMenuListItemComponent,
	GcMenuBarComponent,
	GcMenuComponent,
	GcDefaultComponent,
	GcTickerComponent,
	GcDeleteDialog,
	CustDataTableComponent,
	ErrorDialogComponent,
	JiraButtonComponent,
	TabSelectButtonComponent,
	RowExtraButtonsComponent,
	CompareFilesButtonComponent,
	DeleteButtonComponent,
	DialogDeleteFilterComponent,
    LabelRequiredDirective,
	GcFileUploadComponent
];

@NgModule({
    declarations: [
		...declareExportComponents,
		ErrorDialogComponent,
		FrontendErrorDialogComponent,
		BackendErrorDialogComponent
    ],
    entryComponents: [
		MessageDialogComponent,
		GcHelpDialogComponent,
		GcDeleteDialog,
		ErrorDialogComponent,
		FrontendErrorDialogComponent,
		BackendErrorDialogComponent,
		JiraButtonComponent,
		TabSelectButtonComponent,
		DialogDeleteFilterComponent
	],
    providers: [
		DefaultEnvironmentService,
		GcHelpService,
		GcNavService,
		MatDatepickerModule,
		GcTickerDataService,
		ErrorDialogService,
		{
		  provide: LocationStrategy,
		  useClass: HashLocationStrategy
		},
		GcHelpService,  
        {
            provide: MatDialogRef,
            useValue: {
            }
        },
	],
	schemas: [ CUSTOM_ELEMENTS_SCHEMA ],
    imports: [
		CommonModule,
		BrowserModule,
        FormsModule,
        ReactiveFormsModule,
		MonacoEditorModule.forRoot(),
		MarkdownModule.forRoot(),
		RouterModule.forChild( [ defaultRoute ] ),
		//	sanitize: SecurityContext.NONE
		//} ),
		GridsterModule,
		...importExportModules
    ],
    exports: [
		...declareExportComponents,
		...importExportModules
    ]
})
export class GenCrudModule
{
    static forChild(): ModuleWithProviders<GenCrudModule>
    {
        return { ngModule: GenCrudModule };
    }
}
