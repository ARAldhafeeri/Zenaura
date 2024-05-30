from .mount import Mount
from .render import Render

class Dom(
    Mount,
    Render
):
    """
    Zenaura virtual DOM.

    This class combines the functionalities of `Mount` and `Render` classes to provide a comprehensive virtual DOM implementation.

    **Attributes:**

    * **Mount:** Inherits all attributes and methods from the `Mount` class, which handles the mounting lifecycle of components.
    * **Render:** Inherits all attributes and methods from the `Render` class, which handles the rendering lifecycle of components.

    **Methods:**

    * **mount(comp, container):** Mounts the component to the specified container element in the real DOM.
    * **render(comp):** Renders the component to a virtual DOM tree.
    * **update(prev_comp, new_comp):** Updates the real DOM based on the differences between the previous and new virtual DOM trees.

    **Usage:**

    ```python
    # Create a Dom instance
    dom = Dom()

    # Create a component
    comp = MyComponent()

    # Mount the component to a container element
    dom.mount(comp, container)

    # Render the component
    dom.render(comp)

    # Update the component
    dom.update(prev_comp, new_comp)
    ```
    """
