
from .mount import Mount
from .render import Render

class Dom(
    Mount,
    Render
):
    """
        Zenaura virtual dom.
        Mount is responsible for mounting lifecycle of component.
        Render is responsible for rendering lifecycle of component.
    """