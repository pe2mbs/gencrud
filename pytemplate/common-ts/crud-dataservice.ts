import { BehaviorSubject} from 'rxjs';
import { HttpClient, HttpErrorResponse} from '@angular/common/http';

export class CrudDataService<T> 
{
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

    public lockRecord( record: T ): void 
    {
        this.httpClient.post<T>( this._uri + '/lock', record ).subscribe(result => {
            console.log ( result );
        },
        (error: HttpErrorResponse) => {
            console.log (error.name + ' ' + error.message);
        });
        return;
    }

    public unlockRecord( record: T ): void 
    {
        this.httpClient.post<T>( this._uri + '/unlock', record ).subscribe(result => {
            console.log ( result );
        },
        (error: HttpErrorResponse) => {
            console.log (error.name + ' ' + error.message);
        });
        return;
    }

    public addRecord( record: T ): void 
    {
        console.log( 'addRecord', record );
        this.dialogData = record;
        this.httpClient.post<T>( this._uri + '/new', record ).subscribe(result => {
            console.log ( result );
            this.getAll();
        },
        (error: HttpErrorResponse) => {
            console.log (error.name + ' ' + error.message);
        });
        return;
    }

    public getRecord( record: T ): void 
    {
        console.log( 'addRecord', record );
        this.dialogData = record;
        this.httpClient.get<T>( this._uri + '/get', record ).subscribe(result => {
            console.log ( result );
        },
        (error: HttpErrorResponse) => {
            console.log (error.name + ' ' + error.message);
        });
        return;
    }

    public updateRecord( record: T ): void 
    {
        console.log( 'updateRecord', record );
        this.dialogData = record;
        this.httpClient.post<T>( this._uri + '/update', record ).subscribe(result => {
            console.log ( result );
        },
        (error: HttpErrorResponse) => {
            console.log (error.name + ' ' + error.message);
        });
        return;
    }

    public deleteRecord( record: string ): void 
    {
        console.log( 'deleteRecord', record );
        this.httpClient.delete<T>( this._uri + '/' + record ).subscribe( result => {
            console.log ( result );
        },
        (error: HttpErrorResponse) => {
            console.log ( error.name + ' ' + error.message );
        });
        return;
    }
}
