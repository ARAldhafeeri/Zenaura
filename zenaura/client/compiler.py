from zenaura.client.tags import Node, Attribute
from typing import List 
import io 
import html
import re
import bleach

class ZenuiCompiler:
    def __init__(self):
        self.attrKeyWords= {
             "styles" : "class"
        }


    def sanitize(self, user_input, allowed_tags=None, allowed_attributes=None):
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

        # # 1. Input Validation (using regular expressions for flexibility)
        # safe_chars = re.compile(r"[^\w\s\.,\-+=@#$%^&*()]")  # Customize this allowed character list

        # if not safe_chars.sub("", user_input) == user_input:  
        #     raise ValueError("Invalid characters detected in input")

        # 2. HTML Sanitization (if necessary)
        user_input = str(user_input)
        if allowed_tags:
            safe_html = html.escape(user_input)  # Escape all HTML special characters initially
            safe_html = bleach.clean(safe_html, tags=allowed_tags, attributes=allowed_attributes) 
        else:
            safe_html = html.escape(user_input)

        return safe_html 
    
    def compile(self, elm: Node, componentName=None, zenaura_dom_mode=False):
        """Compiles a Zenui Node into its corresponding HTML representation.

        Args:
            elm: The Zenui Node object to compile.
            parent: true by default, zenui set data-zenui-id to every parent component
            the data-zenui-id will be used in zenui-dom functionality
            in tests, if not testing zenui-dom, set this to false.
            componentName: for event handling attributes like onclick,
            transcript needs the following format : 
            "index.componentName.eventHandler"
            this must be the output for every event handler
            otherwise the component event handler will not work.
            passed optionally as None for testing purposes.
            zenaura_dom_mode : adds unique attribute for virtual dom 
            data-zenui-id=uuid4

        Returns:
            A string containing the compiled HTML.
        """
        if not isinstance(elm, Node):
            return elm[0]

        tag = elm.name 

        zenui_id = ""

        #  assign unique id for zenui dom
        if isinstance(elm, Node) and zenaura_dom_mode:
            zenui_id = f'data-zenui-id="{elm.nodeId}"'

        # get node attributes
        attributes = self.process_attributes(elm.attributes, componentName)

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
        """Processes a list of Attributes, converting them to HTML-formatted attributes.

        Args:
            attrs: A list of Zenui Attribute objects.

        Returns:
            A string containing the HTML-formatted attributes, ready to be included in a tag.
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