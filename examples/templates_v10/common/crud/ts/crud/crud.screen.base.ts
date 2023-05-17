import { FormGroup, FormControl, ValidationErrors } from '@angular/forms';
import { OnInit, Input, OnDestroy, Component, Injectable, AfterViewInit, HostListener } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GcCrudServiceBase } from './crud.service.base';
import {Location} from '@angular/common'; 
import { GcSubscribers } from '../subscribers';
import { isNullOrUndefined } from 'util';
import Swal from 'sweetalert2';
import { Subject } from 'rxjs';
import { commonErrorHandler, redirectingErrorHandler } from '../error-dialog/http-error-handler';
import { AppInjector } from 'src/app/injector';

export class ActionEvent<T>
{
    public Record: T;
    public Status: boolean;
    public Data: any;

    constructor( status: boolean, record: T = null, data: any = null )
    {
        this.Status = status;
        this.Record = record;
        this.Data = data;
    }
};

// @Component( {
// 	template: ''
// } )
@Injectable()
// tslint:disable-next-line:component-class-suffix
export class GcScreenBase<T> extends GcSubscribers implements OnInit, OnDestroy, AfterViewInit
{
	@Input()	id: string;
	@Input()	value: any;
	@Input()	mode: string;	// edit, add, filter
    public      saveButtonClicked: Subject<boolean> = new Subject();
    public      exitButton: boolean = true;
    private     callBack: ( event: ActionEvent<T> ) => any;
    public      callBackData: any = null;
	public      row: T;
	public      formGroup: FormGroup;
	public      formControl: FormControl;
	public      sub: any;
	protected   fixedValues: any = null;
    protected   debug: boolean = true;
    public      fieldsToExcludeFromChangeDetection: string[] = [];
    public      tabIndex: number = 0;
    private     ignoreStoredTabIndex = false;
    public      hasFormErrors: boolean = false;
    public      invalidFields: string = "";
    public      initiallyLoaded: boolean = false;
    public      isModified: boolean = false;
    public      prevRecord: any;
    public      router: Router;
    private     location: Location

	constructor( protected name: string,
                 protected route: ActivatedRoute,
                 public dataService: GcCrudServiceBase<T>
                )
	{
		super();
        this.router = AppInjector.injector.get( Router );
        this.location = AppInjector.injector.get( Location );
        const state = this.router.getCurrentNavigation() != null && this.router.getCurrentNavigation().extras != null ? this.router.getCurrentNavigation().extras.state : null;
        if ( state != null && state.record != null ) this.prevRecord = state.record;
		return;
	}

	protected updateFormGroup( record: T ): void
	{
        if ( !this.initiallyLoaded ) {
            //this.prevRecord = record;
            this.initiallyLoaded = true;
        }
	}

	public ngOnInit(): void 
    {
        if ( this.id === undefined || this.id === null )
        {
            this.registerSubscription( this.route.queryParams.subscribe( params => {
                this.id             = params.id;    // Contains the key field, currently only the primary key is supported.
                this.value          = params.value; // Contains val value for the key field.
                this.mode           = params.mode;  // edit or new, filter only supported on the table component.
                if ( params.tabIndex != null ) {
                    this.tabIndex = params.tabIndex;
                    this.ignoreStoredTabIndex = true;
                }
                // ugly workaround: if we set prevRecord above by routing params, we can use it here
                if ( this.prevRecord != null ) this.processRecordData( this.prevRecord );
                this.updateFixedValues( params );
            } ) );
        }
        if ( ( this.value != null || this.value !== undefined ) && this.prevRecord == null )
        {
            this.loadData();
        }
        this.restoreView();
        return;
    }

    @HostListener('window:beforeunload', ['$event'])
    handleBeforeUnload($event) {
         // prompt user on reload when he/she has unsaved changes
        if (this.isModified) {
            $event.returnValue = true;
        }
    }

    @HostListener('window:unload', ['$event'])
    handleUnload($event) {
        // if user clicks on leave in the above method, this is the last code
        // portion to execute
        this.dataService.unlockRecord( this.row, true  );
    }

    public loadData( next?: () => void ) {
        this.dataService.getRecordById( this.value ).toPromise().then( record => {
            this.processRecordData( record );
            if ( next ) {
                next();
            }
        }).catch( errorResponse => {
            redirectingErrorHandler( errorResponse, "/" );
        } );
    }

