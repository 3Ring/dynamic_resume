import typing as t
from os import PathLike
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from dynamic_resume.utils.escape_string import escape_string
from dynamic_resume.models.resume import Resume


def render_to_tex(
    resume: Resume,
    output_file_name: t.Optional[str] = None,
    output_dir: t.Optional[str | PathLike] = None,
    template_path: t.Optional[str | PathLike] = None,
) -> Path:
    if output_file_name is None:
        output_file_name = "resume.tex"
    output_file_name = escape_string(output_file_name, for_tex=False)
    print(output_file_name)
    if not output_file_name.endswith(".tex"):
        raise ValueError("Output file name must have a .tex extension.")

    if template_path is None:
        from dynamic_resume.config import TEMPLATE_PATH

        template_path = TEMPLATE_PATH
    else:
        template_path = Path(escape_string(str(template_path), for_tex=False))

    template_path = template_path.expanduser().resolve()

    if output_dir is None:
        output_dir = Path.cwd()
    else:
        output_dir = (
            Path(escape_string(str(output_dir), for_tex=False)).expanduser().resolve()
        )

    output_path = output_dir / output_file_name

    parent_dir = template_path.parent
    env = Environment(
        loader=FileSystemLoader(str(parent_dir)),
        block_start_string="{%",
        block_end_string="%}",
        variable_start_string="/{{",
        variable_end_string="}}/",
        comment_start_string="{##",
        comment_end_string="##}",
    )
    template = env.get_template(template_path.name)
    tex_content = template.render(resume=resume)
    with open(output_path, "w", encoding="utf-8") as f:
        print(f"Writing TeX output to {output_path}")
        f.write(tex_content)
    return output_path
