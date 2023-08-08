import pytest
from schemas.column_constraint import (
    parameters_validator,
    ConstraintType,
    BooleanConstraint,
    PicklistConstraint,
    RangeConstraint,
    RegexConstraint,
    FloatConstraint,
)


def test_parameters_validator_bool_empty_params():
    result = parameters_validator(None, None, {"type": ConstraintType.BOOL})
    assert isinstance(result, BooleanConstraint)


def test_parameters_validator_bool_with_params():
    with pytest.raises(ValueError, match="parameters must be empty for bool type"):
        parameters_validator(
            None, {"some_param": "value"}, {"type": ConstraintType.BOOL}
        )


def test_parameters_validator_picklist():
    parameters = {"options": ["option1", "option2"]}
    result = parameters_validator(None, parameters, {"type": ConstraintType.PICKLIST})
    assert isinstance(result, PicklistConstraint)


def test_parameters_validator_range():
    parameters = {"min": 1, "max": 10}
    result = parameters_validator(None, parameters, {"type": ConstraintType.RANGE})
    assert isinstance(result, RangeConstraint)
    assert result.min == 1
    assert result.max == 10


def test_parameters_validator_regex():
    parameters = {"pattern": "^[a-zA-Z]+$"}
    result = parameters_validator(None, parameters, {"type": ConstraintType.REGEX})
    assert isinstance(result, RegexConstraint)


def test_parameters_validator_float():
    parameters = {"number": 3.14}
    result = parameters_validator(None, parameters, {"type": ConstraintType.FLOAT})
    assert isinstance(result, FloatConstraint)
    assert result.number == 3.14


def test_parameters_validator_unsupported_type():
    with pytest.raises(ValueError, match="Unsupported constraint constraint_type:"):
        parameters_validator(None, {"param": "value"}, {"type": "UNSUPPORTED_TYPE"})
