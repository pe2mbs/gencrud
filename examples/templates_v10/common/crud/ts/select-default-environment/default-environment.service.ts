import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable,  } from 'rxjs';
import { GcSelectList } from 'src/app/common/crud/model';
import { SysEnvRecord } from 'src/app/testrun/te_sysenv/model';
import { isNull } from 'util';
import { BehaviorSubject } from 'rxjs';
import { GcCrudServiceBase } from '../crud/crud.service.base';


export interface SystemEnvironmentEvent
{
    SE_ID:  number;
    SE_NAME: string;
    SE_S_ID: number;
    SE_E_ID: number;
};


@Injectable({
    providedIn: 'root'
})
export class DefaultEnvironmentService extends GcCrudServiceBase<SysEnvRecord>
{
    private _systemEnvironment: number = 0;
    private _sysEnvRecord: SysEnvRecord = null;
    public subject = new BehaviorSubject( { SE_ID: 0, SE_NAME: '', SE_S_ID: 0, SE_E_ID: 0 } as SystemEnvironmentEvent );

    constructor( protected httpService: HttpClient ) 
    { 
        super(httpService, 'te_sysenv');
        const defEnv = localStorage.getItem( 'default-environment' )   
        if ( !isNull( defEnv ) )
        {
            console.log( "Loading environments", +defEnv );
            this.setSystemEnvironment( +defEnv );
        } else {
            // set initial system environment
            
        }
        return;
    }

    public get environmentId(): number
    {
        if ( !isNull( this._sysEnvRecord ) )
        {
            return ( this._sysEnvRecord.SE_E_ID );
        }
        return ( 0 );
    }

    public get systemId(): number
    {
        if ( !isNull( this._sysEnvRecord ) )
        {
            return ( this._sysEnvRecord.SE_S_ID );
        }
        return ( 0 );
    }

    public get systemEnvironmentId(): number
    {
        if ( !isNull( this._sysEnvRecord ) )
        {
            return ( this._sysEnvRecord.SE_ID );
        }
        return ( 0 );
    }

    public get sysEnvRecord(): SysEnvRecord
    {
        return ( this._sysEnvRecord );
    }

    public setSystemEnvironment( env: number )
    {
        if ( this._systemEnvironment == env && !isNull( this._sysEnvRecord ) || env == 0 )
        {
            // No need to trigger again, as the services contains the data already
            return;
        }
        this._systemEnvironment = env;
        localStorage.setItem( 'default-environment', env.toString() );
        this.httpService.get<SysEnvRecord>( `/api/te_sysenv/get/${this._systemEnvironment}` ).subscribe( data => {
            console.log( 'SysEnvRecord', data );
            this._sysEnvRecord = data;
            this.subject.next({ SE_ID: this._sysEnvRecord.SE_ID,
                                SE_NAME: this._sysEnvRecord.SE_NAME,
                                SE_S_ID: this._sysEnvRecord.SE_S_ID,
                                SE_E_ID: this._sysEnvRecord.SE_E_ID } as SystemEnvironmentEvent );
        } );
        return;
    }
}
