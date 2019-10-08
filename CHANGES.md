0.7.9               08-01-2019      Marc Bertens-Nguyen
    - Added getSelectionList() to crud service class. Added imports for all services used in a component 
      to the dialog, component and html. Fixed issue in filter, now only the string fields are included. 
      In view.py.templ now the primary key is removed on insert in to the data table. Updated the menuItem 
      structure with icon and route from the template.
    - Merge branch 'master' of https://git.pe2mbs.nl/angular/pytemplate.
    
0.8.0               08-01-2019      Marc Bertens-Nguyen
    - Adding unique-key option to column and table.
    
0.8.10              09-01-2019      Marc Bertens-Nguyen
    - Move the Foreign key functions from table.component into the datasource. Move the build filter from datasource.ts.templ into the TemplateTable object Minor fixes to the dialog.ts and crud-dataservice.ts scripts.
    
0.9.0               09-01-2019      Marc Bertens-Nguyen
    - Adding relationship option to table column.
    
0.9.2               13-01-2019      Marc Bertens-Nguyen
    - Change service patch id to build number
    - Implement base error message for input fields with mat-error. pyt-checkbox-input-box accepts now color, 
      labelPosition and indeterminate attributes. pyt-slider-input-box accepts now color, thumbLabel, vertical, 
      disabled, invert, step, tickInterval, min and max attributes. pyt-slidertoggle-input-box  accepts now color 
      and labelPosition (note labelPosition not yet supported by mat-slide-toggle) pyt-textbox-input-box now 
      has mat-error and mat-hint implemented.
    - Adding options to Input components, extending the ui class with extra properies.
    - Remove on insert the local update of the record list in the frontend.
    - Fix field conversion, lookup SQL type and convert.
    - Move source files into sub-packages to cleanup the source tree.
    - Move main.py from inline code to actual file in common-py.
    - Add comments for OBSOLETE properties. removing some text file.
    - Adding listview propery in the template at the column level, making 'index' and 'css.width' obsolete.
    - Fix typo in slider.component fix setup on copying template and common files into the package by using 
      wildcards.

1.0.148             29-01-2019      Marc Bertens-Nguyen
    - Adding action buttons
    - Version bump to 1.0

1.0.149             24-06-2019      Marc Bertens-Nguyen
    - Fixes for common.py with converstion function and added options default and autoupdate in template.
    - Update master with branch actions.
    - fix the missing common-py folder in the installation.
    - Correct string to PySelectList.
    - Fix typo in crud-dataservice.ts
 
1.0.(150-155)       19-09-2019      Marc Bertens-Nguyen
    - Fixes to improve the usability.
    - Make sure that the new/edit/delete dialog files or new/edit screens are not generated in case of not needed.
    
1.0.(155-174)       23-09-20019     Marc Bertens-Nguyen
    - minor fixes to improve general workings.
    
1.1.175     28-09-20019     Marc Bertens-Nguyen
    - Adding 'viewSort' to the 'table' with properties 'field' and 'order'. For the fields that are present
      in the list view the sorting cen be set, otherwise the database primary index is used.
    - Adding 'viewSize' to the 'table', this can now be set to an integer 5, 10, 25 or 100.
      dynamic viewSize is on the TODO list.
    - adding OBSOLETE warning for properties 'index' and 'css.width'
    - Replace print statements for logging to have muliple loglevels WARNING, ERROR, INFO and DEBUG
      putting in the command options '-v' results in INFO level, 'vv' results in DEBUG level.
    - Added the field identifier to the python model.
    - Adding option to select lowercase datebase identifiers.  
    - Version bump to 1.1  
    
1.2.186     08-10-2019      Marc Bertens-Nguyen
    - Adding mixin for model and is implemented in model.py
    - Adding mixin for schema, but needs implemented in schema.py       
    - Adding mixin for view, but needs implemented in view.py
    - Version bump to 1.2