    private processRecordData( record ) {
        this.row = record;
        this.prevRecord = record;
        this.updateFormGroup( this.row );
        this.updateFixedValues();
        this.dataService.lockRecord( this.row );
    }

    public ngAfterViewInit(): void {
        this.formGroup.markAllAsTouched();
        this.registerSubscription(
            this.formGroup.valueChanges.subscribe(changes => {
                if ( this.debug ) {
                    console.log("******** change", changes, this.prevRecord);
                }
                if( this.initiallyLoaded && this.prevRecord ) {
                    var flag = false;
                    for ( var key of Object.keys(changes)) {
                        if ( !this.fieldsToExcludeFromChangeDetection.includes(key) && changes[key] != this.prevRecord[key] && key in this.prevRecord && 
                            !((changes[key] == "" && this.prevRecord[key] == null) ||
                             (this.prevRecord[key] == "" && changes[key] == null)) ) {
                            if ( this.debug ) {
                                console.log("******** different", key, changes[key], this.prevRecord[key]);
                            }
                            this.isModified = true;
                            flag = true;
                            break;
                        }
                    }
                    if ( !flag ) this.isModified = false;
                }
                //if ( this.initiallyLoaded && this.prevRecord == null ) {
                //    this.prevRecord = changes;
                //}
            })
        )
    }
    
    public onTabChanged( $event ): void 
    {
        console.log( 'onTabChanged', $event );
        this.tabIndex = $event.index;
        this.storeView();
    }

	public ngOnDestroy(): void 
    {
        if ( this.isModified ) {
            Swal.fire({
                title: 'Do you want to save the changes?',
                showDenyButton: true,
                showCancelButton: false,
                confirmButtonText: 'Save',
                denyButtonText: `Don't save`,
              }).then((result) => {
                if (result.isConfirmed) {
                  this.save(false, () => {
                    this.dataService.unlockRecord( this.row );
                  });
                } else if (result.isDenied) {
                    // dont do anything
                    // Swal.fire('Changes are not saved', '', 'info')
                    this.dataService.unlockRecord( this.row );
                }
                this.storeView();
                super.ngOnDestroy();
              })
        } else {
            this.dataService.unlockRecord( this.row );
            this.storeView();
            super.ngOnDestroy();
        }
        return;
    }

    public doInitialize(id, value, callback: ( event: ActionEvent<T> ) => any, data: any): void {
        this.id = id;
        this.value = value;
        this.mode = 'edit';
        this.callBack = callback;
        this.callBackData = data;
        // after component creation, ngOnInit is called already, however, we need to ensure
        // that the hidden ngOninit is called AFTER this doInitialize. right now it does, but it
        // might be a racing condition
        //this.ngOnInit();
    }

	protected updateFixedValues( fixed_values: any = null ): void
    {
        if ( fixed_values != null )
        {
            this.fixedValues = fixed_values;
        }
        if ( this.fixedValues != null )
        {
            for ( const key in this.fixedValues )
            {
                if ( key.endsWith( '_ID' ) )
                {
                    console.log("id-key")
                    const value: number = +this.fixedValues[ key ];
                    const ctrl = this.formGroup.get( key );
                    if ( ctrl != null )
                    {
                        ctrl.setValue( value );
                        if ( !this.editMode )
                        {
                            ctrl.disable( { onlySelf: true } );
                        }
                    }
                }
            }
        }
        return;
    }

	public get editMode(): boolean
    {
        return ( this.mode === 'edit' );
	}

    public invalidFieldsListString(): string
    {
        const keys = Object.keys(this.formGroup.controls).filter(key => {
            const controlErrors: ValidationErrors = this.formGroup.get(key).errors;
            if (!isNullOrUndefined(controlErrors)) {
              return true;
            }
            return false;
          }).map(key => key.substring(key.indexOf("_") + 1, key.length - (key.endsWith("_ID") ? 3 : 0 ) ));
        return keys.join(", ")
    }

    public hasErrors() {
        return Object.values(this.formGroup.controls).some((control) => control.errors != null);
    }

	public onCancelClick(): void 
	{
        //this.dataService.unlockRecord( this.row );
        if ( isNullOrUndefined( this.callBack ) )
        {
            window.history.back();
        }
        else
        {
            this.callBack( new ActionEvent<T>( false ) );
        }
        return;		
	}

    public onSaveClick(): void
	{
        this.save();
    }

    public onSaveExitClick(): void
	{
        this.save(true);
    }

