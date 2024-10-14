import re
from gencrud.config.column import TemplateColumn
from gencrud.config.ui import TemplateUi
from gencrud.config.object import TemplateObject
from gencrud.configuraton import TemplateConfiguration


def normalize_variable( data: str ) -> str:
    data = re.sub('[^0-9a-zA-Z]+', '_', data.upper())
    data = re.sub('__', '_', data).strip()
    data = re.sub('^_', '', data)
    return data


def generatePythonConstants( config: TemplateConfiguration, obj: TemplateObject ):
    # Generate the constants.py file for the module
    constantLines = []
    for column in obj.table.columns:
        column: TemplateColumn
        if isinstance( column.ui, TemplateUi ) and column.ui.hasResolveList():
            # C_T_ACTION_INSERT                                             = 1
            constantMapping = []
            for key, value in column.ui.resolveListPy.items():
                if isinstance(value, (bool, int)):
                    value = str(value)

                if isinstance(value, str):
                    constant = normalize_variable( value )

                else:
                    constant = '<unknown>'

                constantLines.append( f"C_{column.name}_{constant} = {key}")
                constantMapping.append( f"C_{column.name}_{constant}: '{value}'")

            # C_T_ACTION_MAPPING = {C_T_ACTION_INSERT: 'Insert',
            #                       C_T_ACTION_UPDATE: 'Update',
            #                       C_T_ACTION_DELETE: 'Delete'}
            tmp = ', '.join( constantMapping )
            # Add an empty line
            constantLines.append('')
            constantLines.append(f'C_{column.name}_MAPPING = {{ {tmp} }}')

    return constantLines
