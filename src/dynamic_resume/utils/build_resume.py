from dynamic_resume.models.resume import Resume
from dynamic_resume.models.experience import Experience


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
    data["professional_experience"] = professional_experience
    return Resume(**data)
