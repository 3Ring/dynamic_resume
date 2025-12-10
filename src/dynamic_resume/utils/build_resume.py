from dynamic_resume.models.resume import Resume
from dynamic_resume.models.experience import Experience
from dynamic_resume.models.education import Education


def build_resume_from_dict(data: dict) -> Resume:
    professional_experience = []
    for exp in data.get("professional_experience", {}):
        if not isinstance(exp, dict):
            raise ValueError(f"Invalid experience entry: {exp}")
        for k, v in exp.items():
            if not isinstance(v, dict):
                raise ValueError(f"Invalid experience details for {k}: {v}")
            professional_experience.append(
                Experience(
                    company=k,
                    company_info=v.get("company_info", ""),
                    dates_employed=v.get("dates_employed", ""),
                    title=v.get("title", ""),
                    highlights=v.get("highlights", []),
                    alternatives=v.get("alternatives", None),
                )
            )
    education = []
    for edu in data.get("education", []):
        if not isinstance(edu, dict):
            raise ValueError(f"Invalid education entry: {edu}")
        for k, v in edu.items():
            if not isinstance(v, dict):
                raise ValueError(f"Invalid education details for {k}: {v}")
            education.append(
                Education(
                    title=k,
                    institution=v.get("institution", ""),
                    info=v.get("info", ""),
                    date=v.get("date", ""),
                    highlights=v.get("highlights", []),
                    alternatives=v.get("alternatives", None),
                )
            )
    
    data["professional_experience"] = professional_experience
    data["education"] = education
    return Resume(**data)
