from zenaura.client.tags import Node
from .attribute import AttributeProccessor
from .sanitize import CompilerSanitizer
from zenaura.client.config import (
    ZENAURA_DOM_ATTRIBUTE,
    self_closing_tags
)



class Compiler(
    CompilerSanitizer,
    AttributeProccessor,
):
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