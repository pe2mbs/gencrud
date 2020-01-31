from flask import Flask as BaseFlask
from config import Config


class Flask( BaseFlask ):
    """Extended version of `Flask` that implements custom config class
    """
    def make_config( self, instance_relative = False ):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path

        return Config( root_path, self.default_config )
