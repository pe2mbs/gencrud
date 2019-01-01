import { Input } from "@angular/core";
import { FormControl, FormGroupDirective } from "@angular/forms";
import { trigger, state, style, transition, animate } from '@angular/animations';

export const CUSTOM_ANIMATIONS_CONTROLE: any = [ trigger(
    'visibilityChanged', [
            state( 'true', style( { 'height':'*','padding-top':'4px' } ) ),
            state( 'false', style( { height:'0px','padding-top':'0px' } ) ),
            transition( '*=>*', animate( '200ms' ) )
        ]
    )
]

export class PytBaseComponent
{
    // ID attribute for the field and for attribute for the label
    @Input()    id:             string; 
    // placeholder input
    @Input()    placeholder:    string; 
    // formControlName fieldname
    @Input()    formControlName:string; 
    // is the control readonly 
    @Input()    readonly:       string;
    // Field prefix
    @Input()    prefix:         string;
    public      prefixType:     string;
    // Field suffix
    @Input()    suffix:         string;
    public      suffixType:     string;

    public      control:        FormControl;
    public      formGroupDir:   FormGroupDirective;        

    constructor( fgd: FormGroupDirective )
    {
        this.formGroupDir = fgd;
        return;
    }

    ngOnInit() 
    {
        console.log( 'base-ngOnInit', this.formControlName );
        this.control = this.formGroupDir.control.get( this.formControlName ) as FormControl;
        console.log( 'base-control', this.control );
        if ( this.placeholder === undefined )
        {
            this.placeholder = "Enter text"; 
        }
        if ( this.readonly !== undefined )
        {
            this.control.disable();
        }
        console.log( 'base-ngOnInit - this.readonly', this.readonly );
        if ( this.prefix !== undefined )
        {
            let result = this.prefix.split( ' ' );
            if ( result.length == 1 )
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
            if ( result.length == 1 )
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
        console.log( 'base-ngOnChanges', this.control );
        return;
    }

    public get value()
    {
        return ( this.control.value );
    }
    
    public set value( v: any ) 
    {
        this.control.setValue( v );
        return;
    }

    //Lifecycle hook. angular.io for more info
    ngAfterViewInit()
    { 
        console.log( 'base-ngAfterViewInit', this.formControlName, this.control );
        // RESET the custom input form control UI when the form control is RESET
        this.control.valueChanges.subscribe( () => {
            // check condition if the form control is RESET
            if ( this.control.value == "" || 
                  this.control.value == null || 
                  this.control.value == undefined ) {
                this.value = "";      
            }
        } );
    }

    // event fired when input value is changed. later propagated up 
    // to the form control using the custom value accessor interface
    onChange( e:Event, value:any )
    {
        console.log( 'base-onChange', this.control );
        // set changed value
        this.value = value;
        // propagate value into form control using control value 
        // accessor interface
        this.propagateChange( this.value );
        return;
    }

    // propagate changes into the custom form control
    propagateChange = (_: any) => { }
    touchedChange   = (_: any) => { }

    // From ControlValueAccessor interface
    writeValue( value: any ) 
    {
        console.log( 'base-writeValue', value );
        this.value = value;
    }

    //From ControlValueAccessor interface
    registerOnChange( fn: any ) 
    {
        console.log( 'base-registerOnChange', fn );
        this.propagateChange = fn;
        return;
    }

    //From ControlValueAccessor interface
    registerOnTouched( fn: any ) 
    {
        console.log( 'base-registerOnTouched', fn );
        this.touchedChange = fn;
        return;
    }

}
