import typing as t
from dataclasses import dataclass, asdict
import subprocess
from jinja2 import Environment, FileSystemLoader
import yaml
from pathlib import Path


TEMPLATE_DIR = Path(__file__).parent.joinpath("templates")
RESUME1_TEMPLATE = TEMPLATE_DIR.joinpath("resume1.j2")

def escape_string(s: str, for_tex: bool = True) -> str:
    if for_tex:
        s = s.replace("\\", "\\textbackslash{}")
    return (
        s.replace("%", "\\%")
        .replace("#", "\\#")
        .replace("{", "\\{")
        .replace("}", "\\}")
        .replace("&", "\\&")
        .replace("$", "\\$")
    )


@dataclass
class EscapeClass:

    def __post_init__(self):
        for field in self.__dataclass_fields__:
            value = getattr(self, field)
            if isinstance(value, str):
                setattr(self, field, escape_string(value))
            elif isinstance(value, list):
                for i in range(len(value)):
                    if isinstance(value[i], str):
                        value[i] = escape_string(value[i])


@dataclass
class Experience(EscapeClass):
    company: str
    company_info: str
    dates_employed: str
    title: str
    highlights: list[str]

    @property
    def start_date(self) -> str:
        return self.dates_employed.split(",")[0].strip()

    @property
    def end_date(self) -> str:
        return self.dates_employed.split(",")[1].strip()


@dataclass
class Resume(EscapeClass):
    name: str = ""
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
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

    def __str__(self):
        obj = asdict(self)
        out = ["Resume:"]
        gd = lambda d: d * "  "

        def compile(value, depth=1):
            if isinstance(value, dict):
                for k, v in value.items():
                    out.append(f"{gd(depth)}{k}:")
                    compile(v, depth + 1)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        compile(item, depth + 1)
                    else:
                        out.append(f"{gd(depth)}- {item}")
            else:
                out.append(f"{gd(depth)}{value}")

        compile(obj)
        return "\n".join(out)


    @classmethod
    def build_from_yaml(cls, yaml_path: str) -> "Resume":
        with open(yaml_path, "r", encoding="utf-8") as f:
            resume_data: dict = yaml.safe_load(f)
        return cls.build(resume_data)
    
    @classmethod
    def build(cls, data: dict) -> "Resume":
        """
        Build a Resume instance from the provided data dictionary.
        """
        first_name = data.get("first_name", "")
        middle_name = data.get("middle_name", "")
        last_name = data.get("last_name", "")
        headline = data.get("headline")
        email = data.get("email")
        phone = data.get("phone")
        location = data.get("location")
        github_profile = data.get("github_profile")
        linkedin_profile = data.get("linkedin_profile")
        website = data.get("website")
        education = data.get("education")
        professional_experience = []
        for exp in data.get("professional_experience", {}):
            for k, v in exp.items():
                professional_experience.append(
                    Experience(
                        company=k,
                        company_info=v.get("company_info", ""),
                        dates_employed=v.get("dates_employed", ""),
                        title=v.get("title", ""),
                        highlights=v.get("highlights", []),
                    )
                )
        skills: t.Optional[dict[str, list]] = data.get("skills")
        return cls(
            name= f"{first_name} {middle_name} {last_name}".strip(),
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            headline=headline,
            email=email,
            phone=phone,
            location=location,
            github_profile=github_profile,
            linkedin_profile=linkedin_profile,
            website=website,
            education=education,
            professional_experience=professional_experience,
            skills=skills,
        )

    def render_to_tex(self, output_path: str, template_path: str):
        output_path = escape_string(output_path, for_tex=False)
        template_path = escape_string(template_path, for_tex=False)
        template_name = Path(template_path).name
        parent_dir = Path(template_path).parent
        env = Environment(
            loader=FileSystemLoader(str(parent_dir)),
            block_start_string="{%",
            block_end_string="%}",
            variable_start_string="/{{",
            variable_end_string="}}/",
            comment_start_string="{##",
            comment_end_string="##}",
        )
        template = env.get_template(template_name)
        tex_content = template.render(resume=self)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(tex_content)
    
    @staticmethod
    def tex_to_pdf(tex_file: str, output_dir: str):
        subprocess.run(["pdflatex", "-output-directory", escape_string(output_dir, for_tex=False), escape_string(tex_file, for_tex=False)], check=True)