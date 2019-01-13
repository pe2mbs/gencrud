import { Input, OnChanges, OnInit, AfterViewInit } from '@angular/core';
import { FormControl, FormGroupDirective, ControlValueAccessor } from '@angular/forms';
import { trigger, state, style, transition, animate } from '@angular/animations';

export const CUSTOM_ANIMATIONS_CONTROLE: any = [ trigger(
    'visibilityChanged', [
            state( 'true', style( { 'height': '*', 'padding-top': '4px' } ) ),
            state( 'false', style( { height: '0px', 'padding-top': '0px' } ) ),
            transition( '*=>*', animate( '200ms' ) )
        ]
    )
];

export class PytBaseComponent implements ControlValueAccessor, OnChanges, OnInit, AfterViewInit
{
    @Input()                debug:              boolean = false;
    // ID attribute for the field and for attribute for the label
    @Input()                id:                 string;
    // placeholder input
    @Input()                placeholder:        string;
    // formControlName fieldname
    @Input()                formControlName:    string;
    // is the control readonly
    @Input()                readonly:           string;
    // Field prefix
    @Input()                prefix:             string;
    @Input( 'prefix-type' ) prefixType:         string = 'text';
    // Field suffix
    @Input()                suffix:             string;
    @Input( 'suffix-type' ) suffixType:         string = 'text';

    @Input()                color;
    @Input()                hint;
    @Input()                error:              string = 'false';

    public                  control:            FormControl;
    public                  formGroupDir:       FormGroupDirective;

    constructor( fgd: FormGroupDirective )
    {
        this.formGroupDir = fgd;
        return;
    }

    GetErrorMessage()
    {
        if ( this.control == null || this.control.valid || this.control.disabled )
        {
            return ( '' );
        }
        let result = 'Unknown error';
        if ( this.control.hasError( 'required' ) )
        {
            result = 'Required field';
        }
        else if ( this.control.hasError( 'email' ) )
        {
            result = 'Not a valid email';
        }
        else if ( this.control.hasError( 'maxlength' ) )
        {
            result = 'The data is too long, allowed (' + this.control.errors.maxlength.requiredLength + ')';
        }
        else if ( this.control.invalid )
        {
            if ( this.debug )
            {
                console.log( 'getErrorMessage( control = "', this.control, '" )' );
            }
        }
        if ( this.debug && result == 'Unknown error' )
        {
            console.log( "getErrorMessage() => " + result );
        }
        return ( result );
    }

    ngOnInit() 
    {
        if ( this.debug )
        {
            console.log( 'base-ngOnInit', this.formControlName );
        }
        this.control = this.formGroupDir.control.get( this.formControlName ) as FormControl;
        if ( this.debug )
        {
            console.log( 'base-control', this.control );
        }
        if ( this.placeholder === undefined )
        {
            this.placeholder = 'Enter text';
        }
        if ( this.color === '' || this.color === null ||
                  this.color === undefined )
        {
            this.color = 'primary';
        }
        if ( this.readonly !== undefined )
        {
            this.control.disable();
        }
        if ( this.debug )
        {
            console.log( 'base-ngOnInit - this.readonly', this.readonly );
        }
        if ( this.prefix !== undefined )
        {
            let result = this.prefix.split( ' ' );
            if ( result.length === 1 )
            {
                this.prefix = result[ 0 ];
                this.prefixType = 'text';
            }
            else if ( result.length >= 2 )
            {
                this.prefix = result[ 0 ];
                this.prefixType = result[ 1 ];
            }
        }
        if ( this.suffix !== undefined )
        {
            let result = this.prefix.split( ' ' );
            if ( result.length === 1 )
            {
                this.suffix = result[ 0 ];
                this.suffixType = 'text';
            }
            else if ( result.length >= 2 )
            {
                this.suffix = result[ 0 ];
                this.suffixType = result[ 1 ];
            }
        }
        return;
    }

    ngOnChanges()
    {
        if ( this.debug )
        {
            console.log( 'base-ngOnChanges', this.control );
        }
        return;
    }

    public get value()
    {
        return ( this.control.value );
    }
    
    public set value( v: any ) 
    {
        //this.control.setValue( v, { emitEvent: false } );
        //this.control.patchValue( v, { emitEvent: false } )
        return;
    }

    //Lifecycle hook. angular.io for more info
    ngAfterViewInit()
    {
        if ( this.debug )
        {
            console.log( 'base-ngAfterViewInit', this.formControlName, this.control );
        }
        // RESET the custom input form control UI when the form control is RESET
        this.control.valueChanges.subscribe( () => {
            // check condition if the form control is RESET
            if ( this.control.value === '' ||
                  this.control.value === null ||
                  this.control.value === undefined ) {
                this.value = '';
            }
        } );
    }

    // event fired when input value is changed. later propagated up 
    // to the form control using the custom value accessor interface
    onChange( e: Event, value: any )
    {
        if ( this.debug )
        {
            console.log( 'base-onChange', this.control );
        }
        // set changed value
        this.value = value;
        // propagate value into form control using control value 
        // accessor interface
        this.propagateChange( this.value );
        return;
    }

    // propagate changes into the custom form control
    propagateChange = (_: any) => { };
    touchedChange   = (_: any) => { };

    // From ControlValueAccessor interface
    writeValue( value: any ) 
    {
        if ( this.debug )
        {
            console.log( 'base-writeValue', value );
        }
        this.value = value;
        //this.control.patchValue( value, { emitEvent: false } )
    }

    //From ControlValueAccessor interface
    registerOnChange( fn: any ) 
    {
        if ( this.debug )
        {
            console.log( 'base-registerOnChange', fn );
        }
        this.propagateChange = fn;
        return;
    }

    //From ControlValueAccessor interface
    registerOnTouched( fn: any ) 
    {
        if ( this.debug )
        {
            console.log( 'base-registerOnTouched', fn );
        }
        this.touchedChange = fn;
        return;
    }

}
