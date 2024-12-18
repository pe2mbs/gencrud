import typing as t
import logging
from gencrud.constants import *


logger = logging.getLogger( 'gengrud.generate.angular' )


class ServicesList(list):
    def __init__(self):
        self.__mapper = {}
        super(ServicesList, self).__init__()
        return

    def append(self, new_item):
        if new_item.mapperName in self.__mapper:
            logger.error("NOT ADDED SERVICE {}".format(new_item))
            return

        logger.info("Adding service: {}".format(new_item))
        idx = len(self)
        list.append(self, new_item)
        self.__mapper[new_item.mapperName] = idx
        return

    def unique(self, *args, exclude = None ):
        if exclude is None:
            exclude = []

        logger.debug("ServicesList.unique: {}".format(args))
        intermediate = {}
        for service in list(self):
            if service.parent is None or service.parent.uiObject not in exclude:
                key = ''.join([v for k, v in service.dictionary.items() if k in args])
                logger.debug("ServicesList.service: {} => {} | {}".format(service, args, key))
                if key == '':
                    continue

                intermediate[key] = service

        logger.debug("ServicesList.unique => {}".format(intermediate.values()))
        return intermediate.values()

    @property
    def externalService(self) -> str:
        FILLER = (' ' * 17) + ', '
        FILLER_LF = '\r\n{}'.format(FILLER)
        result = []
        for service in list(self.unique('class', 'name')):
            result.append('public {name}Service: {cls}'.format(name=service.name, cls=service.cls))

        return (FILLER if len(result) > 0 else '') + (FILLER_LF.join(result))


def buildServiceLists( columns: list, service_list: t.Optional[ServicesList] = None, full_service_list: t.Optional[ ServicesList ] = None ):
    if not isinstance( service_list, ServicesList ):
        service_list = ServicesList()

    if not isinstance( full_service_list, ServicesList ):
        full_service_list = ServicesList()

    for field in columns:
        if field.ui is not None and field.hasService():
            field.ui.service.fieldLabel = field.label
            if field.ui.isUiType(C_CHOICE, C_CHOICE_AUTO, C_CHOICE_BASE, C_COMBOBOX, C_COMBO, C_CHECKBOX):
                service_list.append( field.ui.service )

            full_service_list.append( field.ui.service )

        # required ad-on for the support of siblings, i.e., multiple usage of the same database field
        for sibling in field.siblings:
            if sibling.ui is not None and sibling.hasService():
                sibling.ui.service.fieldLabel = sibling.label
                if sibling.ui.isUiType(C_CHOICE, C_CHOICE_AUTO, C_CHOICE_BASE, C_COMBOBOX, C_COMBO, C_CHECKBOX):
                    service_list.append( sibling.ui.service )

                full_service_list.append( sibling.ui.service )

    return service_list, full_service_list