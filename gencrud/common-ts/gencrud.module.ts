import { NgModule, ModuleWithProviders } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PytTextInputComponent } from './input-component/textbox.component';
import { PytChoiceInputComponent } from './input-component/choice.component';
import { PytComboInputComponent } from './input-component/combobox.component';
import { PytDateInputComponent } from './input-component/date.component';
import { PytDateTimeInputComponent } from './input-component/datetime.component';
import { PytNumberInputComponent } from './input-component/number.component';
import { PytPasswordInputComponent } from './input-component/password.component';
import { PytEmailInputComponent } from './input-component/email.component';
import { PytTextareaInputComponent } from './input-component/textarea.component';
import { PytTimeInputComponent } from './input-component/time.component';
import { PytLabelComponent } from './input-component/label.component';
import { PytCheckboxInputComponent } from './input-component/checkbox.component';
import { PytSliderToggleInputComponent } from './input-component/slidertoggle.component';
import { PytSliderInputComponent } from './input-component/slider.component';
import { CustomMaterialModule } from '../material.module';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { NgxMaterialTimepickerModule } from 'ngx-material-timepicker';
import { MatButtonModule, MatDialogModule, MatInputModule,
         MatTableModule, MatFormFieldModule, MatIconModule,
         MatListModule, MatPaginatorModule, MatSortModule,
         MatCheckboxModule, MatRadioModule, MatSelectModule,
         MatDatepickerModule, MatNativeDateModule, MatCardModule,
         MatGridListModule, MatTooltipModule, MatSliderModule,
         MatAutocompleteModule, MatSlideToggleModule,
         MatTabsModule } from '@angular/material';


@NgModule({
    declarations: [
        PytTextInputComponent,
        PytChoiceInputComponent,
        PytComboInputComponent,
        PytDateInputComponent,
        PytDateTimeInputComponent,
        PytNumberInputComponent,
        PytPasswordInputComponent,
        PytTextareaInputComponent,
        PytTimeInputComponent,
        PytEmailInputComponent,
        PytLabelComponent,
        PytCheckboxInputComponent,
        PytSliderToggleInputComponent,
        PytSliderInputComponent
    ],
    entryComponents: [
    ],
    providers: [
    ],
    imports: [
        CommonModule,
        MatButtonModule,
        MatInputModule,
        MatDialogModule,
        MatFormFieldModule,
        MatIconModule,
        MatListModule,
        MatPaginatorModule,
        MatSortModule,
        MatSliderModule,
        MatSlideToggleModule,
        MatCheckboxModule,
        MatRadioModule,
        MatSelectModule,
        MatDatepickerModule,
        MatNativeDateModule,
        MatTableModule,
        MatCardModule,
        MatGridListModule,
        MatTooltipModule,
        MatAutocompleteModule,
        MatTabsModule,
        FormsModule,
        ReactiveFormsModule,
        NgxMaterialTimepickerModule.forRoot(),
    ],
    exports: [
        PytTextInputComponent,
        PytChoiceInputComponent,
        PytComboInputComponent,
        PytDateInputComponent,
        PytDateTimeInputComponent,
        PytEmailInputComponent,
        PytNumberInputComponent,
        PytPasswordInputComponent,
        PytTextareaInputComponent,
        PytTimeInputComponent,
        PytLabelComponent,
        PytCheckboxInputComponent,
        PytSliderToggleInputComponent,
        PytSliderInputComponent,
    ]
})
export class GenCrudModule
{
    static forChild(): ModuleWithProviders
    {
        return { ngModule: GenCrudModule };
    }
}
