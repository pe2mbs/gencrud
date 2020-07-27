from webapp2.commands.inporter.base import DbInporters
from webapp2.commands.inporter.csv import CsvDbInporter
from webapp2.commands.inporter.sql import SqlDbInporter
from webapp2.commands.inporter.yaml import YamlDbInporter
from webapp2.commands.inporter.json import JsonDbInporter


dbInporters = DbInporters( { 'csv': CsvDbInporter,
                             'sql': SqlDbInporter,
                             'yaml': YamlDbInporter,
                             'json': JsonDbInporter } )


