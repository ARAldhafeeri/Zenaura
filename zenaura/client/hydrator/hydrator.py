
from .compiler_adapter import HydratorCompilerAdapter
from .real_dom_adapter import HydratorRealDomAdapter
from .virtual_dom_adapter import HydratorVirtualDomAdapter
from .tasker import HydratorTasker



class Hydrator(
    HydratorVirtualDomAdapter,
    HydratorCompilerAdapter,
    HydratorRealDomAdapter,
    HydratorTasker
):
    """
    Hydrator acts as the central communication hub between:

    1. **Virtual DOM and Compiler:**
        - Methods interacting with the compiler start with `hyd_comp_`, e.g., `hyd_comp_get_keyed_uuid`, `hyd_comp_compile_node`.
    2. **Virtual DOM:**
        - Methods interacting with Zenaura's virtual DOM start with `hyd_vdom_`, e.g., `hyd_vdom_update`, `hyd_vdom_delete`.
    3. **DOM:**
        - Methods interacting with the DOM start with `hyd_dom_`, e.g., `hyd_rdom_attach_to_root`.
    4. **Tasker:**
        - Tasks for updating the DOM are created in the updater and dequeued during the render lifecycle, enabling asynchronous DOM updates.

    Essentially, Hydrator bridges the gap between various components within the Zenaura framework, facilitating seamless communication and efficient DOM manipulation.
    """