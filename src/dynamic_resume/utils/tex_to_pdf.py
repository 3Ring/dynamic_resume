import typing as t
import shutil
from pathlib import Path
import subprocess
from os import PathLike



def tex_to_pdf(
    tex_file: str | PathLike,
    output_dir: t.Optional[str | PathLike] = None,
    pdf_file_name: t.Optional[str] = None,
) -> None:
    if output_dir is None:
        output_dir = Path.cwd()
    else:
        output_dir = Path(str(output_dir)).expanduser().resolve()
    tex_file = Path(str(tex_file)).expanduser().resolve()
    print(f"Converting {tex_file} to PDF in {output_dir}")
    if not shutil.which("pdflatex"):
        raise EnvironmentError("pdflatex is not installed or not found in PATH")
    subprocess.run(
        [
            "pdflatex",
            "-output-directory",
            output_dir,
            tex_file
        ],
        check=True,
    )
    if pdf_file_name:
        print(f"Renaming generated PDF to {pdf_file_name}")
        generated_pdf = Path(output_dir) / (Path(tex_file).stem + ".pdf")
        target_pdf = Path(output_dir) / pdf_file_name
        generated_pdf.rename(target_pdf)
