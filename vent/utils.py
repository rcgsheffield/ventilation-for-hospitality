import pathlib
from typing import Union

import jinja2


def render_template(path: Union[pathlib.Path, str], **kwargs) -> str:
    path = pathlib.Path(path)
    with path.open() as file:
        template = jinja2.Template(file.read())
    return template.render(**kwargs)
