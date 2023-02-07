import os

import pytest
from grai_actions.config import AccessModes, Config, DefaultValues, config


def test_config_set_to_test_mode():
    assert config.grai_access_mode == AccessModes.TEST_MODE.value


@pytest.fixture
def test_key():
    test_key = "grai_namespace"
    original_value = os.environ.pop(test_key, None)
    yield test_key

    if original_value is not None:
        os.environ[test_key] = original_value


def test_empty_values_are_treated_as_missing(test_key):
    os.environ[test_key] = ""
    current_config = config.dict()
    current_config.pop(test_key)
    test = Config(**current_config)
    assert getattr(test, test_key) == getattr(DefaultValues, test_key)


# def test_config_access_mode_case_sensitivity():
#     config.grai_access_mode = "TeSt_mOde"
