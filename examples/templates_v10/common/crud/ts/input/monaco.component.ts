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
import { GcBaseComponent } from './base.input.component';
import { NgxMonacoEditorConfig } from "ngx-monaco-editor";
import { MatSlideToggleChange } from '@angular/material';
import { NgxEditorModel } from 'ngx-monaco-editor';
import * as YAML from 'js-yaml';
import { isNullOrUndefined } from 'util';
import Swal from 'sweetalert2';
import { Subject } from 'rxjs';
import format from 'xml-formatter';
import * as jsonFormatter from 'json-string-formatter';
import { HttpClient } from '@angular/common/http';
/*
*   This module depends on the following versions
*   "ngx-monaco-editor": "^8.1.1",
*   "monaco-editor": "^0.21.2",
*
*   And the following chnage in angular.json
*   "assets": [
*           ...
*    				{ 	"glob": "** /*",
*    					"input": "node_modules/ngx-monaco-editor/assets/monaco/",
*    					"output": "./assets/monaco/"
*    				},
*    				{ 	"glob": "** /*",
*    					"input": "node_modules/monaco-editor/min/",
*    					"output": "./assets/monaco/"
*    				}
*   ],
*/
declare const monaco: any;

export const CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR: any = {
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef( () => GcMonacoEditorComponent ),
    multi: true
};


export function OnLoadMonaco(): void
{
    // here monaco object will be available as window.monaco use this function to extend monaco editor functionalities.
    if ( this.debug )
    {
        console.log( "OnLoadMonaco", (window as any).monaco );
    }
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
    selector: 'gc-monaco-editor',
    template: `
    <div #editor class="monaco-code-editor">
        <label class="label-style">
            <span>{{ placeholder }}</span>
        </label>
        <button class="mat-raised-button"
        id="button.prettyprint"
        *ngIf="(language == 'xml' || language == 'json') && prettyPrintOption"
          class="primary"
          [disabled]="isModified"
          [(ngModel)]="prettyPrintActive"
          (click)="prettyPrintSlideToggled( $event )"
        >
        pretty-print
        </button>
        <button class="mat-raised-button"
        id="button.prettyprint"
        *ngIf="(language == 'xml' || language == 'json') && prettyPrintOption"
          class="primary"
          [disabled]="isModified"
          [(ngModel)]="prettyPrintActive"
          (click)="showOriginalMessage( $event )"
        >
        original message
        </button>
        <ngx-monaco-editor (onInit)="onEditorInit($event)"
                        [options]="monacoOptions"
                        [(ngModel)]="code" class="ngx-monaco-editor">
        </ngx-monaco-editor>
    </div>
  `,
    styles: [ `
    .monaco-code-editor
    {
    width: 100%;
    min-height: 200px;
    height: calc( 100% - 25px );
    padding-bottom: 35px;
    box-sizing: content-box;
    }

    .ngx-monaco-editor
    {
    height: calc( 100% - 25px );
    border: 1px solid rgba(0, 0, 0, 0.10) !important;
    }

    .label-style
    {
    font-size: inherit;
    font-weight: 400;
    line-height: 1.125;
    margin-right: 10px;
    font-family: Roboto, monospace;
    font-size: 14px;
    color: rgba(0, 0, 0, 0.54);`
    ],
    providers: [ CUSTOM_INPUT_CONTROL_VALUE_ACCESSOR ],
    animations: [ trigger(
    'visibilityChanged', [
    state( 'true',  style( { 'height': '*', 'padding-top': '4px' } ) ),
    state( 'false', style( { height: '0px', 'padding-top': '0px' } ) ),
    // transition( '*=>*', animate( '200ms' ) )
    ] )
    ]
} )
export class GcMonacoEditorComponent extends GcBaseComponent implements OnChanges, OnInit, AfterViewInit
{
    @Input() height: string = 'auto';
    @Input() language: string = "plaintext";
    @Input() prettyPrintOption: boolean = true;
    @Input() minimap: boolean = true;
    public monacoOptions = monacoConfig.defaultOptions;
    public prettyPrintActive: boolean = false;
    @Input() public originalCode: string;
    public code: string = "";
    private _editorInstance: any; // monaco.editor.IStandaloneCodeEditor;
    @Input() public encodeFunc: string;
    public encode: Function;
    @Input() public decodeFunc: string;
    private decode: Function;
    @Input() public onSaveClick: Subject<boolean>;
    @ViewChild( "editor", { static: true } ) editorContent: ElementRef;
    private static didInitialize = false;
    public isModified: boolean = false;

    constructor( formGroupDir: FormGroupDirective, private httpClient: HttpClient )
    {
        super( formGroupDir );
        return;
    }

    public ngOnInit()
    {
        super.ngOnInit();
        if (this.decodeFunc) {
            this.decode = eval("this." + this.decodeFunc);
            console.log("*** init decoder", this.decode)
        }
        if (this.encodeFunc) {
            this.encode = eval("this." + this.encodeFunc);
        }
        this.code = this.decode ? this.decode(this.control.value) : this.control.value;
        //this.code = this.control.value;
        if ( this.originalCode == null ) this.originalCode = this.control.value;
        this.monacoOptions.language = this.language;
        this.control.registerOnChange( () => {
            this.update();
        } );

        /*const prettyPrint = sessionStorage.getItem( "prettyPrint" );
        if ( prettyPrint != null && this.prettyPrintOption ) {
            this.prettyPrintActive = JSON.parse(prettyPrint);
            if ( this.prettyPrintActive ) this.prettyPrint( this.originalCode );
        }*/

        // user wants to save the content --> encode the code again
        if (!isNullOrUndefined(this.onSaveClick)) {
            this.registerSubscription(
                this.onSaveClick.subscribe(v => {
                    if (!isNullOrUndefined(this.encode) && !isNullOrUndefined(this.control)) {
                        const val = this._editorInstance.getValue();
                        this.control.patchValue( this.encode(val) );
                        this.control.markAsPending();
                        this.control.updateValueAndValidity();
                    }
                })
            );
        }
        return;
    }

