import re


def escape_string(s: str, for_tex: bool = True) -> str:
    if for_tex:
        s = re.sub(r"(\\)", r"\\textbackslash{}", s)
    return re.sub(r"([\\%#{}&$])", r"\\\1", s)
