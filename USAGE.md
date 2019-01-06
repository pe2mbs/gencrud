# 1. Templating engine for Python and Angular CRUD interfaces.
This tool generates the Python backend and Angular frontend code for 
CRUD interfaces.

## 1.1 Licencing
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

# 2. Installation
Download the zip file from the version control or use git to obtain the
 repository.

## 2.1 Install via .zip
```bash
    pip3 install pytemplate-master.zip
```

```bash
    git clone https://gitlab.pe2mbs.nl/angular/pytemplate.git
    cd pytemplate
    pip3 install . 
```     

**Note: if you're using Python 2.7.x use pip2** 

# 3. Usage
Standard usage:
```bash
    gencrud [ options ] <configuration-files> 
```

## 3.1. Actual usage
```bash
    gencrud examples\role-table.yaml 
```
This generates for the role table the frontend and backend code. 
 
```bash
    gencrud examples\role-table.yaml examples\user-table.yaml 
```
This generates for the role and user tables the frontend and backend code. 
 
 
## 3.2. Options
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

# 4. Example files
The folowing example files use the templates that where installed with the
 package.
- examples\role-table.yaml
- examples\user-table.yaml
- examples\screens-base.yaml

The folowing example file use private templates that where created by you.
examples\screens.yaml
 
# 5. YAML Template
YAML (YAML Ain't Markup Language) is a human-readable data serialization 
language. It is commonly used for configuration files. See for more information 
https://yaml.org/spec/1.2/spec.html. 

Below an example of a simple template for demonstration purposes.
 
```yaml 
templates:
  python:                   ./templates/python
  angular:                  ./templates/angular
source:
  python:                   ./output/backend
  angular:                  ./output/src/app
objects:
- name:                     role
  class:                    Role
  application:              testrun
  uri:                      /api/role
  menu:
    displayName:            Database
    iconName:               database
    index:                  0
  itemItem:
    displayName:            Roles
    iconName:               roles
    index:                  0
    route:                  /roles
  table:
    name:                   WA_ROLES
    columns:
    - field:                D_ROLE_ID       INT         AUTO NUMBER  PRIMARY KEY
      label:                Identification
      index:                0
      ui:                 
        type:               label
    - field:                D_ROLE          CHAR(20)    NOT NULL
      label:                Role
      index:                1
      ui:                 
        type:               textbox
```

## 5.1. templates section 
```yaml
templates:
  python:   ./templates/python
  angular:  ./templates/angular
``` 

This is an optional section, as the default templates are located with the 
module itself. But you can set a different set of templates when you need. 

### 5.1.1. python variable
The 'python' value contains the template folder of the Python backend folder. 
This folder contains the Python scripts for the generated module. These scripts 
must be able to be handled by Mako templating engine. 

### 5.1.2. angular variable
The 'angular' value contains the template folder of the Angular frontend folder.
This folder contains the Angular scripts for the generated module. This folder 
contains the Angular scripts for the generated module.

## 5.2. source section
```yaml
source:
  python:   ./output/backend
  angular:  ./output/src/app
```

### 5.2.1. python variable
The 'python' value contains the root folder of the Python backend folder. 
This folder must contain the Flask main module.

### 5.2.2. angular variable
The 'angular' value contains the root folder of the Angular frontend folder. 
This folder should contain at the end '/src/app/'
  
## 5.3. objects section (list)
```yaml
objects:
- name:                   role
  class:                  Role
  application:            testrun
  uri:                  /api/role
  menu:
    displayName:            Database
    iconName:               database
    index:                  0
  itemItem:
    displayName:            Roles
    iconName:               roles
    index:                  0
    route:                  /roles
  table:
```  

### 5.3.1. name variable
This contains the name of the module 
     
### 5.3.2. class variable
This contains the name of the class used within the Python and Angular modules.
 
### 5.3.3. application variable

### 5.3.4. uri section
The section contains the backend and frontend uri used for this module.

#### 5.3.4.1. backend variable 
This contains the base uri for the backend.

#### 5.3.4.2. frontend variable
This contains the uri for the frontend.  

### 5.3.5. menu section
This section describes the menu entry in the frontend for the module. 

#### 5.3.5.1. displayName variable
This is the display name presented to the user. 

#### 5.3.5.2. iconName variable
This is to display an icon be sides the name. 

#### 5.3.5.3. index variable
This is the index within the menu.
 
### 5.3.6. menuitem section
This section describes the menu entry in the frontend for the module. 

#### 5.3.6.1. displayName variable
This is the label presented to the user. 

#### 5.3.6.2. iconName variable
This is to display an icon be sides the name. 

#### 5.3.6.3. index variable
This is the index within the menu.

#### 5.3.6.4. route variable
This is the route path in the frontend.
  
### 5.3.7. table sub section
This section describes the table itself, the columns and column attributes.   
  
## 5.4. table sub section

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

### 5.4.1. name variable
This is the name of the table in the database.

### 5.4.2. column section (list)
This section contains a list of column defintions
 
#### 5.4.2.1. field variable
This is the field defintion using SQL syntax.

#### 5.4.2.2. label variable
This is the field caption used in the frontend to present to the user. 

#### 5.4.2.3. ui section (optional)

##### 5.4.2.3.1. type variable
This is user interface type of the field, the following types are supported;
Depended of the SQL type the ``ui`` setting can be used to override the default.

Default setting:
* ``textbox``:      CHAR, TEXT, CHARVAR, INT, BIGINT 
* ``checkbox``:     BOOLEAN
* ``timebox``:      TIME
* ``datebox``:      DATE
* ``datetimebox``:  DATETIME
* ``choice``:       CHAR, TEXT, CHARVAR, INT, BIGINT
* ``combo``:        CHAR, TEXT, CHARVAR, INT, BIGINT
* ``textarea``:     CHAR, TEXT, CHARVAR
* ``slidetoggle``:  BOOLEAN
* ``listbox``:      CHAR, TEXT, CHARVAR, INT, BIGINT
* ``slider``:       INT, BIGINT

All ui types take the following extra paramaters; ``prefix``, ``prefix-type``, ``suffix``, ``suffix-type``    
   
For some ui components extra parameters are needed;
* ``choice`` and ``combo``
  need a service section with parameters; ``name``, ``class``, ``value``, ``label`` and optional ``path``.
* ``slider``
  need ``min``, ``max`` and optinally ``interval`` and/or ``displayWith``.        
* ``textarea``
  takes optinally ``rows`` and ``cols``
   
   
##### 5.4.2.3.3. max (optional)
This is maximal value for the slider field, when omitted the value 100 is 
used as default.
 
##### 5.4.2.3.2. min (optional)   
This is minimal value for the slider field, when omitted the value 0 is 
used as default.

##### 5.4.2.3.4. rows (optional)   
This is the the number of rows for the textarea field, when omitted the 
value 4 is used as default.

##### 5.4.2.3.5. cols (optional)
This is the the number of columns for the textarea field, when omitted 
the value 80 is used as default.

##### 5.4.2.3.6. interval (optional)
This is minimal value for the slider field, when omitted the value 1 is 
used as default.

##### 5.4.2.3.7. displayWith (optional)
This is displayWith value for the slider field, when omitted the value 
``displayWith` is used as default.

##### 5.4.2.3.9. prefix-type (optional)
This is the prefix type, it can contain only two values: 
* text
* icon 
When omitted the default value is text.

##### 5.4.2.3.8. prefix (optional)   
This can be used to prerfix a field with some text or icon.

##### 5.4.2.3.11. suffix-type (optional)   
This is the suffix type, it can contain only two values: 
* text
* icon 
When omitted the default value is text.

##### 5.4.2.3.10. suffix (optional)
This can be used to suffix a field with some text or icon.

##### 5.4.2.3.12. service section (optional)
The service section contains variable for the choice or combobox type fields, 
this service retrieves the values and labels for the choice. And for the 
combobox the values and labels must be the same.       

###### 5.4.2.3.12.1. name variable
The name of the module used to populate the list, when ever this doesn't end 
with 'Service' then 'DataService' shall be appended to name. 
 
###### 5.4.2.3.12.2.class
The name of the base class name used to populate the list

###### 5.4.2.3.12.3.path (optional)
The name of the file where the class used to populate the list is located.
whenever this is omitted the path used shall be '../<name>/service' 

###### 5.4.2.3.12.4.value
The name of the field from the table used to populate the value of the list, 
this value must be of the same type as the type of the field in the current 
table. For the combobox this revers to the same column.
 
###### 5.4.2.3.12.5.label 
The name of the field from the table used to populate the label (presentation) 
of the list. For the combobox this revers to the same column. 

#### 5.4.2.4. index variable (optional)
When set to a numeric value the field is included into list view, the value dertemines the order where the fields shall appear.
Also when set the column is included in the search filter of the list view. 
  
#### 5.4.2.5. css section (optional)

##### 5.4.2.5.1. width variable (optional)
This variable is used for the width of the list view columns. 
The best way to define the width of the columns is using percentage, therefore the columns scale with the total view. 
The total width of the columns may not exceed 97%. 

#### 5.4.2.6. import variable (optional) 
When set to a string the first word is the class name of the table that contains the relationship, the second part is the path where the module can be found. 