    public update() {
        if ( this.debug ) {
            console.log("****** decoder: ", this.decode, this.decodeFunc, this.control.value);
        }
        this.code = !isNullOrUndefined(this.decode) ? this.decode(this.control.value) : this.control.value;
    }

    public prettyPrintSlideToggled( event: MatSlideToggleChange ) {
          this.prettyPrint();
        //sessionStorage.setItem( "prettyPrint", JSON.stringify( event.checked ) );
    }

    public showOriginalMessage( event: MatSlideToggleChange ) {
        if ( this.originalCode != null ) this.control.setValue(  this.originalCode );
        //sessionStorage.setItem( "prettyPrint", JSON.stringify( event.checked ) );
    }

    public prettyPrint( value: string = null )
    {
        if (this.language == 'xml')
        {
            try {
                var hvalue = format( value != null ? value : this.control.value, {
                    indentation: '    ',
                    // filter: (node) => node.type !== 'Comment',
                    collapseContent: true,
                    lineSeparator: '\n'
                });
                this.control.setValue( hvalue );
                this.isModified = false;
            } catch (error) {
                console.log("******", value, this.control.value)
                console.log(error);
            }
        } else if (this.language == 'json')
        {
            this.control.setValue(jsonFormatter.format( value != null ? value : this.control.value ));
            this.isModified = false;
        }
    }

    public onModelChange(func) {
        this._editorInstance.onDidChangeModelContent(func);
    }

    public get editorValue() {
        return this._editorInstance.getValue();
    }

    public onEditorInit( $event ): void
    {
        this._editorInstance = $event;
        this._editorInstance.updateOptions( { readOnly: this.readonly,
                                                minimap: { enabled: this.minimap }
        } );
        const model = this._editorInstance.getModel(); // we'll create a model for you if the editor created from string value.
        monaco.editor.setModelLanguage( model, this.language );

        if (!GcMonacoEditorComponent.didInitialize) {
            GcMonacoEditorComponent.didInitialize = true;
            this.setCompletionProviders(this.language);
        }

        this._editorInstance.onDidChangeModelContent( () => {
            // no update of control when the content was decoded
            // update will only happen on explicit save
            if (isNullOrUndefined(this.decode)) {
                const val = this._editorInstance.getValue();
                this.control.patchValue( val );
                this.control.markAsPending();
                this.control.updateValueAndValidity();
            }
            console.log("**** editor change", this._editorInstance.getValue())
            if ( this.prettyPrintActive ) this.isModified = true;
        } );
        setInterval( () => {
            this._editorInstance.layout();
        }, 500 );
        return;
    }

    public setCompletionProviders(language: string) {
        //if (language == "python") {
        this.httpClient.get("/api/testprocess/generatorFunctions").toPromise().then((data: any) => {
            // register auto completion for python
            monaco.languages.registerCompletionItemProvider('python', {
                provideCompletionItems:  function (model, position) {
                    // find out if we are completing a property in the 'dependencies' object.
                    var textUntilPosition = model.getValueInRange({
                        startLineNumber: 1,
                        startColumn: 1,
                        endLineNumber: position.lineNumber,
                        endColumn: position.column
                    });
                    var match = textUntilPosition.match(
                        /\s*/
                    );
                    if (!match) {
                        return { suggestions: [] };
                    }
                    var word = model.getWordUntilPosition(position);
                    var range = {
                        startLineNumber: position.lineNumber,
                        endLineNumber: position.lineNumber,
                        startColumn: word.startColumn,
                        endColumn: word.endColumn
                    };
                    return {
                        suggestions: data.methods.map(functionName => {
                            return {
                                label: functionName,
                                kind: monaco.languages.CompletionItemKind.Function,
                                documentation: 'standard generator function',
                                insertText: "${ s." + functionName + " }",
                                range: range
                            };
                        })
                    };
                }
            });
        })
        //}
    }

    public convertJSONtoYAML(jsonString: string | any) {
        try {
            let jsonObject = jsonString;
            if ( typeof jsonString === 'string' ) {
                jsonObject = JSON.parse(jsonString);
            }
            const value = YAML.dump(jsonObject);
            return value
        } catch (error) {
            console.log("*****", error)
            return jsonString;
        }
    }

    public convertYAMLtoJSON(yamlString: string) {
        try {
            const yamlObject = YAML.load(yamlString);
            const jsonString = JSON.stringify(yamlObject);
            return jsonString;
        } catch (error) {
            console.log("*****", error)
            Swal.fire({
                position: 'bottom-end',
                icon: 'error',
                title: 'Something went wrong. Please check your input for correct YAML syntax.',
                html: error.message,
                showConfirmButton: false,
                timer: 1500
            });
            return yamlString;
        }
    }
}
