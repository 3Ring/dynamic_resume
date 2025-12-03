import typing as t
from pydantic import BaseModel, computed_field


class Experience(BaseModel):
    company: str
    company_info: str
    dates_employed: str
    title: str
    highlights: list[str]
    alternatives: t.Optional[dict[str, str]] = None # Added field for alternative details primarily for AI purposes

    @computed_field
    @property
    def start_date(self) -> str:
        return self.dates_employed.split(",")[0].strip()

    @computed_field
    @property
    def end_date(self) -> str:
        return self.dates_employed.split(",")[1].strip()
