import { Component, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment.prod';

@Component({
  	// tslint:disable-next-line:component-selector
  	selector: 'gc-footer',
  	template: `<footer>{{footerText}}</footer>`,
  	styles: ['footer { padding: 10px; background-color: lightgray; text-align: center; maxHeight: 40px;}']
})
export class GcFooterComponent
{
	footerText: string = 'Webapp2 Python-flask angular core, \u00A9 Copyright 2017-2020 All rights reserved by Marc Bertens-Nguyen';

	constructor() 
	{ 
		if ( environment.footerText !== undefined && environment.footerText != null )
		{
			this.footerText = environment.footerText; 
		}
		return;
	}
}
