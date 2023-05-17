import { Component, Input, Output, EventEmitter } from "@angular/core";

export interface GcContextMenuModel {
    menuText: string;
    menuEvent: string;
}

@Component({
  selector: "app-context-menu",
  templateUrl: "./context.menu.component.html",
  styleUrls: ["./context.menu.component.css"],
})
export class GcContextMenuComponent {
  @Input()
  contextMenuItems: Array<GcContextMenuModel>;

  @Output()
  onContextMenuItemClick: EventEmitter<any> = new EventEmitter<any>();

  onContextMenuClick(event, data): any {
    this.onContextMenuItemClick.emit({
      event,
      data,
    });
  }
}