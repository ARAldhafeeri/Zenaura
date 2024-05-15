from zenaura.client.tags import Node
from zenaura.client.tags import HTMLElement
from zenaura.client.component import Component
from pyscript import document

class HyderatorRealDomAdapter:
    """
        hyderator adapter for all real dom operations
        methods should start with:
        hyd_romp_
    """

    def hyd_rdom_create_element(self, virtual_node: Node) -> HTMLElement:
        """
            DOM operation : creates html element and returns it as HTMLElement
        """
        element = self.document.createElement(virtual_node.tag_name)
        
        return element

    def hyd_rdom_attach_to_root(self, comp : Component) -> None:
        """
            atttach page to root
            args:
                page: Page
        """
        dom_node = document.getElementById("root")
        compiled_comp = self.compile_node(comp.node(), comp)
        dom_node.innerHTML = compiled_comp

    def hyd_rdom_attach_to_mounted_comp(
            self,
            mounted_comp_id: str,
            compiled_comp: str
    ):
        """
            DOM operation : attaches compiled_comp to mounted_comp_id
            args:
                mounted_comp_id: str previosuly mounted component id
                compiled_comp: str compiled html from comp.node()
        """
        foundNode = document.querySelector(f'[{mounted_comp_id}="{mounted_comp_id}"]')
        if foundNode:
            foundNode.outerHTML = compiled_comp
