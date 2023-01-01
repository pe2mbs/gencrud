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
import { Component, Input, forwardRef, ViewChild, ElementRef,
		 OnInit, OnChanges, AfterViewInit } from '@angular/core';
import { NG_VALUE_ACCESSOR, FormGroupDirective } from '@angular/forms';
import { trigger, state, style,
	     transition, animate } from '@angular/animations';
import { PytBaseComponent } from './base.input.component';
import { NgxMonacoEditorConfig } from "ngx-monaco-editor";
import { NgxEditorModel } from 'ngx-monaco-editor';


export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef( () => PytMonacoEditorComponent ),
    multi: true
};


export function OnLoadMonaco(): void
{
    // here monaco object will be available as window.monaco use this function to extend monaco editor functionalities.
    console.log( "OnLoadMonaco", (window as any).monaco );
    return;
}


export const monacoConfig: NgxMonacoEditorConfig = {
    baseUrl: 'assets',  // configure base path for monaco editor default: './assets'
    defaultOptions:     // pass default options to be used
    {
        scrollBeyondLastLine: false,
        automaticLayout: false
    },
    onMonacoLoad: OnLoadMonaco
};

@Component( {
    // tslint:disable-next-line:component-selector
    selector: 'pyt-monaco-editor-box',
    template: `<div #editor class="monaco-code-editor">
    <label class="label-style">
    <span>{{ placeholder }}</span>
    </label>
    <ngx-monaco-editor (onInit)="onEditorInit($event)"
                       [options]="monacoOptions"
                       [(ngModel)]="code" class="ngx-monaco-editor">
    </ngx-monaco-editor>
    </div>`,
	styles: [ `:host
    {
        height: calc( 100% - 40px );
    }

    .monaco-code-editor
    {
		width: 100%;
		min-height: 200px;
		height: calc( 100% - 20px );
		padding-bottom: 35px;
		box-sizing: content-box;
	}

	.ngx-monaco-editor
	{
		height: calc( 100% - 16px );
		border: 1px solid rgba(0, 0, 0, 0.10) !important;
	}

	.label-style
	{
		font-size: inherit;
		font-weight: 400;
		line-height: 1.125;
		font-family: Roboto, monospace;
		font-size: 14px;
		color: rgba(0, 0, 0, 0.54);`
	],
    providers: [ CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR ],
    animations: [ trigger(
    'visibilityChanged', [
        state( 'true',  style( { 'height': '*', 'padding-top': '4px' } ) ),
        state( 'false', style( { height: '0px', 'padding-top': '0px' } ) ),
        transition( '*=>*', animate( '200ms' ) )
    ] )
    ]
} )
export class PytMonacoEditorComponent extends PytBaseComponent implements OnChanges, OnInit, AfterViewInit
{
    @Input() height: string = 'auto';
    @Input() language: string = "plaintext";
    @Input() minimap: boolean = true;
    public monacoOptions = monacoConfig.defaultOptions;
    public code: string = "";
    private _editorInstance: monaco.editor.IStandaloneCodeEditor;
    @ViewChild( "editor", { static: true } ) editorContent: ElementRef;

    constructor( formGroupDir: FormGroupDirective )
    {
        super( formGroupDir );
        return;
    }

    public ngOnInit()
    {
        super.ngOnInit();
        this.code = this.control.value;
        this.monacoOptions.language = this.language;
        this.control.registerOnChange( () => {
            this.code = this.control.value;
        } );
        return;
    }

    public onEditorInit( $event ): void
    {
        this._editorInstance = $event;
        this._editorInstance.updateOptions( { readOnly: this.readonly,
                                              minimap: { enabled: this.minimap }
        } );
        const model = this._editorInstance.getModel(); // we'll create a model for you if the editor created from string value.
        monaco.editor.setModelLanguage( model, this.language );
        this._editorInstance.onDidChangeModelContent( () => {
            this.control.patchValue( this._editorInstance.getValue() );
            this.control.markAsPending();
            this.control.updateValueAndValidity();
        } );
		setInterval( () => {
			this._editorInstance.layout();
		}, 500 );
        return;
    }
}
