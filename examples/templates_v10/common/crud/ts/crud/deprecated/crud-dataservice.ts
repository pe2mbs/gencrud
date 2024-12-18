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
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { HttpClient, HttpErrorResponse, HttpParams, HttpHeaders } from '@angular/common/http';
import { tap } from 'rxjs/operators';
import { isObject } from 'util';


export interface BackEndInfo
{
    code: number;
    name: string;
    message: string;
    url: string;
    traceback: any;
    request: any;
}


export class BackendError extends Error
{
    public code: number;
    public backend: string;
    public trace: string;
    public url: string;
    public backendInfo: BackEndInfo
    constructor( message: string, backend_info: BackEndInfo )
    {
        const trueProto = new.target.prototype;
        super( message );
        Object.setPrototypeOf(this, trueProto);
        this.code = backend_info.code;
        this.backend = backend_info.message;
        this.trace = backend_info.traceback;
        this.url = backend_info.url;
        this.backendInfo = backend_info;
    }
}


export interface PytSelectList
{
    value:  any;
    label:  string;
}


export class CrudDataService<T>
{
    protected debug: boolean = false;
    protected _uri: string;
    protected _backend_filter: string = null;
    dataChange: BehaviorSubject<T[]> = new BehaviorSubject<T[]>([]);
    // Temporarily stores data from dialogs
    dialogData: T;

    constructor ( protected httpClient: HttpClient )
    {
        return;
    }

    public get uri() : string
    {
      return this._uri;
    }

    public set uri( value: string )
    {
      this._uri = value;
      return;
    }

    public get data(): T[]
    {
        return this.dataChange.value;
    }

    public getDialogData()
    {
        return this.dialogData;
    }

    /** CRUD METHODS */
    public getAll( _backend_filter: any ): void
    {
        let uri = '/list'
        if ( _backend_filter !== null )
        {
            this._backend_filter = _backend_filter;
            uri += '/' + _backend_filter.id + '/' + _backend_filter.value
        }
        this.httpClient.get<T[]>( this._uri + uri ).subscribe(
            data => {
                this.dataChange.next( data );
            },
            (error: HttpErrorResponse) => {

                throw new BackendError( error.message, error.error );
            }
        );
        return;
    }

    public list( _backend_filter: any ): Observable<T[]>
    {
        let uri = '/list'
        if ( _backend_filter !== null )
        {
            this._backend_filter = _backend_filter;
            uri += '/' + _backend_filter.id + '/' + _backend_filter.value
        }
        return this.httpClient.get<T[]>( this._uri + uri );
    }

    public getSelectListSimple( value: string, label: string, initial: any = null, final: any = null ): Observable<PytSelectList[]>
    {
        // TODO IS this depricated ?
        return this.httpClient.post<PytSelectList[]>( this._uri + '/select', { label, value } );
    }

    public getSelectList( value: string, label: string, initial: any = null, final: any = null ): Observable<PytSelectList[]>
    {
        // TODO IS this depricated ?
        const params = { label, value };
        if ( initial != null )
        {
            params['initial'] = initial;
        }
        if ( final != null )
        {
            params[ 'final' ] = final;
        }
        return ( Observable.create( observer => {
            this.httpClient.get<PytSelectList[]>( this._uri + '/select', { params: params } )
            .subscribe( ( data ) => {
                    if ( this.debug )
                    {
                        console.log( 'getSelectList() => ', data );
                    }
                    observer.next( data );
                    observer.complete();
                },
                ( error: HttpErrorResponse ) => {
                    throw new BackendError( error.message, error.error );
                }
            );
        } ) );
    }

    public getSelectionList( value: string, label: string, initial: any = null, final: any = null ): Observable<Array<string>>
    {
        // TODO IS this depricated ?
        const params = new HttpParams().set('label', label ).set('value', value );
        if ( initial != null )
        {
            params.set( 'initial', initial );
        }
        if ( final != null )
        {
            params.set( 'final', final );
        }
        return ( Observable.create( observer => {
            this.httpClient.get<PytSelectList[]>( this._uri + '/select', { params: params } )
            .subscribe( ( data ) => {
                    if ( this.debug )
                    {
                        console.log( 'getSelectList() => ', data );
                    }
                    let result = new Array<string>();
                    result.push( '-' );
                    data = data.sort( ( n1, n2 ) => {
                        if (n1.value > n2.value )
                        {
                            return 1;
                        }
                        else if (n1.value < n2.value )
                        {
                            return -1;
                        }
                        return 0;
                    });
                    for ( let entry of data )
                    {
                        result.push( entry.label );
                    }
                    observer.next( result );
                    observer.complete();
                },
                ( error: HttpErrorResponse ) => {
                    throw new BackendError( error.message, error.error );
                }
            );
        } ) );
    }