	public save(exit: boolean = false, next?: () => void ): void 
	{
        // tell child components that the save button was clicked 
        this.saveButtonClicked.next(true);
        
        this.invalidFields = this.invalidFieldsListString();
        // validate first which visible fields are invalid
        if (this.hasErrors()) {
            this.hasFormErrors = true;
            return;
        } else {
            this.hasFormErrors = false;
        }

        //if (!this.formGroup.valid) {
        //    return;
        //}

        // proceed with default saving behavior
		if ( !this.editMode )
        {
            if ( this.fixedValues != null )
            {
                for ( const key in this.fixedValues )
                {
                    if ( key.endsWith( '_ID' ) )
                    {
                        const value: number = +this.fixedValues[ key ];
                        const ctrl = this.formGroup.get( key );
                        if ( ctrl != null )
                        {
                            ctrl.enable( { onlySelf: true } );
                            ctrl.setValue( value );
                        }
                    }
                }
            }
            Swal.fire('Creating new entry')
            Swal.showLoading();
            this.registerSubscription(
                this.dataService.addRecord( this.formGroup.value ).subscribe( record => {
                    this.registerSubscription(
                        this.dataService.getPrimaryKey().subscribe(result => {
                            const id = result["primaryKey"];
                            this.id = id;
                            this.value = record[id];
                            this.mode = "edit";
                            this.isModified = false;
                            //this.prevRecord = this.row;
                            //this.ngOnInit();
                            this.processRecordData( record );
                            const url = this.router.createUrlTree([], {relativeTo: this.route, queryParams: { id: id, mode: 'edit', value: this.value }}).toString().replace("new", "edit");
                            this.location.replaceState( url )  // .replaceState("/some/newstate/");

                            Swal.fire({
                                position: 'bottom-end',
                                icon: 'success',
                                title: 'New item successfully created',
                                showConfirmButton: false,
                                timer: 1500
                            });
                            if ( next ) {
                                next();
                            }
                            this.exitScreen(exit, true);
                        })
                    )}, error => {
                        Swal.fire({
                            position: 'bottom-end',
                            icon: 'error',
                            title: 'Something went wrong. Please try again or contact the developers.',
                            html: error.message,
                            showConfirmButton: true
                        });
                        this.exitScreen(exit, false);
                    }
                )
            );
        }
        else
        {
            Swal.fire('Saving changes...')
            Swal.showLoading();
            // update current row elements based on fomrGroup contents
            this.synchronizeRowWithFormGroup();
            this.dataService.updateRecord( this.row ).toPromise().then( record => {
                this.isModified = false;
                this.prevRecord = this.row;
                Swal.fire({
                    position: 'bottom-end',
                    icon: 'success',
                    title: 'Changes successfully saved',
                    showConfirmButton: false,
                    timer: 1500
                });
                if ( next ) {
                    next();
                }
                this.exitScreen(exit, true);
            }).catch( (error) => {
                Swal.fire({
                    position: 'bottom-end',
                    icon: 'error',
                    title: 'Something went wrong. Please try again or contact the developers.',
                    html: error.message,
                    showConfirmButton: true
                });
                this.exitScreen(exit, false);
            })
		}

        // unlocking disabled because saving does not close the component
        // this.dataService.unlockRecord( this.row );
		return;
	}

    private synchronizeRowWithFormGroup() {
        for ( var key of Object.keys( this.formGroup.value ) ) {
            // console.log("**** setting key: ", key, this.formGroup.value[key])
            this.row[key] = this.formGroup.value[key];
        }
    }


    private exitScreen(exit: boolean = true, callBack: boolean = false) {
        if ( callBack && !isNullOrUndefined( this.callBack ) )
        {
            this.callBack( new ActionEvent<T>( true, this.formGroup.value, this.callBackData ) );
        }

        if (exit) {
            window.history.back();
        }
    }

    private storeView(): void
    {
        if(!isNullOrUndefined(this.id)) {
		    sessionStorage.setItem( "tab-" + this.id.toString(), JSON.stringify( this.tabIndex ) );
        }
        return;
    }

    private restoreView(): void
    {
        if(!isNullOrUndefined(this.id) && !this.ignoreStoredTabIndex) {
            const data = sessionStorage.getItem( "tab-" + this.id.toString() );
            if ( !isNullOrUndefined( data ) )
            {
                this.tabIndex = JSON.parse( data );
            }
        }
        return;
    }
}
