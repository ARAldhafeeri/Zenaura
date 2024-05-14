from zenaura.client.tags import Node, Data
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
    
    def getKeyedUID(self, 
                    componentId, 
                    level, 
                    child_index, 
                    withAttribut=False, 
                    path=None
                ):
        """
            from unique UID for component generate unique
            keyed UUID for each child within the component tree.
            This is used to create keyed ZENAURA_DOM_ATTRIBUTE

            args :
                componentId (str): unique id for the component
                level (int): level of the component tree
                child index (int): index of the child within the component tree
                withAttribute (bool, optional): adds unique attribute for virtual dom.
            used in :
                - compiler
                - mount life cycle 
                - render life cycle
            returns :
                if withAttribute is True :
                {ZENAURA_DOM_ATTRIBUTE}="{componentId}-{level}-{child_index}"
                else :
                {componentId}-{level}-{child_index}
        """
        if withAttribut:
            return f' {ZENAURA_DOM_ATTRIBUTE}="{componentId}{path}"'
        return f'{componentId}{path}'
    
    def compile(
        self, 
        elm: Node,
        componentId=None, 
        zenaura_dom_mode=False,
        level=0,
        child_index=0,
        path=""
    ):
        """
        Compiles a Zenui Node into its corresponding HTML representation.

        Args:
            elm (Node): The Zenui Node object to compile.
            componentId (str, optional): used to create keyed ZENAURA_DOM_ATTRIBUTE
            attribute UID-parent-child-child-child on so on.
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
            zenui_id = self.getKeyedUID(
                componentId, 
                level, 
                child_index, 
                withAttribut=True, 
                path=path
            )

        # get node attributes
        attributes = self.process_attributes(elm.attributes)
        
        if tag in self_closing_tags:
            return f"<{tag}{zenui_id}{attributes}>"
        
        # start tag
        html = f"<{tag}{zenui_id}{attributes}>"

        # get children
        for idx, child in enumerate(elm.children):
            if  isinstance(child, Node):
                path += f"{level}{idx}"
                html += self.compile(
                    child, 
                    componentId, 
                    zenaura_dom_mode=zenaura_dom_mode,
                    level=level,
                    child_index=child_index,
                    path=path
                )
                child_index += idx
                level += 1
            
            if isinstance(child, list):
                if isinstance(child[0], Data):
                    html += self.sanitize(child[0].content)
                else:
                    html += self.sanitize(child[0])

            if isinstance(child, str):
                html += self.sanitize(child)

                    
        html += f'</{tag}>'

        # finish tag
        return html