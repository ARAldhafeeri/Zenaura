from zenaura.client.tags import Node, Data
from .attribute import AttributeProccessor
from .sanitize import CompilerSanitizer
import io
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
    
    def getKeyedUID(self, 
                    id, 
                    withAttribut=False, 
                    path=None
                ):
        """
            from unique UID for component generate unique
            keyed UUID for each child within the component tree.
            This is used to create keyed ZENAURA_DOM_ATTRIBUTE

            args :
                id (str): unique id for the component
                level (int): level of the component tree
                child index (int): index of the child within the component tree
                withAttribute (bool, optional): adds unique attribute for virtual dom.
            used in :
                - compiler
                - mount life cycle 
                - render life cycle
            returns :
                if withAttribute is True :
                {ZENAURA_DOM_ATTRIBUTE}="{id}-{level}-{child_index}"
                else :
                {id}-{level}-{child_index}
        """
        if withAttribut:
            return f' {ZENAURA_DOM_ATTRIBUTE}="{id}{path}"'
        return f'{id}{path}'
    
    def compile(
        self, 
        elm: Node,
        id=None, 
        zenaura_dom_mode=False
    ):
        """
        Compiles a Zenui Node into its corresponding HTML representation.

        Args:
            elm (Node): The Zenui Node object to compile.
            id (str, optional): used to create keyed ZENAURA_DOM_ATTRIBUTE
            attribute UID-parent-child-child-child on so on.
            zenaura_dom_mode (bool, optional): Adds unique attribute for virtual dom.

        Returns:
            str: A string containing the compiled HTML.
        """
        if elm.is_text_node or isinstance(elm, str):
            return self.sanitize(elm.text)

        tag = elm.name 

        zenui_id = ""
    
        #  assign unique id for zenui dom
        if isinstance(elm, Node) and zenaura_dom_mode:
            zenui_id = self.getKeyedUID(
                id, 
                withAttribut=True, 
                path="" # should be from node.path
            )

        # get node attributes
        attributes = self.process_attributes(elm.attributes)
        
        if tag in self_closing_tags:
            return f"<{tag}{zenui_id}{attributes}>"
        
        # start tag
        html = io.StringIO()
        html.write(f"<{tag}{zenui_id}{attributes}>")

        # get children
        for child in elm.children:
            html.write(
                self.compile(
                    child, 
                    id, 
                    zenaura_dom_mode, 
                )
            )

                    
        html.write(f"</{tag}>")

        # finish tag
        return html.getvalue()