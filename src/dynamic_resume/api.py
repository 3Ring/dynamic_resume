import typing as t
from os import PathLike

from dynamic_resume.models.resume import Resume
from dynamic_resume.utils.get_resume_data import get_resume_data
from dynamic_resume.utils.build_resume import build_resume_from_dict
from dynamic_resume.utils.render_to_text import render_to_tex
from dynamic_resume.utils.clean_text import clean_resume_for_tex
from dynamic_resume.utils.tex_to_pdf import tex_to_pdf
from dynamic_resume.config import set_data_path


def generate_resume_obj(data_path: t.Optional[str | PathLike] = None) -> Resume:
    if data_path is not None:

        set_data_path(data_path)
    from dynamic_resume.config import DATA_PATH

    if DATA_PATH is None:
        raise ValueError(
            "DATA_PATH is not set. Please provide a valid data path."
        )

    resume_data = get_resume_data(DATA_PATH)
    return build_resume_from_dict(resume_data)


def generate(
    resume_data_or_path: Resume | str | PathLike,
    template_path: t.Optional[str | PathLike] = None,
    tex_output_path: t.Optional[str | PathLike] = None,
    pdf_output_path: t.Optional[str | PathLike] = None,
    tex_file_name: t.Optional[str | PathLike] = None,
    pdf_file_name: t.Optional[str | PathLike] = None,
    generate_tex: bool = True,
    generate_pdf: bool = True,
) -> Resume:
    if isinstance(resume_data_or_path, (str, PathLike)):
        resume = generate_resume_obj(resume_data_or_path)
    else:
        resume = resume_data_or_path

    if generate_tex:

        cleaned = clean_resume_for_tex(resume)

        tex_output_path = render_to_tex(
            cleaned,
            output_file_name=tex_file_name,
            output_dir=tex_output_path,
            template_path=template_path,
        )

    if generate_pdf:
        if not tex_output_path:
            raise ValueError(
                "To generate PDF, TeX generation must be enabled or TeX output path must be provided."
            )

        tex_to_pdf(tex_output_path, pdf_output_path, pdf_file_name=pdf_file_name)

    return resume
