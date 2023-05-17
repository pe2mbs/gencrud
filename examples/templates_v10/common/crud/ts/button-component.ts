/**
 * Class of Components that can be inserted into ng-templates
 */
export interface ButtonComponent {
    //attributes: any;
    cssClass: string;
    onClick: () => void;
}