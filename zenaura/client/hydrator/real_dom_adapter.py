from zenaura.client.tags import Node, HTMLElement, Attribute
from zenaura.client.component import Component
from zenaura.client.config import ZENAURA_DOM_ATTRIBUTE
from pyscript import document
from typing import Dict

class HydratorRealDomAdapter:
    # for testing 
    """
        hyderator adapter for all real dom operations
        methods should start with:
        hyd_romp_
    """


    def hyd_rdom_create_element(self, virtual_node: Node) -> HTMLElement:
        """
            DOM operation : creates html element and returns it as HTMLElement
        """
        element = document.createElement(virtual_node.name)
        
        return element
    
    def hyd_rdom_attach_to_root(self, html : str) -> None:
        """
            atttach page to root
            args:
                page: Page
        """
        document.getElementById("root").innerHTML = html

    def hyd_rdom_attach_to_mounted_comp(
            self,
            mounted_comp_id: str,
            html: str
    ):
        """
            DOM operation : attaches compiled_comp to mounted_comp_id
            args:
                mounted_comp_id: str previosuly mounted component id
                compiled_comp: str compiled html from comp.node()
        """
        foundNode = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{mounted_comp_id}"]')
        if foundNode:
            foundNode.outerHTML = html

    def hyd_rdom_set_attribute(self, mounted_comp_id: str, attribute: Attribute) -> None:
        """
        DOM operation: Sets attributes on an HTML element.

        Args:
            mounted_comp_id: The ID of the element to modify.
            attributes: A dictionary of attribute names and their values.
        """
        element = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{mounted_comp_id}"]')
        if element:
            element.setAttribute(attribute.key, attribute.value)


    def hyd_rdom_remove_attribute(self, mounted_comp_id: str, attribute_name: str) -> None:
        """
        DOM operation: Removes an attribute from an HTML element.

        Args:
            mounted_comp_id: The ID of the element.
            attribute_name: The name of the attribute to remove.
        """
        element = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{mounted_comp_id}"]')
        if element:
            element.removeAttribute(attribute_name)

    def hyd_rdom_remove_element(self, mounted_comp_id: str) -> None:
        """
        DOM operation: removes an element from the DOM
        args:
            mounted_comp_id: str
        """
        element = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{mounted_comp_id}"]')
        if element:
            element.parentNode.removeChild(element)
   
    
    def hyd_rdom_append_child(self, mounted_comp_id:str, child_html:str) -> None:
        """
        DOM operation: appends a child to an element
        """
        element = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{mounted_comp_id}"]')
        if element:
            child_node = document.createElement("div")
            child_node.innerHTML = child_html
            element.appendChild(child_node)

    def hyd_rdom_remove_child(self, mounted_comp_id:str, child_id:str) -> None:
        """
        DOM operation: removes a child of an element
        """
        element = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{mounted_comp_id}"]')
        if element:
            child_node = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{child_id}"]')
            if child_node:
                element.removeChild(child_node)


    def hyd_rdom_add_text_node(self, mounted_comp_id: str, text_content: str) -> None:
        """
        DOM operation: Adds a text node to an element.
        """
        element = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{mounted_comp_id}"]')
        if element:
            text_node = document.createTextNode(text_content)
            element.appendChild(text_node)
            

    def hyd_rdom_replace_inner_text(self, mounted_comp_id: str, new_text: str) -> None:
        """
        DOM operation: Replaces the inner text content of an element.
        """
        element = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{mounted_comp_id}"]')
        if element:
            text_node = document.createTextNode(new_text)
            first_child = element.childNodes[0]
            element.removeChild(first_child)
            element.appendChild(text_node)

    def hyd_rdom_is_interactive(self) -> bool:
        """
        DOM operation: checks if real dom  is interactive
        """
        return document.readyState == "interactive"

    def hyd_rdom_is_complete(self) -> bool:
        """
        DOM operation: checks if real dom  is complete
        """
        return document.readyState == "complete"
    
    def hyd_rdom_is_loading(self) -> bool:
        """
        DOM operation: checks if real dom  is loading
        """
        return document.readyState == "load"
    
    def hyd_rdom_is_content_loaded(self) -> bool:
        """
        DOM operation: checks if real dom  is content loaded
        """
        return document.readyState == "DOMContentLoaded"
