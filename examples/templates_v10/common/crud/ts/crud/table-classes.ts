/** Class for an ensamble of super classes for the mixin table classes */

import { GcSubscribers } from "../subscribers";

export class RowHighlighting<T> extends GcSubscribers {
    public records: T[] = [];
    public highlightedRow: T;
    public idField: string;

    constructor(id: string) {
        super();
        this.idField = id;
    }

    public addRowToCompare( row: T, onPairSelected?: () => void ): void
    {
        if ( this.records.length == 0 ) {
            // simply add record to the list
            this.records.push(row);
            this.highlightedRow = row;
        } else if ( this.records.length == 1 ) {
            // check if the current row equals the new row
            if ( this.records[0][this.idField] != row[this.idField] ) {
                // add new item and start compare
                this.records.push(row);
                if ( onPairSelected ) {
                    onPairSelected();
                }
            }
            // remove the current item
            this.highlightedRow = null;
            this.records = [];
        }
        return;
    }

}