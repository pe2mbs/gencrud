# -*- coding: utf-8 -*-
"""Main webapp application package."""
#
# Main webapp application package
# Copyright (C) 2018-2020 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License GPL-2.0-only
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

from flask import Flask as BaseFlask
from webapp2.extensions.config import Config


class Flask( BaseFlask ):
    def __init__( self, import_name, static_url_path=None, static_folder='static', static_host=None,
                        host_matching=False, subdomain_matching=False, template_folder='templates',
                        instance_path=None, instance_relative_config=False, root_path=None ):
        BaseFlask.__init__( self, import_name, static_url_path, static_folder, static_host, host_matching, subdomain_matching,
                                  template_folder, instance_path, instance_relative_config, root_path )
        self.__sendEmail = None
        return

    """Extended version of `Flask` that implements custom config class
    """
    def make_config( self, instance_relative = False ):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path

        return Config( root_path, self.default_config )

    def sendMail( self, record ):
        if callable( self.__sendEmail ):
            self.__sendEmail( record )

        return

    @property
    def sendMailFunction( self ):
        return self.__sendEmail

    @sendMailFunction.setter
    def sendMailFunction( self, value ):
        self.__sendEmail = value
        return

