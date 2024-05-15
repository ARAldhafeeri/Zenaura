from zenaura.client.tags import Node
from zenaura.client.compiler import compiler
from zenaura.client.config import ZENAURA_DOM_ATTRIBUTE
from zenaura.client.component import Component
from typing import List

class HyderatorCompilerAdapter:
    """
        hyderator adapter for all real dom operations
        methods should start with:
        hyd_comp_
    """        
    def hyd_comp_get_keyed_uuid(
        componentId : str, 
        level : int, 
        child_index : int, 
        path : str
    ):
        """
            compiler operation : wraps compiler.getKeyedUID 
        """
        return compiler.getKeyedUID(
            componentId, 
            level, 
            child_index, 
            path
        )
    
    def hyd_comp_compile_node(
        comp_tree: Node,
        comp: Component
    ):
        """
            compiler operation : wraps compiler compile, returns str "HTMLElement"
        """
        return compiler.compile(
                comp_tree, 
                componentId=comp.componentId,
                zenaura_dom_mode=True
            )