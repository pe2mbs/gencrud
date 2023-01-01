import { Directive, HostListener } from "@angular/core";

@Directive({
    // tslint:disable-next-line:directive-selector
    selector: "[click-stop-propagation]"
})
// tslint:disable-next-line:directive-class-suffix
export class ClickStopPropagation
{
    @HostListener("click", ["$event"])
    public onClick(event: any): void
    {
        event.stopPropagation();
    }
}
