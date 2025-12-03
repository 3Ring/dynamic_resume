import typing as t
from pydantic import BaseModel, Field, computed_field
from dynamic_resume.models.experience import Experience


class Resume(BaseModel):
    first_name: str = Field(default="")
    middle_name: str = Field(default="")
    last_name: str = Field(default="")
    summary: t.Optional[str] = None
    headline: t.Optional[str] = None
    email: t.Optional[str] = None
    phone: t.Optional[str] = None
    location: t.Optional[str] = None
    github_profile: t.Optional[str] = None
    linkedin_profile: t.Optional[str] = None
    website: t.Optional[str] = None
    education: t.Optional[list[str]] = None
    professional_experience: t.Optional[list[Experience]] = None
    skills: t.Optional[dict[str, list]] = None
    alternatives: t.Optional[dict[str, str]] = (
        None  # Added field for alternative details primarily for AI purposes
    )

    @computed_field
    @property
    def name(self) -> str:
        return " ".join(
            filter(None, [self.first_name, self.middle_name, self.last_name])
        )
