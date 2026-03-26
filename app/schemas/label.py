from pydantic import BaseModel, field_validator
import re


class LabelCreate(BaseModel):
    name: str
    color: str

    @field_validator("color")
    @classmethod
    def validate_hex_color(cls, v: str) -> str:
        if not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Color must be a valid hex code like #FF5733")
        return v


class LabelUpdate(BaseModel):
    name: str | None = None
    color: str | None = None

    @field_validator("color")
    @classmethod
    def validate_hex_color(cls, v: str | None) -> str | None:
        if v and not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Color must be a valid hex code like #FF5733")
        return v


class LabelOut(BaseModel):
    id: int
    name: str
    color: str

    model_config = {"from_attributes": True}