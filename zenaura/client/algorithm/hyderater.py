from zenaura.client.tags import Node, Data
from zenaura.client.tags import HTMLElement
from typing import List
from pyscript import document

class Hyderater:
    """
        Hyderation step in zenaura virtual dom algorithm.
    """
    element_cache = {}
    document = document

    def hydrate(self, virtual_dom: Node, container: HTMLElement) -> None:
        self._hydrate_node(virtual_dom, container)

    def _hydrate_node(self, virtual_node: Node, parent_element: HTMLElement) -> None:
        if isinstance(virtual_node, Data):
            text_node = self.document.createTextNode(virtual_node.value)
            parent_element.appendChild(text_node)
        else:
            element = self.create_element(virtual_node)
            parent_element.appendChild(element)
            for child_node in virtual_node.children:
                self._hydrate_node(child_node, element)

    def create_element(self, virtual_node: Node) -> HTMLElement:
        element = self.document.createElement(virtual_node.tag_name)
        for attribute_name, attribute_value in virtual_node.attributes.items():
            element.setAttribute(attribute_name, attribute_value)
        return element

    def update_element(self, virtual_node: Node, element: HTMLElement) -> None:
        # Update attributes
        for attribute_name, attribute_value in virtual_node.attributes.items():
            element.setAttribute(attribute_name, attribute_value)

        # Update children
        # ...

    def remove_element(self, element: HTMLElement) -> None:
        element.parentNode.removeChild(element)