
from .compiler_adapter import HyderatorCompilerAdapter
from .real_dom_adapter import HyderatorRealDomAdapter
from .virtual_dom_adapter import HyderatorVirtualDomAdapter



class Hyderator(
    HyderatorVirtualDomAdapter,
    HyderatorCompilerAdapter,
    HyderatorRealDomAdapter
):
    """
        Hyderator is the bridge of communication between:
        1. Virtual dom and compiler :
            methods that communicate with the compiler
            should start with:
            hyd_comp_
            e.g. :
            hyd_comp_get_keyed_uuid
            hyd_comp_compile_node
        2. Virtual dom : 
            methods that interact with zenaura virtual dom.
            should start with:
            hyd_vdom_
            e.g. :
            hyd_vdom_update
            hyd_vdom_delete
        3. DOM : 
            methods that interact with the DOM.
            should start with:
            hyd_dom_
            e.g. :
            hyd_rdom_attach_to_root
    """