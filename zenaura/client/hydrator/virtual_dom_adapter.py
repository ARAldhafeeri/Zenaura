from zenaura.client.component import Component
from .lookup import VDomLookupTable

class HydratorVirtualDomAdapter(
    VDomLookupTable
):
    """
        hyderator adapter for all virtual dom operations
        methods should start with:
        hyd_vdom_
    """

    def hyd_vdom_update(self, comp: Component) -> None:
        """
            virtual dom operation : updates virtual dom of component
            args:
                comp: Component
        """
        self.zen_dom_table[comp.id] = comp.render()

    def hyd_vdom_delete(self, comp: Component) -> None:
        """
            virtual dom operation : deletes virtual dom of component
            args:
                comp: Component
        """
        del self.zen_dom_table[comp.id]

    def hyd_vdom_update_with_new_render(self, comp: Component, new_node):
        """
            update component with new node
            args:
                comp: Component
                new_node: Node
        """
        self.zen_dom_table[comp.id] = new_node
