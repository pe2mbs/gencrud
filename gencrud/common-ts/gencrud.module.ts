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
import { NgModule, ModuleWithProviders } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PytTextInputComponent } from './input-component/textbox.component';
import { PytChoiceInputComponent } from './input-component/choice.component';
import { PytComboInputComponent } from './input-component/combobox.component';
import { PytDateInputComponent } from './input-component/date.component';
import { PytDatePickerInputComponent } from './input-component/date.picker.component';
import { PytDateTimeInputComponent } from './input-component/datetime.component';
import { PytDateTimePickerInputComponent } from './input-component/datetime.picker.component';
import { PytNumberInputComponent } from './input-component/number.component';
import { PytPasswordInputComponent } from './input-component/password.component';
import { PytEmailInputComponent } from './input-component/email.component';
import { PytTextareaInputComponent } from './input-component/textarea.component';
import { PytTimeInputComponent } from './input-component/time.component';
import { PytTimePickerInputComponent } from './input-component/time.picker.component';
import { PytLabelComponent } from './input-component/label.component';
import { PytCheckboxInputComponent } from './input-component/checkbox.component';
import { PytSliderToggleInputComponent } from './input-component/slidertoggle.component';
import { PytSliderInputComponent } from './input-component/slider.component';
import { CustomMaterialModule } from '../material.module';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

@NgModule({
    declarations: [
        PytTextInputComponent,
        PytChoiceInputComponent,
        PytComboInputComponent,
        PytDateInputComponent,
        PytDatePickerInputComponent,
        PytDateTimeInputComponent,
        PytDateTimePickerInputComponent,
        PytNumberInputComponent,
        PytPasswordInputComponent,
        PytTextareaInputComponent,
        PytTimeInputComponent,
        PytTimePickerInputComponent,
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
        CustomMaterialModule,
        FormsModule,
        ReactiveFormsModule
    ],
    exports: [
        PytTextInputComponent,
        PytChoiceInputComponent,
        PytComboInputComponent,
        PytDateInputComponent,
        PytDatePickerInputComponent,
        PytDateTimeInputComponent,
        PytDateTimePickerInputComponent,
        PytEmailInputComponent,
        PytNumberInputComponent,
        PytPasswordInputComponent,
        PytTextareaInputComponent,
        PytTimeInputComponent,
        PytTimePickerInputComponent,
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
