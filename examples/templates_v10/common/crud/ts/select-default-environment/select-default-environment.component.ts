import { AfterViewInit, ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { GcSelectList } from 'src/app/common/crud/model';
import { GcSubscribers } from '../subscribers';
import { DefaultEnvironmentService } from './default-environment.service';

@Component({
    selector: 'app-select-default-environment',
    templateUrl: './select-default-environment.component.html',
    styleUrls: ['./select-default-environment.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class SelectDefaultEnvironmentComponent extends GcSubscribers implements OnInit
{
    public formGroup:       FormGroup;
    public readonly:        boolean = false;
    public items:           Array<GcSelectList> = new Array<GcSelectList>();

    constructor( private defEnvironment: DefaultEnvironmentService ) 
    { 
        super();
        this.formGroup = new FormGroup( {
            environment: new FormControl( null, [ Validators.pattern(/^[1-9]*$/) ] )
        } );
        defEnvironment.subject.subscribe( data => { 
            this.formGroup.get( 'environment' ).setValue( data.SE_ID );          
        } );
        return;
    }

    ngOnInit() 
    {
        // console.log( 'ngOnInit', this.items );
        this.registerSubscription(this.defEnvironment.getSelectList("SE_ID", "SE_NAME").subscribe( data => {
            this.items = data;
            console.log( "SelectDefaultEnvironmentComponent.ngOnInit", this.defEnvironment.systemEnvironmentId, this.items );
            this.formGroup.get( 'environment' ).patchValue( this.defEnvironment.systemEnvironmentId, { emitEvent: true } );
        } ));
        return;
    }

    public onChange( $event )
    {
        console.log( 'SelectDefaultEnvironmentComponent - onChange', $event );
        this.defEnvironment.setSystemEnvironment( $event.value );
        return;
    }

    public onSaveClick()
    {
        return;
    }
}
