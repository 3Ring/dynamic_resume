import typing as t
from pydantic import BaseModel


class Education(BaseModel):
    title: str
    institution: str
    info: str
    date: str
    highlights: list[str]
    alternatives: t.Optional[dict[str, str]] = None # Added field for alternative details primarily for AI purposes

