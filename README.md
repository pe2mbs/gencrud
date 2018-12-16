# Templating engine for Python and Angular CRUD interfaces.
 
# YAML Template
Below an example of a simple template for demonstration purposes.
 
```YAML 
templates:
  python:   ./templates/python
  angular:  ./templates/angular
source:
  python:   ./output/backend
  angular:  ./output/src/app
objects:
- name:                   role
  class:                  Role
  application:            testrun
  uri:
    backend:              /api/role
    frontend:             /roles
  menu:
    caption:              Database
    index:                0
  table:
    name:                 WA_ROLES
    columns:
    - field:              D_ROLE_ID       INT         AUTO NUMBER  PRIMARY KEY
      label:              Identification
      index:              0
      ui:                 label
    - field:              D_ROLE          CHAR(20)    NOT NULL
      label:              Role
      index:              1
      ui:                 textbox
    - field:              USERS           RECORD      RELATION User
      label:              Users
      ui:                 label
      inport:             User            ../../testrun/user/model
```

## templates section 
```yaml
templates:
  python:   ./templates/python
  angular:  ./templates/angular
``` 

### python variable
The 'python' value contains the template folder of the Python backend folder.

### angular variable
The 'angular' value contains the template folder of the Angular frontend folder. 

## source section
```yaml
source:
  python:   ./output/backend
  angular:  ./output/src/app
```

### python variable
The 'python' value contains the root folder of the Python backend folder. This folder must contain the Flask main module.

### angular variable
The 'angular' value contains the root folder of the Angular frontend folder. This folder should contain at the end '/src/app/'
  
## objects section (list)
```yaml
objects:
- name:                   role
  class:                  Role
  application:            testrun
  uri:
    backend:              /api/role
    frontend:             /roles
  menu:
    caption:              Database
    index:                0
  table:
```  

### name variable
This contains the name of the module 
     
### class variable
This contains the name of the class used within the Python and Angular modules. 
### application variable

### uri section
The section contains the backend and frontend uri used for this module.

#### backend variable 
This contains the base uri for the backend.

#### frontend variable
This contains the uri for the frontend.  

### menu section
This section describes the menu entry in the frontend for the module. 

#### caption variable
This is the label presented to the user. 

#### index variable
This is the index within the sub-menu 'Tables'. 
  
### table sub section
This section describes the table itself, the columns and column attributes.   
  
## table sub section

```yaml
table:
  name:                 WA_ROLES
  columns:
  - field:              D_ROLE_ID       INT         AUTO NUMBER  PRIMARY KEY
    label:              Identification
    index:              0
    ui:                 label
  - field:              D_ROLE          CHAR(20)    NOT NULL
    label:              Role
    index:              1
    ui:                 textbox
  - field:              USERS           RECORD      RELATION User
    label:              Users
    ui:                 label
    inport:             User            ../../testrun/user/model  
```

### name variable
This is the name of the table in the database.

### column section (list)
This section contains a list of column defintions
 
#### field variable
This is the field defintion using SQL syntax.

#### label variable
This is the field caption used in the frontend to present to the user. 

#### ui variable (optional)
This is user interface type of the field, the following types are supported;
Depended of the SQL type the 'ui' setting can be used to override the default.

Default setting:
* textbox: CHAR, TEXT, CHARVAR, INT, BIGINT 
* checkbox: BOOLEAN
* timebox: TIME
* datebox: DATE
* datetimebox: DATETIME
* choice: RECORD

For standard CHAR, TEXT, CHARVAR, INT, BIGINT and BOOLEAN fields 
* textbox
* textarea
* checkbox

For relationshis RECORD fields 
* combobox
* choice
* listbox
 

#### index variable (optional)
When set to a numeric value the field is included into list view, the value dertemines the order where the fields shall appear.  

#### import variable (optional) 
When set to a string the first word is the class name of the table that contains the relationship, the second part is the path where the module can be found. 
