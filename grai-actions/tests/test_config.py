import pytest

from grai_actions.config import AccessModes, ConcatenateableSecretStr, config


def test_config_set_to_test_mode():
    assert config.grai_access_mode == AccessModes.TEST_MODE.value


# def test_config_access_mode_case_sensitivity():
#     config.grai_access_mode = "TeSt_mOde"


def test_concatenateablesecretstr_radd():
    obj = ConcatenateableSecretStr("test")
    result = "addition " + obj
    assert result == "addition test", result
