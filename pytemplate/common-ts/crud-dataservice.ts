import { BehaviorSubject, Observable } from 'rxjs';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';


export interface PytSelectList
{
    value:  number;
    label:  string;
}


export class CrudDataService<T> 
{
    protected debug: boolean = false;
    protected _uri: string;
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
    public getAll(): void 
    {
        this.httpClient.get<T[]>( this._uri + '/list' ).subscribe(data => {
            this.dataChange.next( data );
        },
        (error: HttpErrorResponse) => {
            console.log (error.name + ' ' + error.message);
        });
    }

    public getSelectList( value: string, label: string ): Observable<PytSelectList[]>
    {
        const params = new HttpParams().set('label', label ).set('value', value );
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
                    console.log (error.name + ' ' + error.message);
                }
            );
        } ) );
    }

    public getSelectionList( value: string, label: string ): Observable<Array<string>>
    {
        const params = new HttpParams().set('label', label ).set('value', value );
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
                    console.log (error.name + ' ' + error.message);
                }
            );
        } ) );
    }

    public lockRecord( record: T ): void 
    {
        this.dialogData = record;
        this.httpClient.post<T>( this._uri + '/lock', record ).subscribe(result => {
            if ( this.debug )
            {
                console.log( result );
            }
        },
        (error: HttpErrorResponse) => {
            console.log( error.name + ' ' + error.message );
        });
        return;
    }

    public unlockRecord( record: T ): void 
    {
        this.dialogData = null;
        this.httpClient.post<T>( this._uri + '/unlock', record ).subscribe(result => {
            if ( this.debug )
            {
                console.log( result );
            }
        },
        (error: HttpErrorResponse) => {
            console.log( error.name + ' ' + error.message );
        });
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
            this.getAll();
        },
        (error: HttpErrorResponse) => {
            console.log( error.name + ' ' + error.message );
        });
        return;
    }

    public getRecord( record: T ): void 
    {
        if ( this.debug )
        {
            console.log( 'addRecord', record );
        }
        this.dialogData = record;
        this.httpClient.get<T>( this._uri + '/get', record ).subscribe(result => {
            if ( this.debug )
            {
                console.log( result );
            }
        },
        (error: HttpErrorResponse) => {
            console.log( error.name + ' ' + error.message );
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
        },
        (error: HttpErrorResponse) => {
            console.log( error.name + ' ' + error.message );
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
        },
        (error: HttpErrorResponse) => {
            console.log ( error.name + ' ' + error.message );
        });
        return;
    }
}
