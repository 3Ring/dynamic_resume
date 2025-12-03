from pydantic import BaseModel


def prettify(obj: BaseModel) -> str:
    dump = obj.model_dump()
    out = [obj.__class__.__name__]
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

    compile(dump)
    return "\n".join(out)