    public copyRecordSimple( record: T ): T
    {
        // This is added to keep memory allocations on the backend to a minimum.
        let tmpRecord: T = <T>{};
        for ( let key in record )
        {
            if ( !isObject( record[ key ] ) )
            {
                tmpRecord[ key ] = record[ key ];
            }
            else
            {
                tmpRecord[ key ] = null;
            }
        }
        return ( tmpRecord );
    }

    public lockRecord( record: T ): void
    {
        this.dialogData = record;
//         this.httpClient.post<T>( this._uri + '/lock', this.copyRecordSimple( record ) ).subscribe(result => {
//             if ( this.debug )
//             {
//                 console.log( result );
//             }
//         },
//         (error: HttpErrorResponse) => {
//             throw new BackendError( error.message, error.error );
//         });
        return;
    }

    public unlockRecord( record: T ): void
    {
        this.dialogData = null;
//         this.httpClient.post<T>( this._uri + '/unlock', this.copyRecordSimple( record ) ).subscribe(result => {
//             if ( this.debug )
//             {
//                 console.log( result );
//             }
//         },
//         (error: HttpErrorResponse) => {
//             throw new BackendError( error.message, error.error );
//         });
        return;
    }

    public addRecord( record: T ): void
    {
        if ( this.debug )
        {
            console.log( 'addRecord', record );
        }
        this.dialogData = record;
        this.httpClient.post<T>( this._uri + '/new', record ).subscribe(result => {
            if ( this.debug )
            {
                console.log( result );
            }
            this.getAll( this._backend_filter );
        },
        (error: HttpErrorResponse) => {
            throw new BackendError( error.message, error.error );
        });
        return;
    }

    public getRecordById( id )
    {
        if ( this.debug )
        {
            console.log( 'getRecordById', id );
        }
        return this.httpClient.get<T>( this._uri + '/get/' + id );
    }

    public getRecord( record: T ): void
    {
        if ( this.debug )
        {
            console.log( 'getRecord', record );
        }
        this.dialogData = record;
        this.httpClient.get<T>( this._uri + '/get', record ).subscribe(result => {
            if ( this.debug )
            {
                console.log( result );
            }
        },
        (error: HttpErrorResponse) => {
            throw new BackendError( error.message, error.error );
        });
        return;
    }

    public updateRecord( record: T ): void
    {
        if ( this.debug )
        {
            console.log( 'updateRecord.orignal ', this.dialogData );
            console.log( 'updateRecord.updated ', record );
        }
        for ( let key of Object.keys( record ) )
        {
            if ( this.debug )
            {
                console.log( 'update key ' + key + ' with value ', record[ key ] );
            }
            this.dialogData[ key ] = record[ key ];
        }
        this.httpClient.post<T>( this._uri + '/update', this.dialogData ).subscribe( result => {
            if ( this.debug )
            {
                console.log ( result );
            }
            this.getAll( this._backend_filter );
        },
        (error: HttpErrorResponse) => {
            throw new BackendError( error.message, error.error );
        });
        return;
    }

    public deleteRecord( record: string ): void
    {
        console.log( 'deleteRecord', record );
        this.httpClient.delete<T>( this._uri + '/' + record ).subscribe( result => {
            if ( this.debug )
            {
                console.log ( result );
            }
            this.getAll( this._backend_filter );
        },
        (error: HttpErrorResponse) => {
            throw new BackendError( error.message, error.error );
        });
        return;
    }

    public genericPut( uri: string, params: any ): void
    {
        console.log( 'genericPut', uri, params );
        this.httpClient.put( this._uri + uri, params ).subscribe( result => {
            if ( this.debug )
            {
                console.log ( result );
            }
        },
        (error: HttpErrorResponse) => {
            throw new BackendError( error.message, error.error );
        });
        return;
    }

    public genericGet( uri: string, params: any ): Observable<any>
    {
        console.log( 'genericGet', uri, params );
        return this.httpClient.get( this._uri + uri, params );
    }

    public genericPost( uri: string, body: any | null, options: any | null ): Observable<any>
    {
        console.log( 'genericPost', this._uri + uri, body, options );
        return this.httpClient.post( this._uri + uri, body );
    }

    public downloadFile( filename: string, reqParams: any ): Observable<any>
    {
        let options = new HttpHeaders( { 'Content-Type': 'application/octet-stream' } );
        return this.httpClient.get( this._uri + '/' + filename, { headers: options,
                                                                  params: reqParams,
                                                                  responseType: 'blob' } ).pipe (
            tap ( data => {
                console.log('You received data') ;
            },
            error => {
                console.log(error);
                throw new BackendError( error.message, error.error );
            } )
        );
    }
}
