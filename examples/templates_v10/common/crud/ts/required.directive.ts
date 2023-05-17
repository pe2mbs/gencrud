import { Directive, ElementRef } from "@angular/core";


@Directive({
    selector: '[required]'
})
export class LabelRequiredDirective 
{
    constructor( private elRef:ElementRef )
    {
        return;
    }
  
    ngAfterContentInit() 
    {
        this.elRef.nativeElement.labels.forEach( l => l.textContent += ' *' );
    }
}