from enum import Enum, auto

from pydantic import BaseModel


class thing(str, Enum):
    x = "x"
    y = "y"


class Thing(BaseModel):
    item: thing

    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True  # remove trailing whitespace
        use_enum_values = True  # Populates model with the value property of enums
        validate_assignment = True  # Perform validation on assignment to attributes


x = Thing(item="x")

print(x)
