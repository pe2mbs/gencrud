export class GcFilterColumn
{
	protected _column: string;
	protected _value: string | string[];
	protected _operator: string;
	protected debug: boolean;
	
	constructor( column: string, debug = false )
	{
		this._column = column;
		this._value = null;
		this._operator = null;
		this.debug = debug;
	}

	public clear()
	{
		this._value = null;
		this._operator = null;
		return;
	}

	public apply( values: any | any[], operator: string )
	{
		if ( this.debug )
		{
			console.log( 'FilterColumn.apply', this._column, values, operator );
		}
		this._value = values;
		this._operator = operator;
		return;
	}

	public get column(): string
	{
		return ( this._column );
	}
	
	public get value(): string | string[]
	{
		return ( this._value );
	}

	public get operator(): string
	{
		return ( this._operator );
	}
}
