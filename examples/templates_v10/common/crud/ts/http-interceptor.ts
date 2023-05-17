import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpResponse } from '@angular/common/http';
import { HttpRequest } from '@angular/common/http';
import { HttpHandler } from '@angular/common/http';
import { HttpEvent } from '@angular/common/http';
import { tap } from 'rxjs/operators';
import { GcSpinnerService } from './spinner-service';


@Injectable()
export class GcHttpInterceptor implements HttpInterceptor
{
    private counter: number;
    constructor( private spinnerService: GcSpinnerService )
    {
        this.counter = 0;
    }

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        this.counter++;
        this.spinnerService.show();
        return next
            .handle(req)
            .pipe(
                tap((event: HttpEvent<any>) => {
                    if (event instanceof HttpResponse) {
                        this.counter--;
                        if ( this.counter === 0 )
                        {
                            this.spinnerService.hide();
                        }
                    }
                }, (error) => {
                    this.counter--;
                    if ( this.counter === 0 )
                    {
                        this.spinnerService.hide();
                    }
                })
            );
    }
}
