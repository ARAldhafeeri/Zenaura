
from .lookup import VDomLookupTable
from .compiler_adapter import HyderatorCompilerAdapter
from .real_dom_adapter import HyderatorRealDomAdapter
from zenaura.client.component import Component


class Hyderator(
    VDomLookupTable,
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
    def hyd_vdom_update(self, comp: Component) -> None:
        """
            virtual dom operation : updates virtual dom of component
            args:
                comp: Component
        """
        self.zen_dom_table[comp.componentId] = comp.node()

    def hyd_vdom_delete(self, comp: Component) -> None:
        """
            virtual dom operation : deletes virtual dom of component
            args:
                comp: Component
        """
        del self.zen_dom_table[comp.componentId]