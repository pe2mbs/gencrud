from gencrud.configuraton import TemplateConfiguration
import os
from pytest import fixture
import pytest


@fixture
def normal_template_config() -> TemplateConfiguration:
    filename = os.path.join(os.getcwd(), 'tests', 'input', 'te_format.yaml')
    return TemplateConfiguration(filename)


@fixture
def invalid_template_config() -> TemplateConfiguration:
    filename = os.path.join(os.getcwd(), 'tests', 'input', 'invalid_te_format.yaml')
    with pytest.raises(SystemExit):
        return TemplateConfiguration(filename)


def test_normal_schema(normal_template_config: TemplateConfiguration):
    assert True


def test_invalid_schema(invalid_template_config: TemplateConfiguration):
    assert True
