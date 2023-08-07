from typing import Optional, Any
from pydantic import BaseModel, validator
from enum import Enum


def parameters_validator(cls, parameters, values):
    constraint_type = values.get("type")
    if constraint_type == ConstraintType.BOOL:
        if parameters:  # Checking if parameters is non-empty
            raise ValueError("parameters must be empty for bool type")
        return BooleanConstraint()
    elif constraint_type == ConstraintType.PICKLIST:
        return PicklistConstraint(**parameters)
    elif constraint_type == ConstraintType.RANGE:
        return RangeConstraint(**parameters)
    elif constraint_type == ConstraintType.REGEX:
        return RegexConstraint(**parameters)
    elif constraint_type == ConstraintType.FLOAT:
        return FloatConstraint(**parameters)
    else:
        raise ValueError(f"Unsupported constraint constraint_type: {constraint_type}")


class ConstraintType(Enum):
    PICKLIST = "PICKLIST"
    FLOAT = "FLOAT"
    RANGE = "RANGE"
    REGEX = "REGEX"
    BOOL = "BOOL"


class BooleanConstraint(BaseModel):
    pass


class PicklistConstraint(BaseModel):
    options: list[str]


class RangeConstraint(BaseModel):
    min: float
    max: float


class RegexConstraint(BaseModel):
    pattern: str


class FloatConstraint(BaseModel):
    number: float


class ConstraintBase(BaseModel):
    id: Optional[int]


# Model for reading data from the Constraint table
class ConstraintRead(ConstraintBase):
    constraint_type: ConstraintType
    parameters: Optional[Any]

    class Config:
        orm_mode = True


# Model for creating a new entry in the Constraint table
class ConstraintCreate(ConstraintBase):
    constraint_type: ConstraintType
    parameters: Optional[Any]

    validator("parameters", always=True, allow_reuse=True)(parameters_validator)


# Model for updating an entry in the Constraint table
class ConstraintUpdate(BaseModel):
    constraint_type: Optional[ConstraintType]
    parameters: Optional[Any]

    validator("parameters", always=True, allow_reuse=True)(parameters_validator)
