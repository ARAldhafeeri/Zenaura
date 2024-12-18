from zenaura.client.tags import Node, HTMLElement, Attribute
from zenaura.client.page import Page 
from zenaura.client.config import ZENAURA_DOM_ATTRIBUTE
from zenaura.web.utils import document, in_browser


class HydratorRealDomAdapter:
    # for testing 
    """
        hyderator adapter for all real dom operations
        methods should start with:
        hyd_romp_
    """


    def hyd_rdom_create_element(self, virtual_node: Node) -> HTMLElement:
        """
        DOM operation: creates html element and returns it as HTMLElement

        Args:
            virtual_node: Node - the virtual node representing the element to be created

        Returns:
            HTMLElement - the created HTML element
        """
        element = document.createElement(virtual_node.name)
        
        return element
    
    def hyd_rdom_attach_to_root(self, html : str) -> None:
        """
        DOM operation: attaches compiled_comp to mounted_comp_id

        Args:
            html: str - the HTML string to be attached to the root element
        """
        document.getElementById("root").innerHTML = html

    def hyd_rdom_attach_to_mounted_comp(
            self,
            mounted_comp_id: str,
            html: str
    ):
        """
        DOM operation: attaches compiled_comp to mounted_comp_id

        Args:
            mounted_comp_id: str - the ID of the previously mounted component
            html: str - the HTML string to be attached to the mounted component
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

        Args:
            mounted_comp_id: str - the ID of the element to be removed
        """
        element = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{mounted_comp_id}"]')
        if element:
            element.parentNode.removeChild(element)
   
    
    def hyd_rdom_append_child(self, mounted_comp_id:str, child_html:str) -> None:
        """
        DOM operation: appends a child to an element

        Args:
            mounted_comp_id: str - the ID of the parent element
            child_html: str - the HTML string of the child element to be appended
        """
        element = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{mounted_comp_id}"]')
        if element:
            child_node = document.createElement("template")
            child_node.innerHTML = child_html
            element.appendChild(child_node.content.firstChild)

    def hyd_rdom_append_child_after(self, parent_node_id, child_node_id, child_html) -> None:
        """
        DOM operation: appends a child to an element after a specific child

        Args:
            parent_node_id: str - the ID of the parent element
            child_node_id: str - the ID of the child element to insert after
            child_html: str - the HTML string of the child element to be appended
        """
        element = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{parent_node_id}"]')
        if element : # if parent exists
            child_node = document.createElement("template")
            child_node.innerHTML = child_html
            curr_node = child_node.content.firstChild
            child_index = int( child_node_id[-1])
            prev_child = child_index - 1 # child on the dom to insert the new child after it
            prev_child_id = child_node_id[:-1] + str(prev_child) # parent-childIndex
            prev_child = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{prev_child_id}"]')
            if prev_child: # insert after the current child:
                element.insertBefore(curr_node, prev_child.nextSibling)
            else: # parent is a leaf no children
                element.append(curr_node)
            pass

    def hyd_rdom_remove_child(self, child_id:str) -> None:
        """
        DOM operation: removes a child of an element

        Args:
            child_id: str - the ID of the child element to be removed
        """
        child_node = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{child_id}"]')
        if child_node:
            child_node.outerHTML = ""


    def hyd_rdom_add_text_render(self, mounted_comp_id: str, text_content: str) -> None:
        """
        DOM operation: Adds a text node to an element.

        Args:
            mounted_comp_id: str - the ID of the element to add the text node to
            text_content: str - the text content of the text node
        """
        element = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{mounted_comp_id}"]')
        if element:
            text_node = document.createTextNode(text_content)
            element.appendChild(text_node)
            

    def hyd_rdom_replace_inner_text(self, mounted_comp_id: str, new_text: str) -> None:
        """
        DOM operation: Replaces the inner text content of an element.

        Args:
            mounted_comp_id: str - the ID of the element to replace the text content of
            new_text: str - the new text content
        """
        element = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{mounted_comp_id}"]')
        if element:
            element.textContent = new_text

    def hyd_rdom_is_interactive(self) -> bool:
        """
        DOM operation: checks if real dom  is interactive

        Returns:
            bool - True if the DOM is interactive, False otherwise
        """
        return document.readyState == "interactive"

    def hyd_rdom_is_complete(self) -> bool:
        """
        DOM operation: checks if real dom  is complete

        Returns:
            bool - True if the DOM is complete, False otherwise
        """
        return document.readyState == "complete"
    
    def hyd_rdom_is_loading(self) -> bool:
        """
        DOM operation: checks if real dom  is complete

        Returns:
            bool - True if the DOM is complete, False otherwise
        """
        return document.readyState == "load"
    
    def hyd_rdom_is_content_loaded(self) -> bool:
        """
        DOM operation: checks if real dom  is content loaded

        Returns:
            bool - True if the DOM is content loaded, False otherwise
        """
        return document.readyState == "DOMContentLoaded"
        

    def hyd_rdom_toggle_pages_visibilty(self, previous_page : Page, current_page : Page ):
        """
        Toggles the visibility of the previous and current pages.

        Args:
            previous_page: Page - the previously mounted page
            current_page: Page - the currently mounted page
        """
        p_page = document.querySelector(f'[data-zenaura="{previous_page.id}"]')
        if p_page:
            p_page.hidden = True
        curr_page = document.querySelector(f'[data-zenaura="{current_page.id}"]')
        if curr_page:
            curr_page.hidden = False # Update the title