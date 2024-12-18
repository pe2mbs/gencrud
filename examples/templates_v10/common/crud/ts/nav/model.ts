export interface GcMenuItem
{
	caption: string;
	icon: string;
	route?: string;
	id: string;
	disabled?: boolean;
	children?: GcMenuItem[];
}
