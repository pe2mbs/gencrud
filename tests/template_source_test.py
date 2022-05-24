from pytest import fixture
from gencrud.configuraton import TemplateConfiguration
from .schema_test import normal_template_config
from gencrud.config.source import TemplateSourceAngular, TemplateSourcePython
import os


@fixture()
def template_source_python(normal_template_config: TemplateConfiguration) -> TemplateSourcePython:
    return normal_template_config.python


@fixture()
def template_source_angular(normal_template_config: TemplateConfiguration) -> TemplateSourceAngular:
    return normal_template_config.angular


def test_source_base(template_source_python: TemplateSourcePython):
    assert os.path.abspath(template_source_python.sourceBaseFolder) == os.path.join(os.getcwd(), "tests", "input", "source")


def test_template_base(template_source_python: TemplateSourcePython):
    assert os.path.abspath(template_source_python.templateBaseFolder) == os.path.join(os.getcwd(), "gencrud", "templates")


def test_common_base(template_source_python: TemplateSourcePython):
    assert os.path.abspath(template_source_python.commonBaseFolder) == os.path.join(os.getcwd(), "gencrud", "templates", "common")


def test_source_python(template_source_python: TemplateSourcePython):
    assert template_source_python.sourceFolder == os.path.join(os.getcwd(), "tests", "input", "source", "python")


def test_source_angular(template_source_angular: TemplateSourceAngular):
    assert template_source_angular.sourceFolder == os.path.join(os.getcwd(), "tests", "input", "source", "angular")


def test_common_template_python(template_source_python: TemplateSourcePython):
    assert template_source_python.commonFolder == os.path.join(os.getcwd(), "gencrud", "templates", "common", "python")
