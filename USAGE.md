# Templating engine for Python and Angular CRUD interfaces.
This tool generates the Python backend and Angular frontend code for 
CRUD interfaces.

## Licencing
Python backend and Angular frontend code generation by Template
Copyright (C) 2018 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

# Installation
Download the zip file from the version control or use git to obtain the
 repository.

## Install via .zip
```bash
    pip3 install pytemplate-master.zip
```

```bash
    git clone https://gitlab.pe2mbs.nl/angular/pytemplate.git
    cd pytemplate
    pip3 install . 
```     

**Note: if you're using Python 2.7.x use pip2** 

# Usage
Standard usage:
```bash
    gencrud [ options ] <configuration-files> 
```

## Actual usage
```bash
    gencrud examples\role-table.yaml 
```
This generates for the role table the frontend and backend code. 
 
```bash
    gencrud examples\role-table.yaml examples\user-table.yaml 
```
This generates for the role and user tables the frontend and backend code. 
 
 
## Options
The following options
> -h / --help         This help information.

> -b / --backup       Make backup of the orginal project files files.

When used every file that belongs to the orignal project will be backuped every time its altered.  

> -o / --overwrite    Force overwriting the files.

If  this option is omitted the program will exit on encountering a module name that already exists.

> -s / --sslverify    Disable the verification of ssl certificate when
>                     retrieving some external profile data.

When you are behind a proxy that uses it own certificates, you may need to enable this option ones,
  to retrieve to extra data files from the nltk package.

> -v                  Verbose option, prints what the tool is doing.

> -V / --version      Print the version of the tool.



# Example files
The folowing example files use the templates that where installed with the
 package.
examples\role-table.yaml
examples\user-table.yaml
examples\screens-base.yaml

The folowing example file use private templates that where created by you.
examples\screens.yaml


 
# YAML Template
Below an example of a simple template for demonstration purposes.
 
```yaml 
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

This is an optional section, as the default templates are located with the module itself.

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
  
#### css section (optional)

##### width variable (optional)
This variable is used for the width of the list view columns. 
The best way to define the width of the columns is using percentage, therefore the columns scale with the total view. 
The total width of the columns may not exceed 97%. 

#### import variable (optional) 
When set to a string the first word is the class name of the table that contains the relationship, the second part is the path where the module can be found. 
