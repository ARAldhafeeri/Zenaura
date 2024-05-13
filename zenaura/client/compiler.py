from zenaura.client.tags import Node, Attribute
from typing import List 
from zenaura.client.config import (
    allowed_tags,
    allowed_attributes,
    ZENAURA_DOM_ATTRIBUTE,
    self_closing_tags
)
import io 
import html
import re
import bleach



class Compiler:
    def __init__(self):
        """
            Constructor for the Compiler class.
            Initializes the attribute keyword mapping.

            Args:
                self: The Compiler instance.

            Returns:
                None
        """
        self.attrKeyWords= {
             "styles" : "class"
        }


    def sanitize(self, user_input, allowed_tags=allowed_tags, allowed_attributes=allowed_attributes):
        """
        Sanitizes user input to prevent various injection attacks.

        Args:
            user_input (str): The raw user input to sanitize.
            allowed_tags (list): A list of allowed HTML tags (e.g., ['p', 'br', 'strong']).
            allowed_attributes (dict): A dictionary mapping allowed tags to their allowed 
                                    attributes (e.g., {'img': ['src', 'alt']}).  

        Returns:
            str: The sanitized input.
        """
        user_input = str(user_input)
        
        safe_html = html.escape(user_input)  # Escape all HTML special characters initially
        safe_html = bleach.clean(safe_html, tags=allowed_tags, attributes=allowed_attributes) 
      

        return safe_html 
    
    def compile(self, elm: Node, componentName=None, zenaura_dom_mode=False):
        """
        Compiles a Zenui Node into its corresponding HTML representation.

        Args:
            elm (Node): The Zenui Node object to compile.
            componentName (str, optional): For event handling attributes like onclick.
            zenaura_dom_mode (bool, optional): Adds unique attribute for virtual dom.

        Returns:
            str: A string containing the compiled HTML.
        """
        if not isinstance(elm, Node):
            return self.sanitize(elm[0])

        tag = elm.name 

        zenui_id = ""

        #  assign unique id for zenui dom
        if isinstance(elm, Node) and zenaura_dom_mode:
            zenui_id = f' {ZENAURA_DOM_ATTRIBUTE}="{elm.nodeId}"'

        # get node attributes
        attributes = self.process_attributes(elm.attributes, componentName)
        
        if tag in self_closing_tags:
            return f"<{tag}{zenui_id}{attributes}>"
        
        # start tag
        html = f"<{tag}{zenui_id}{attributes}>"

        # get children
        for child in elm.children:
            if  isinstance(child, Node):
                html += self.compile(child, zenaura_dom_mode=zenaura_dom_mode)
            else:
                if isinstance(child, list):
                    html += self.sanitize(child[0])
                else: 
                    html += self.sanitize(child)
                    
        html += f'</{tag}>'

        # finish tag
        return html

    def process_attributes(self, attrs: List[Attribute], componentName=None) -> str:
        """
            Processes a list of Attributes, converting them to HTML-formatted attributes.

            Args:
                attrs (List[Attribute]): A list of Zenui Attribute objects.
                componentName (str, optional): For event handling attributes like onclick.

            Returns:
                str: A string containing the HTML-formatted attributes, ready to be included in a tag.
        """

        s = io.StringIO()  # Create a string buffer for building the output

        for i, attr in enumerate(attrs):
            attrKey = attr.key
            attrValue = attr.value
            if attrKey in self.attrKeyWords.keys():
                attrKey = self.attrKeyWords[attrKey]  # Apply keyword mapping

            # Add space only if it's not the first or last attribute
            if i == 0 or i == len(attrs) - 1:
                s.write(f' {attrKey}="{attrValue}"')
            else:
                s.write(f'{attrKey}="{attrValue}" ')

        res = s.getvalue()
        s.close()
        return res