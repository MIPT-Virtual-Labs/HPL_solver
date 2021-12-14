from typing import List, Optional, Union

from pydantic import BaseModel, validator


class Error(BaseModel):
    error: str
    field: str


class Response(BaseModel):
    errors: Optional[List[Error]]
    description: Optional[str]
    solution: Optional[Union[dict, List[dict]]]
    figures: Optional[List[dict]]
    status: str

    @validator("status")
    def validate_status(cls, st, values):
        if st == "error":
            if "errors" not in values:
                raise ValueError("status is set to `error` but no errors provided")
        else:
            if "errors" in values and values["errors"]:
                raise ValueError(f"status is not {st} but errors were found")
        if st == "failed" and "description" not in values:
            raise ValueError("status is set to `failed` but no description provided")
        return st
