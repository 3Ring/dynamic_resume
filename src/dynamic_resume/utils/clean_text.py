import typing as t
from pydantic import BaseModel
from dynamic_resume.utils.escape_string import escape_string

T = t.TypeVar("T")

def clean_resume_for_tex(obj: T) -> T:
    if isinstance(obj, str):
        return escape_string(obj, for_tex=True)
    elif isinstance(obj, list):
        return [clean_resume_for_tex(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: clean_resume_for_tex(value) for key, value in obj.items()}
    elif isinstance(obj, BaseModel):
        cleaned_data = {
            key: clean_resume_for_tex(value) for key, value in obj.model_dump().items()
        }
        return obj.__class__(**cleaned_data)
    else:
        return obj
    
