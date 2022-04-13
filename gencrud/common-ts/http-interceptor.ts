import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpResponse } from '@angular/common/http';
import { HttpRequest } from '@angular/common/http';
import { HttpHandler } from '@angular/common/http';
import { HttpEvent } from '@angular/common/http';
import { tap } from 'rxjs/operators';
import { SpinnerService } from './spinner-service';


@Injectable()
export class CustomHttpInterceptor implements HttpInterceptor
{
    constructor(private spinnerService: SpinnerService)
    {
        return;
    }

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
       this.spinnerService.show( req.url );
        return next
            .handle( req )
            .pipe(
                tap((event: HttpEvent<any>) => {
                    if (event instanceof HttpResponse)
                    {
                        this.spinnerService.hide( req.url );
                    }
                }, (error) => {
                    this.spinnerService.hide( req.url );
                })
            );
    }
}